import requests
from time import sleep
from request_strategies import RequestStrategies as RS

MONGO_URL = "http://ua-1185-mongo-system-api.us-e2.cloudhub.io/api"

PAYLOAD = "payload"
ROCKET = "rocket"
LAUNCH = "launch"
LAUNCHPAD = "launchpad"
ALL = "all"

class DatabaseFiller:
    strategies = {
        PAYLOAD: ("payloads", RS.create_soap_request_for_payload),
        ROCKET: ("rockets", RS.create_soap_request_for_rocket),
        LAUNCH: ("launches", RS.create_soap_request_for_launch),
        LAUNCHPAD: ("launchpads", RS.create_soap_request_for_launchpad)
    }
    dataset = {}

    def __init__(self, strategy_name) -> None:
        if strategy_name == ALL:
            for k, v in self.strategies.items():
                self.dataset[k] = self.create_dataset_for_entity(*v)
        else:
            self.dataset[strategy_name] = self.create_dataset_for_entity(*self.strategies.get(strategy_name))
            

    def fetch_spacex_data(self, endpoint, **kwargs): 
        base_url = "https://api.spacexdata.com/v4/"
        res = requests.get(base_url + endpoint, **kwargs)
        return res.json()
    
    def create_dataset_for_entity(self, endpoint, strategy):
        data = self.fetch_spacex_data(endpoint)
        return [strategy(record) for record in data]
 
    def save_soap_requests(self):
        for entity, requests in self.dataset.items():
            filename = f"{entity.title()}SoapRequests.xml"
            with open(filename, "w", encoding='utf-8') as file:
                for request in requests:
                    file.write(request + "\n")

    def create_records(self, url=None):
        db_url = 'http://ua-1185-mysql-system-api.us-e2.cloudhub.io/SpaceXdbService/SpaceXdbServiceSoapPort' if not url else url
        
        for entity, request_array in self.dataset.items():
            for request in request_array:
                try:
                    sleep(4)
                    response = requests.post(db_url, data=request.encode('utf-8'), headers={"Content-Type": "application/xml", "Accept-Encoding": "gzip, deflate, br"})
                    response.raise_for_status()  
                    print("Created succeffuly")  
                except requests.HTTPError as e:
                    print(response)
                    continue



payloads = DatabaseFiller(ROCKET)

payloads.create_records()
