import json
import pycurl
from io import BytesIO

api = json.load(open('api.json'))

def make_optiic_request (api_key, filename):
    # Create the curl request object
    buffer = BytesIO()
    c = pycurl.Curl()
    url = api['url']

    c.setopt(c.URL, url)
    c.setopt(c.POST, 1)
    c.setopt(c.POSTFIELDS, 'apiKey=' + api_key)
    c.setopt(c.WRITEDATA, buffer)
    c.setopt(c.HTTPPOST, [("image", (c.FORM_FILE, 'img/' + filename))])
    c.setopt(pycurl.HTTPHEADER, ['Accept-Language: en'])
    c.perform()
    print("POST '" + filename + "' to:", url)
    c.close()

    # Get the response value
    response = buffer.getvalue()
    print(response.decode("utf-8"))
    # Parse the response and get the returned text
    respObj = json.loads(response)
    text = respObj['text']
    print(text)

    return text


# TEST
API_KEY = api['key']
text1 = make_optiic_request(API_KEY, '1.jpg')
text2 = make_optiic_request(API_KEY, '2.jpg')

print(text1, '\n', text2, sep='')