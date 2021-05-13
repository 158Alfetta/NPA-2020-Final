import json
import requests
import time
from prettyprinter import pprint
requests.packages.urllib3.disable_warnings()

#define a token, both room and access token
ACCESS_TOKEN = ""
ROOM_ID = ""

#use get method on RESTCONF protocol to retrive data from interfaces-state container of ietf-interfaces
def getData():
    api_url = "https://10.0.15.104/restconf/data/ietf-interfaces:interfaces-state"
    headers = { "Accept": "application/yang-data+json",
    "Content-type":"application/yang-data+json"
    }
    basicauth = ("admin", "cisco")

    #start a request
    resp = requests.get(api_url, auth=basicauth, headers=headers, verify=False)
    response_json = resp.json() 
    # this output is already dictionary
    interface = response_json['ietf-interfaces:interfaces-state']['interface']
    
    #define an empty string to make a retun statement
    lb_data = ""

    for interface in response_json['ietf-interfaces:interfaces-state']['interface']:
        if interface['name'] == "Loopback60070120":
            lb_data = interface['name'] + "- Operational Status is "+interface['oper-status']
            pprint(lb_data)
    return lb_data

# this is a function to get every room detail, using for get room ID
def getRoomID():
    url = 'https://webexapis.com/v1/rooms'
    headers = {
    'Authorization': 'Bearer {}'.format(ACCESS_TOKEN),
    'Content-Type': 'application/json'
    }
    params={'max': '100'}
    res = requests.get(url, headers=headers, params=params)
    print(res.json())
# getRoomID()
    
#retrieve message of current room (a room that already define ROOM_ID)
def retrieveMsg():
    webex_url = "https://webexapis.com/v1/messages"
    webex_auth = {"Content-Type":"application/json", "Authorization":"Bearer {}".format(ACCESS_TOKEN)}
    webex_param = {"roomId":ROOM_ID, 'max':1}
    webex_response = requests.get(url=webex_url, headers=webex_auth, params=webex_param).json()
    return webex_response['items'][0]['text']

#send message to current room (a room that already define ROOM_ID)
def senderMsg(text):
    webex_url = "https://webexapis.com/v1/messages"
    webex_auth = {"Content-Type":"application/json", "Authorization":"Bearer {}".format(ACCESS_TOKEN)}
    webex_param = {"roomId":ROOM_ID, 'text':text}
    webex_response = requests.post(url=webex_url, headers=webex_auth, json=webex_param).json()
    print(webex_response)

#Operation are here.
def main():
    while 1:
        time.sleep(1)
        msg = retrieveMsg()
        print(msg)
        if msg == "60070120":
            lb_data = getData()
            senderMsg(lb_data)
main()
