import requests
import json
import pandas
from license import user_key
import csv
import time
def nerdgraph_nrql(key):
  # GraphQL query to NerdGraph
  query = """
  { 
    actor { account(id: 1612388) 
      { nrql
      (query: "FROM NrAiIncident SELECT policyName, conditionName, entity.name, entity.type as 'ServiceName', priority, durationSeconds / 60 AS 'minutes', title, incidentLink SINCE 1 DAY AGO WHERE event = 'close' LIMIT 250") 
      { results } } } 
  }"""
  
  # NerdGraph endpoint
  endpoint = "https://api.newrelic.com/graphql"
  headers = {'API-Key': f'{key}'}
  response = requests.post(endpoint, headers=headers, json={"query": query})

  if response.status_code == 200:
   
    # convert a JSON into an equivalent python dictionary
     dict = json.loads(response.content)
     results = dict["data"]["actor"]["account"]["nrql"]["results"]
     with open('data.json', 'w') as f:
      json.dump(results, f)
     myFile = open('/app/kishannrql.csv', 'w')
     writer = csv.DictWriter(myFile, fieldnames=['ServiceName', 'conditionName', 'entity.name','incidentLink','minutes','policyName','priority','timestamp','title'])
     writer.writeheader()
     writer.writerows(results)
     myFile.close()

    # optional - serialize object as a JSON formatted stream
     json_response = json.dumps(response.json(), indent=2)
     print(json_response)
    
    

  else:
      # raise an exepction with a HTTP response code, if there is an error
      raise Exception(f'Nerdgraph query failed with a {response.status_code}.')

nerdgraph_nrql(user_key)

# Code to Create Google Sheet
