import json
import os
import requests

class ESQuery:
    def __init__(self, event, url):
        self.chatfuel_req = json.loads(event['body'])
        self.search_json = {
            "size": int(os.environ['SEARCH_SIZE']),
            "sort": {
                "scrape_start_time": {
                    "order": "desc"
                }
            },
            "query": {
            }
        }

        self.url = url
        self.headers = { "Content-Type": "application/json" }
    
    def build_query(self):
        self.search_json['query']['match'] = {
            'title': self.chatfuel_req['title'].lower()
        }

    def send_to_es(self):
        response = requests.get(self.url, json=self.search_json, headers=self.headers)
        print(self.url)
        print(self.search_json)
        if response.status_code != 200:
            print("ES response error, ", response.text)
            raise Exception("ES response error")

        return response.text