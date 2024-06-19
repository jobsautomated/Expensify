import requests
import json
from pathlib import Path

class ExpensifyIntegration:
    def __init__(self, partner_user_id, partner_user_secret):
        self.partner_user_id = partner_user_id
        self.partner_user_secret = partner_user_secret
        self.api_url = 'https://integrations.expensify.com/Integration-Server/ExpensifyIntegrations'

    def create_request_job(self, job_type, input_type):
        request_data = {
            "type":job_type,
            "credentials": {
                "partnerUserID": self.partner_user_id,
                "partnerUserSecret": self.partner_user_secret
            },
            "onReceive": {"immediateResponse":["returnRandomFileName"]},
            "inputSettings": {
                "type": input_type,
                "filters": {"reportIDList": "REPLACE"},
            },
            "outputSettings":{"fileExtension":"csv"},
            "onFinish":[{"actionName":"email","recipients":"REPLACE", "message":"Report is ready."}]
            }
        headers = {
                "Content-Type": "application/x-www-form-urlencoded"
            }
        home_dir = Path.home()
        file_path = home_dir / 'Expensify' / 'expensify_template.txt'
        try:
            with open(file_path,encoding='utf-8') as file:
                content = file.read()
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        #files = {'template':json.dumps(content)}
        data = {'requestJobDescription':json.dumps(request_data)+'\'','template':json.dumps(content)}
        try:
            response = requests.post(self.api_url,data=data,timeout=60)
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error creating request job: {e}")
            return None

# Example usage:
if __name__ == "__main__":
    # Replace with your actual credentials and API URL
    partner_user_id = "REPLACE"
    partner_user_secret = "REPLACE"

    integration  = ExpensifyIntegration(partner_user_id, partner_user_secret)

    # Example: Create request job
    job_type = "file"
    input_type = "combinedReportData"
    
    result = integration.create_request_job(job_type, input_type)
    if result:
        print("Request job created successfully:")
    print(json.dumps(result, indent=4))