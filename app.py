from flask import Flask
from flask import request as freq
from urllib import request, parse
from base64 import urlsafe_b64encode
import json
import os
import sys
import threading
from flask import copy_current_request_context


sys.path.insert(0, os.path.dirname(__file__))

app = Flask(__name__)

 

@app.route('/')
def application(environ, start_response):
    print(environ)
    name=environ.get('HTTP_CUST_NAME')
    company=environ.get('HTTP_CUST_COMPANY')
    email=environ.get('HTTP_CUST_EMAIL')
    cust_message=environ.get('HTTP_CUST_MESSAGE')
    start_response('200 OK', [('Content-Type', 'text/plain')])
    message = 'It works!\n'
    version = 'Python v' + sys.version.split()[0] + '\n'
    response = '\n'.join([message, version])
    #name = freq.headers.get('name')
    #company = freq.headers.get('company')
    #email = freq.headers.get('email')
    #message = freq.headers.get('message')
    postemail(str(name),str(company),str(email),str(cust_message)) 
    return [response.encode()]

def postemail(name,company,email,message):
    access_token = getAccessToken()
    if len(access_token) > 0:
        print("Access token fetched successfully, Attempting to send email")
        graphSendEmail(name,company,email,message,access_token)
    else:
       print("Failed to receive access token, unable to send email")


def getAccessToken():
    data = {
        "grant_type": "refresh_token",
        "client_id": "fbe37faa-3849-494c-9df7-3404c9d6f72b",
        "client_secret": "MV38Q~IgYO8LODAjd~v9Qq78fxSpeKRaEg5pqapu",
        "refresh_token":"0.AVYAMehG0WjlQUuTwaxtoo3Zp6p_4_tJOExJnfc0BMnW9yufAC0.AgABAAEAAAAmoFfGtYxvRrNriQdPKIZ-AgDs_wUA9P-yWu6vlCzWI1vIqLb8br5Uuci1nOKF4OvNv4S_qurRW2SlK-klTH8WGyx38nhs_eW1uBNYJb_7irfhhdNRsUhBG53Q1lfj1lI32fJoxtUczivWvZ5Qcnp7kru9n6bTfT84tSjv2So9AM_y8FhfPgeY4jxY0DQfLAtV-zXxcZJCN0i74oNIsyA6v4P8j4VCNI8pHLROu-w9VUuVUC2jbpI26LQR8RW6XWbi31fVc4_UOpZDfFwmGxJwBvSGve_eKuzYou0YFaiEtuBxQGz1FEwTvq9HBNLHHHEEKvKVGeHDY_W_YhEwYdl0PaEgo_Y2f4kxvYLvriw6MQtdhEwGM2UntnHmNWRrzwz0WT3zfL6BWLsg-rjrpUYkqQQ7raGtg9JmUZSu05_UiYE1tcKfbRr6ffAYSxx4pWB04pRIzCTQ2nAxfQGDjm1GIixSaMYS9vIVE5VIJ33rFSgRZTiWWib2IC9Pudki_5K8phmBnAFxbTcOGiY-vfFnWK40AnevPfLJVWxYzcFLroWTl9bH87ifKEwhkJwyeUd3RbiRu3zaf3VVifCbezLgJAxkulihxG8u-xdbhls_Bt3ZwgDVb14DNggwU8Vi7lsZZl1-d8vDCP5O4vfJRzqSVPfr1Eu5tzzQDv8OwJcrJ80xPY8PPdJV1sqcoq3m8AQ2TqQEWEuKkXUsnNaYKzwNezPd_lTKSk_hf6t91JxMBiV4ZM-CXrs",
        "redirect)uri":"http://localhost"
        }

    data = parse.urlencode(data).encode("utf-8")
     
    resp = request.Request("https://login.microsoftonline.com/d146e831-e568-4b41-93c1-ac6da28dd9a7/oauth2/v2.0/token", data=data, method="POST")
    with request.urlopen(resp) as response:
        token = json.load(response)
        return token["access_token"]

def graphSendEmail(name,company,email,message,access_token):
    subject = 'Message from '+name+' ,'+company+' '+email
    jsonmessage = {
        "message": {
            "subject": subject,
            "body": {
                "contentType": "Text",
                "content": message,
            },
            "toRecipients": [
                {"emailAddress": {"address": "info@3migostech.com"}}
            ],
            "ccRecipients": [
                {"emailAddress": {"address": "shaik@3migostech.com"}}
            ],
        },
        "saveToSentItems": "true",
    }
    reqheaders = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    message_data = json.dumps(jsonmessage).encode("utf-8")
    emailresp = request.Request("https://graph.microsoft.com/v1.0/me/sendMail", data=message_data, headers=reqheaders, method="POST")
    with request.urlopen(emailresp) as response:
        if response.status == 202:
            print("Email sent successfully.")
        else:
            print(f"Failed to send email. Status code: {response.status}, Response: {response.read().decode('utf-8')}")



if __name__ == '__main__':
   app.run(environ,start_response)