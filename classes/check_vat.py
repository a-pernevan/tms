import requests
from datetime import date
import json

class Vies:
    def __init__(self, country, vat_no):
        self.country = country
        self.vat_no = vat_no

    def check_vies(self):
        self.address = f"https://ec.europa.eu/taxation_customs/vies/rest-api/ms/{self.country}/vat/{self.vat_no}"
        self.response = requests.get(self.address)
        self.data = self.response.json()
        # return self.data
        if self.data["isValid"]:
            return self.data["name"]
        else:
            return False
        
class Anaf:
    def __init__(self, vat_no):
        self.vat_no = vat_no
        self.today_date = date.today().strftime("%Y-%m-%d")
        self.headers = {"Content-Type": "application/json"}
        self.query_params = [{
            "cui": self.vat_no,
            "data": self.today_date
        }]
        self.api_addr = "https://webservicesp.anaf.ro/PlatitorTvaRest/api/v8/ws/tva"

    def check_anaf(self):
        self.response = requests.post(self.api_addr, data=json.dumps(self.query_params), headers=self.headers)
        self.data = self.response.json()
        # if self.data["found"]:
        if self.data["found"]:
            return self.data
        else:
            return False
