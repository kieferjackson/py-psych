import json
import re
import pycurl
import os
from io import BytesIO

IMG_FOLDER_NAME = 'img'
image_filenames = os.listdir('./' + IMG_FOLDER_NAME)

api = json.load(open('api.json'))
API_KEY = api['key']
API_URL = api['url']

def make_optiic_request (filename):
    # Create the curl request object
    buffer = BytesIO()
    c = pycurl.Curl()

    c.setopt(c.URL, API_URL)
    c.setopt(c.POST, 1)
    c.setopt(c.WRITEDATA, buffer)
    c.setopt(c.HTTPPOST, [
        ('apiKey', API_KEY),
        ("image", (c.FORM_FILE, IMG_FOLDER_NAME + '/' + filename))
    ])
    c.setopt(pycurl.HTTPHEADER, ['Accept-Language: en'])
    c.perform()
    print("POST '" + filename + "' to:", API_URL)
    c.close()

    # Get the response value
    response = buffer.getvalue()
    resp = response.decode("utf-8")
    # Parse the response and get the returned text
    respObj = json.loads(resp)
    text = respObj['text']
    print(text)

    return text

# Get index card data and associate based on its collection ID and its face
index_card_data = {}
for filename in image_filenames:
    # Get the collection ID and face from the first numeral and following character
    # NOTE: a = Front ; b = Back
    collection_data = re.findall(r'(\d+|[A-Za-z]+)', filename)
    card_id, card_face, *junk = collection_data
    key_value = 'front' if card_face == 'a' else 'back'

    # POST the file by its filename to Optiic to get the raw text data
    raw_text = make_optiic_request(filename)
    stripped_text = raw_text.replace('\n', ' ')
    text_data = stripped_text.split('%@&')
    print(text_data)

    if index_card_data.get(card_id) == None:
        # Initialize the data property
        index_card_data[card_id] = { 'data': [] }

    for i, text in enumerate(text_data):
        # Check if entry already exists at given index (i), and append empty dict if necessary
        if i >= len(index_card_data[card_id]['data']):
            index_card_data[card_id]['data'].append({})

        index_card_data[card_id]['data'][i][key_value] = text
    
print(index_card_data)