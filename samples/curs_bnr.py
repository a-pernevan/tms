import requests
import xml.etree.ElementTree as ET
from database.datab import cursor, connection

class CursBNR():

    def __init__(self):

        self.url = "https://www.bnr.ro/nbrfxrates.xml"
        self.response = requests.get(self.url)

        if self.response.status_code == 200:
            self.xml_content = self.response.text
            # print(xml_content)
            self.root = ET.fromstring(self.xml_content)

        else:
            print("Failed to retrieve XML file.")

        # Parse the XML file
        # tree = ET.parse(xml_content)

        # Get the root element
        # root = tree.getroot()

        # Define the namespace (required to find elements correctly)
        self.namespace = {'ns': 'http://www.bnr.ro/xsd'}

        # Extract the publishing date from the Cube element
        self.cube = self.root.find('.//ns:Cube', self.namespace)
        self.date = self.cube.attrib['date']
        # print(f"Date: {date}")

        connection._open_connection()
        cursor.execute("SELECT * from curs_bnr WHERE data = %s", (self.date,))
        self.result = cursor.fetchall()

        # print(len(result))

        # Iterate over all Rate elements within the Cube
        # print("Currency Exchange Rates:")

        if len(self.result) == 0:

            for rate in self.cube.findall('ns:Rate', self.namespace):
                self.currency = rate.attrib['currency']
                self.value = rate.text
                # connection._open_connection()
                sql = "INSERT INTO curs_bnr (data, valuta, valoare) VALUES (%s, %s, %s)"
                values = (self.date, self.currency, self.value)
                cursor.execute(sql, values)
                # connection.commit()
                # connection.close()
                # print(f"{currency}: {value}")
        connection.commit()
        connection.close()

CursBNR()