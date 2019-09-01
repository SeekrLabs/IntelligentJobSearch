import json

class MessengerGalleryResponse:
    def __init__(self, input_es_response):
        self.input_es_response = json.loads(input_es_response)
        self.api_response = {
            "messages": [
                {
                    "attachment": {
                        "type": "template",
                        "payload": {
                            "template_type": "generic",
                            "image_aspect_ratio": "square",
                            "elements": [

                            ]
                        }
                    }
                }
            ]
        }

    def process(self):
        items = self.input_es_response['hits']['hits']
        for item in items:
            item = item['_source']
            mg = MessengerGalleryCard(
                title=item['title'], 
                subtitle=item['company'],
                image_url='https://herschel.ca/content/dam/herschel/swatches/1063.png'
            )

            mg.add_button(
                url=item['url'],
                title='Apply Now'
            )

            self.api_response['messages'][0]['attachment']['payload']['elements']\
                .append(mg.card_json)
        return self.api_response

class MessengerGalleryCard:
    def __init__(self, title, subtitle, image_url):
        self.card_json = {
            'title': title,
            'image_url': image_url,
            'subtitle': subtitle,
            'buttons': []
        }

    def add_button(self, url, title):
        self.card_json['buttons'].append(
            {
                'type': 'web_url',
                'url': url,
                'title': title
            }
        )