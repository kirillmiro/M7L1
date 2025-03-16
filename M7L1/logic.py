import json
import time
import requests
import base64
from io import BytesIO
from PIL import Image


class Text2ImageAPI:

    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    def get_model(self):
        response = requests.get(self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS)
        data = response.json()
        return data[0]['id']

    def generate(self, prompt, model, images=1, width=1024, height=1024):
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {
                "query": f"{prompt}"
            }
        }

        data = {
            'model_id': (None, model),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post(self.URL + 'key/api/v1/text2image/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        return data['uuid']

    def check_generation(self, request_id, attempts=10, delay=10):
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/text2image/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            if data['status'] == 'DONE':
                return data['images']

            attempts -= 1
            time.sleep(delay)


def decode_base64_to_image(text, output_image):
    image_data = base64.b64decode(text)
    image = Image.open(BytesIO(image_data))
    image.save(output_image)
    print(f"Изображение сохранено как {output_image}")


if __name__ == '__main__':
    api = Text2ImageAPI('https://api-key.fusionbrain.ai/', '366F4895CF525A89E36BB9F70548E94E', '9A1048EB69D405C7CB51AA2CAB0A591D')
    model_id = api.get_model()
    uuid = api.generate("Cфотографированный кот, сидит на крыльце в пасмурную погоду, а рядом стоит ваза с цветами.", model_id)
    images = api.check_generation(uuid)
    with open('text.txt', 'w', encoding = 'utf-8') as f:
        f.write(images[0])
    print(images)
