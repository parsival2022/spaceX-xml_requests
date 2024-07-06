import requests
from request_strategies import RequestStrategies as RS

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


payloads = DatabaseFiller(ALL)

payloads.save_soap_requests()

 

