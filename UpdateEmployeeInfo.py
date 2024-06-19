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
            "dry-run":False,
            "credentials": {
                "partnerUserID": self.partner_user_id,
                "partnerUserSecret": self.partner_user_secret
            },
            "dataSource": "request",
            "inputSettings": {
                "type": 'employees',
                "entity":"generic",
            "outputSettings": {"fileExtension":"csv"},
            "onFinish":[{"actionName":"email","recipients":"REPLACE", "message":"User is ready."}]
            }}
        headers = {
                "Content-Type": "application/x-www-form-urlencoded"
            }
        data_pass = {"Employee":[{"employeeEmail": "REPLACE",
                                        "managerEmail":"REPLACE",
                                        "policyID": "REPLACE",
                                        "isTerminated":"false",
                                        "employeeID":"API123",#Goes to CustomField 1
                                        "firstname":"John",
                                        "lastname":"Doe",
                                        "approvalLimit":"100",#In Pennies
                                        "overLimitApprover":"REPLACE"
                                        ,"additionalPolicyIDs":["REPLACE"]
                                        }
                                        #multiple emails
                                        #,{"employeeEmail": "REPLACE",
                                        #"managerEmail":"REPLACE",
                                        #"policyID": "31A57D25DF49A11E",
                                        #"isTerminated":"false",
                                        #"employeeID":"API123",#Goes to CustomField 1
                                        #"firstname":"John",
                                        #"lastname":"Doe",
                                        #"approvalLimit":"100",#In Pennies
                                        #"overLimitApprover":"REPLACE"
                                        #,"additionalPolicyIDs":"31A57D25DF49A11E" Does not work
                                        #}
                                        ]}
        data = {'requestJobDescription':json.dumps(request_data)+'\'','data':json.dumps(data_pass)}
        try:
            response = requests.post(self.api_url,data=data,timeout=60)
            response.raise_for_status()  # Raise exception for 4xx/5xx errors
            print(response)
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
    job_type = "update"
    input_type = "combinedReportData"
    
    result = integration.create_request_job(job_type, input_type)
    if result:
        print("Request job created successfully:")
        print(json.dumps(result, indent=4))