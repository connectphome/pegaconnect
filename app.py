#!/usr/bin/env python

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
	if req.get("result").get("action") == "GoogleHome":
		device = req.get("result").get("parameters").get("device")
		baseurl = "http://acc-pw17.pegatsdemo.com:8080/prweb/PRHTTPService/HomeAISmartHomeIntAPIAI2/Services/ProcessData?"
		yql_query = makeYqlQuery(req)
		if yql_query is None:
			return {}
		yql_url = baseurl + urlencode({'type=device'}) + "&format=json"
		result = urlopen(yql_url).read()
		data = json.loads(result)
		speech = data
		#res = makeWebhookResult(data)
		return {
			"speech": data,
			"displayText": data,
			# "data": data,
			# "contextOut": [],
			"source": "apiai-weather-webhook-sample"
		}
		
		
	elif req.get("result").get("action") == "yahooWeatherForecast":
		baseurl = "http://acc-pw17.pegatsdemo.com:8080/prweb/PRHTTPService/HomeAISmartHomeIntAPIAI2/Services/ProcessData?"
		yql_query = makeYqlQuery(req)
		if yql_query is None:
			return {}
		yql_url = baseurl + urlencode({'q': yql_query}) + "&format=json"
		result = urlopen(yql_url).read()
		data = json.loads(result)
		res = makeWebhookResult(data)
	elif req.get("result").get("action") == "Repeat":
		speech = device
		return {
			"speech": speech,
			"displayText": speech,
			# "data": data,
			# "contextOut": [],
			"source": "apiai-weather-webhook-sample"
		}
	else:
		return {}
	return res

	
def makeYqlQuery(req):
    result = req.get("result")
    parameters = result.get("parameters")
    city = parameters.get("geo-city")
    if city is None:
        return None

    return "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='" + city + "')"


def makeWebhookResult(data):
    query = data.get('query')
    if query is None:
        return {}

    result = query.get('results')
    if result is None:
        return {}

    channel = result.get('channel')
    if channel is None:
        return {}

    type = channel.get('type')
    

    # print(json.dumps(item, indent=4))

    speech = "Today in " + location.get('city') + ": " + condition.get('text') + \
             ", the temperature is " + condition.get('temp') + " " + units.get('temperature')

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }



if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
