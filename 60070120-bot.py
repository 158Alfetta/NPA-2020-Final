import json
import requests
from prettyprinter import pprint
requests.packages.urllib3.disable_warnings()

ACCESS_TOKEN = "OWUzMDQ2ZGItNzBmYS00YWI3LWFmYjMtOGUyNjEyODY3MWM1YWFkNDZlNGUtN2Yw_PF84_consumer"
ROOM_ID = "Y2lzY29zcGFyazovL3VzL1JPT00vNjA5Nzk5NDAtNTU3My0xMWViLWEzNzUtY2JkMGE4ZjAxYTA3"

def getData():

    api_url = "https://10.0.15.104/restconf/data/ietf-interfaces:interfaces-state"
    headers = { "Accept": "application/yang-data+json",
    "Content-type":"application/yang-data+json"
    }
    basicauth = ("admin", "cisco")

    resp = requests.get(api_url, auth=basicauth, headers=headers, verify=False)
    response_json = resp.json() 
    # this output is already dictionary
    interface = response_json['ietf-interfaces:interfaces-state']['interface']
    
    lb_data = ""

    for interface in response_json['ietf-interfaces:interfaces-state']['interface']:
        if interface['name'] == "Loopback60070120":
            lb_data = interface['name'] + "- Operational Status is "+interface['oper-status']
            pprint(lb_data)
    return lb_data

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
    

def retrieveMsg():
    webex_url = "https://webexapis.com/v1/messages"
    webex_auth = {"Content-Type":"application/json", "Authorization":"Bearer {}".format(ACCESS_TOKEN)}
    webex_param = {"roomId":ROOM_ID, 'max':1}
    webex_response = requests.get(url=webex_url, headers=webex_auth, params=webex_param).json()
    return webex_response['items'][0]['text']

def senderMsg(text):
    webex_url = "https://webexapis.com/v1/messages"
    webex_auth = {"Content-Type":"application/json", "Authorization":"Bearer {}".format(ACCESS_TOKEN)}
    webex_param = {"roomId":ROOM_ID, 'text':text}
    webex_response = requests.post(url=webex_url, headers=webex_auth, json=webex_param).json()
    print(webex_response)

def main():
    while 1:
        msg = retrieveMsg()
        print(msg)
        if msg == "60070120":
            lb_data = getData()
            senderMsg(lb_data)
main()