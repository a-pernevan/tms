import requests

class Vies:
    def __init__(self, country, vat_no):
        self.country = country
        self.vat_no = vat_no

    def check(self):
        self.address = f"https://ec.europa.eu/taxation_customs/vies/rest-api/ms/{self.country}/vat/{self.vat_no}"
        self.response = requests.get(self.address)
        self.data = self.response.json()
        # return self.data
        if self.data["isValid"]:
            return self.data["name"]
        else:
            return False