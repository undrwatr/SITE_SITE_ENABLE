#!/usr/bin/python

#imports
import sys
import requests
import json
import os
import subprocess
import cred

#custom variables for the program imported from the cred.py file located in the same directory
organization = cred.organization
key = cred.key
hub = cred.hub


#Main URL for the Meraki Platform
dashboard = "https://dashboard.meraki.com"
#api token and other data that needs to be uploaded in the header
headers = {'X-Cisco-Meraki-API-Key': (key), 'Content-Type': 'application/json'}

#variables for testing ***** Need to switch to an argument or something else
store = sys.argv[1]

#pull back all of the networks for the organization
get_network_url = dashboard + '/api/v0/organizations/%s/networks' % organization

#request the network data
get_network_response = requests.get(get_network_url, headers=headers)
if get_network_response.status_code == 200:
    #puts the data into json format
    get_network_json = get_network_response.json()
    #pull back the network_id of the store that you are configuring
    for i in get_network_json:
        if i["name"] == str(store):
            network_id=(i["id"])
else:
    print("API Rate is to high, try again later")
    sys.exit()

#enable VPN by writing out a curl function to a file and then calling it. This is put in due to an issue with the Meraki site. The better code is below, but this works for right now.
curl_com = open("curl", "w", 0)
#bash_com = "curl -L -H 'X-Cisco-Meraki-API-Key: %s' -X PUT -H 'Content-Type: application/json' --data-binary '{\"mode\":\"spoke\",\"hubs\":[{\"hubId\":\"%s\",\"useDefaultRoute\":true }]}' 'https://dashboard.meraki.com/api/v0/networks/%s/siteToSiteVpn'" % (key, hub, network_id)
bash_com = "curl -L -H 'X-Cisco-Meraki-API-Key: %s' -X PUT -H 'Content-Type: application/json' --data-binary '{\"mode\":\"none\"}' 'https://dashboard.meraki.com/api/v0/networks/%s/siteToSiteVpn'" % (key, network_id)
curl_com.write(bash_com)
curl_com.close()

subprocess.call(["bash ./curl"], shell=True)

#turn on VPN for the store once VLAN Configuration is done**** THIS CODE ISN'T READY YET, DUE TO SOME ISSUE WITH THE BACKEND
#VPNSET = {}
#VPNSET["hubs"] = "{'hubId': '%s', 'useDefaultRoute': 'true'}" % hub
#VPNSET["mode"] = "spoke"
#VPNSET = {"mode":"spoke","hubs":[{"hubId":"%s","useDefaultRoute":"true"}]} % hub


#create the url
#get_network_vpnset = dashboard + '/api/v0/networks/%s/siteToSiteVpn' % network_id

#perform the udpate
#get_network_vpnsetjson = requests.put(get_network_vpnset, data=json.dumps(VPNSET), headers=headers)

#Cleanup after everything is done
#close the sql connection