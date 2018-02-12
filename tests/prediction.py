# Install the Python Requests library:
# `pip install requests`

import requests
import json
import io, base64


def testImage():
  TEST_IMG_URL = "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Cat03.jpg/1200px-Cat03.jpg"
  response = requests.get(TEST_IMG_URL)
  img_stream = io.BytesIO(response.content)
  return base64.encodestring(img_stream.read()).decode("utf-8")


try:
    response = requests.post(
        url="https://api.doppler.market/v1/apps/vgg16/models/8/prediction",
        headers={
            "Content-Type": "application/json; charset=utf-8",
            "access-token": "okximez4eaz53cpoikvalfswkrog9qgs4rfbwfp0",
        },
        data=json.dumps({
            "image": testImage()
        })
    )

    print(json.dumps(response.json(), indent=2))
except requests.exceptions.RequestException:
    print('HTTP Request failed')


