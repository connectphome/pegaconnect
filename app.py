#!/usr/bin/env python

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()



from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os
import urllib2

from flask import Flask
from flask import request
from flask import make_response


# Flask app should start in global layout
app = Flask(__name__)

gid = "G123"

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

def basic_authorization(user, password):
	s = user + ":" + password
	return "Basic " + s.encode("base64").rstrip()

def processRequest(req):
	
	if req.get("result").get("action") == "Unpair":
		url = "http://acc-pw17.pegatsdemo.com:8080/prweb/PRHTTPService/HomeAISmartHomeIntGoogleHome/Services/ProcessData"
	
	if req.get("result").get("action") == "CheckPairing":
		url = "http://acc-pw17.pegatsdemo.com:8080/prweb/PRHTTPService/CheckPairing/Services/CheckPairing"
	
	if req.get("result").get("action") == "Escalation":
		url = "http://acc-pw17.pegatsdemo.com:8080/prweb/PRHTTPService/Escalate/Services/Escalate?gid=" + gid + "&command=Escalate"
	
	if req.get("result").get("action") == "GetStep":
		url = "http://acc-pw17.pegatsdemo.com:8080/prweb/PRHTTPService/GetStep/Services/GetStep?gid=" + gid
	
	if req.get("result").get("action") == "StartTroubleshoot":
		url = "http://acc-pw17.pegatsdemo.com:8080/prweb/PRHTTPService/HomeAISmartHomeIntGoogleHome/Services/ProcessData"
	
	if req.get("result").get("action") == "Register":
		result = req.get("result")
   		parameters = result.get("parameters")
		worknumber = parameters.get("number-integer")

		url = "http://acc-pw17.pegatsdemo.com:8080/prweb/PRHTTPService/RegisterHome/Services/RegisterGH?"
		parameter = "worknumber=" + worknumber
		url = url + parameter
		
	params = {}
	req = urllib2.Request(url,  json.dumps(params), headers={"Authorization": basic_authorization('bdonnelly', 'rules'),"Content-Type": "application/json", "Accept": "*/*", })
	result = urllib2.urlopen(req)
	v = result.read()
	data = json.loads(v)
	return makeWebhookResult(data)
	
	

def makeYqlQuery(req):

	return "Google Home"


def makeWebhookResult(data):
	speech = data.get("GHMessage")
	if speech is None:
		speech="Nothing Gotten"

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
