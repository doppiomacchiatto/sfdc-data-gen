import csv
import os
import string
import uuid
import yaml
import random
from simple_salesforce import Salesforce


def create_session():
    with open('sf.yaml', 'r') as file:
        credentials = yaml.safe_load(file)
    # Salesforce credentials
    sf_username = os.environ.get('SALESFORCE_USERNAME')
    sf_password = os.environ.get('SALESFORCE_PASSWORD')
    sf_security_token = os.environ.get('token')
    sf_instance = credentials.get('[salesforce][domain]')
    # Connect to Salesforce
    sf = Salesforce(username=sf_username, password=sf_password, security_token=sf_security_token, domain=sf_instance)
    return sf


# Function to generate random strings
def generate_random_string(length):
    return ''.join(random.choice(string.ascii_uppercase) for _ in range(length))


# Function to generate random records
def generate_records():
    records = []
    for i in range(1, 501):
        account_id = str(random.randint(10000, 99999))
        external_id = str(uuid.uuid4())
        alpha_field = generate_random_string(4)
        beta_field = generate_random_string(3)
        records.append([account_id, external_id, alpha_field, beta_field])
        with open('salesforce_records.csv', 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['AccountId', 'ExternalId', 'Alpha', 'Beta'])
            csv_writer.writerows(records)
    return records


# Function to load records to Salesforce custom object
def load_to_salesforce(sf):
    with open('salesforce_records.csv', 'r') as csvfile:
        csv_data = csv.DictReader(csvfile)
        sf.bulk.Salesforce_Object_Name__c.insert(list(csv_data))


# Main script
if __name__ == "__main__":
    sfdc = create_session()
    print('sfdc auth type: '+sfdc.auth_type)
    generate_records()

