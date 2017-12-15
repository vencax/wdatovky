import requests # NOTE: Nainstalujem http clienta: pip install requests
import base64
import os

if __name__ == '__main__':
    # create payload JSON. Anyhow. I use environment vars.
    payload = {
        'uname': os.environ['USERNAME'],
        'pwd': os.environ['PASSWORD'],
        'subj': os.environ['SUBJECT'],
        'recpt': os.environ['RECIPIENT'],
        'text': os.environ['MESSAGE']
    }
    # create attachements
    attachments = []
    for f in os.environ['FILES'].split(','):
        with open(f) as o:
            attachments.append({
                'filename': os.path.basename(f),
                'content': base64.standard_b64encode(o.read())
            })
    payload['attach'] = attachments
    # send the actual request
    r = requests.post('http://localhost:5000/api', json=payload)
    print r
