from concurrent.futures import thread
from copyreg import constructor
from crypt import methods
import json
from flask import Flask, render_template, request
from urllib.parse import urlparse
from urllib.parse import parse_qs
import requests


app = Flask(__name__)


@app.route('/submit', methods=["POST"])
def submitSkipRequest():
    try:
        json_data = json.loads(request.data)
        name = json_data['name']
        url = json_data['link']
        gender = json_data['gender']
        scores = int(json_data["scores"])

        parsed_url = urlparse(url)
        code = parse_qs(parsed_url.query)['id'][0]

        if code == "" or code == "id":
            raise Exception("Id not found")

        final_link = 'https://api.youtest.me/gateApi/players/'+code
        final_gender = 1 if gender == "male" else 2

        payload = {
            "playerGender" : final_gender,
            "playerName" : name,
            "scores" : scores
        }

        r = requests.post(final_link, json=payload)
        if r.status_code == 200:
            res = r.json()
            playerID = res["playerID"]
            return json.dumps({
                "success": True,
                "playerID": playerID
                })

        raise Exception("Error while submitting request")
        
    except Exception as e:
        print(e)
        return json.dumps({
            "success" : False,
            "error": "Failed to skip challenge. Retry again."
            })

@app.route('/')
def index():
    return render_template('index.html')