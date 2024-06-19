import requests
import json

class ExpensifyIntegration:
    def __init__(self, partner_user_id, partner_user_secret):
        self.partner_user_id = partner_user_id
        self.partner_user_secret = partner_user_secret
        self.api_url = 'https://integrations.expensify.com/Integration-Server/ExpensifyIntegrations'

    def create_request_job(self, job_type, input_type, domain):
        request_data = {
            "type":job_type,
            "credentials": {
                "partnerUserID": self.partner_user_id,
                "partnerUserSecret": self.partner_user_secret
            },
            "inputSettings": {
                "type": input_type,
                "domain": domain
            }
        }
        print(request_data)
        headers = {
                "Content-Type": "application/x-www-form-urlencoded"
            }
        data = 'requestJobDescription='+json.dumps(request_data)+'\''
        try:
            response = requests.post(self.api_url,headers=headers, data=data, timeout=60)
            response.raise_for_status()  # Raise exception for 4xx/5xx errors
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
    job_type = "get"
    input_type = "domainCardList"
    domain = "REPLACE"
    
    result = integration.create_request_job(job_type, input_type, domain)
    if result:
        print("Request job created successfully:")
        print(json.dumps(result, indent=4))