from datetime import datetime

def format_date(date): 
        dt = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")
        return dt.strftime("%Y-%m-%d")

class RequestStrategies:
    @classmethod
    def create_soap_request_for_launchpad(self, record):
        return f"""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:roc="http://example.com/rocketservice">
                                <soapenv:Header/>
                                <soapenv:Body>
                                    <roc:CreateLaunchpadRequest>
                                        <externalId>{record['id']}</externalId>
                                        <name>{record['name']}</name>
                                        <locality>{record['locality']}</locality>
                                        <region>{record['region']}</region>
                                        <status>{record['status']}</status>
                                    </roc:CreateLaunchpadRequest>
                                </soapenv:Body>
                            </soapenv:Envelope>"""
    @classmethod
    def create_soap_request_for_launch(self, record):
        return f"""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:roc="http://example.com/rocketservice">
                                <soapenv:Header/>
                                <soapenv:Body>
                                    <roc:CreateLaunchRequest>
                                        <externalId>{record['id']}</externalId>
                                        <success>{0 if not record['success'] else 1}</success>
                                        <details>{record.get('details', 'Details was not provided.')}</details>
                                        <launchName>{record['name']}</launchName>
                                        <date>{format_date(record['date_utc'])}</date>
                                        <rocketName>{record['rocket']}</rocketName> 
                                    </roc:CreateLaunchRequest>
                                </soapenv:Body>
                            </soapenv:Envelope>"""
    @classmethod
    def create_soap_request_for_rocket(self, record):
         return f"""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:roc="http://example.com/rocketservice">
                                <soapenv:Header/>
                                <soapenv:Body>
                                    <roc:CreateRocketRequest>
                                        <externalId>{record['id']}</externalId>
                                        <name>{record['name']}</name>
                                        <active>{0 if not record['active'] else 1}</active>
                                        <stages>{int(record['stages'])}</stages>
                                        <costPerLaunch>{record['cost_per_launch']}</costPerLaunch>
                                        <description>{record['description']}</description>
                                    </roc:CreateRocketRequest>
                                </soapenv:Body>
                            </soapenv:Envelope>"""
    
    def create_soap_request_for_payload(record):
         return f"""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:roc="http://example.com/rocketservice">
                                <soapenv:Header/>
                                <soapenv:Body>
                                    <roc:CreatePayloadRequest>
                                        <externalId>{record['id']}</externalId>
                                        <name>{record['name']}</name>
                                        <type>{record['type']}</type>
                                        <weight>{0 if not record['mass_kg'] else int(record['mass_kg'])}</weight>
                                        <orbit>{record['orbit']}</orbit>
                                        <apoapsis>{0 if not record['apoapsis_km'] else int(record['apoapsis_km'])}</apoapsis>
                                        <periapsis>{0 if not record['periapsis_km'] else int(record['periapsis_km'])}</periapsis>
                                    </roc:CreatePayloadRequest>
                                </soapenv:Body>
                            </soapenv:Envelope>"""
    



# def create_records_from_requests(filename, batch_size=10, delay=1):
#     url = 'http://ua-1185-mysql-system-api.us-e2.cloudhub.io/SpaceXdbService/SpaceXdbServiceSoapPort'
#     session = requests.Session()
#     session.headers.update({'Content-Type': 'application/xml'})

#     with open(filename, 'r') as file:
#         content = file.read()
#         records = content.split('</soapenv:Envelope>')
    
#     total_records = len(records)

#     for start in range(0, total_records, batch_size):
#         batch = records[start:start + batch_size]

#         for record in batch:
#             try:
#                 response = session.post(url, data=record)
#                 print(response.text)
#                 response.raise_for_status()
#             except requests.exceptions.RequestException as e:
#                 print(e)
        
#         print(f"Batch {start // batch_size + 1} processed. Waiting for {delay} seconds before next batch.")
#         sleep(delay)
    
#     session.close()