#!/usr/bin/env python

'''
Basic wrappers for the VIRL API
'''

import requests 

simengine_host = "http://10.10.10.160:19399"
virl_user = "guest"
virl_password = "guest" 


def get_simulations(): 
    u = simengine_host + "/simengine/rest/list"
    r = requests.get(u, auth=(virl_user, virl_password))
    return r.json()["simulations"]

def get_nodes(simulation): 
    u = simengine_host + "/simengine/rest/nodes/{}".format(simulation)
    r = requests.get(u, auth=(virl_user, virl_password))
    return r.json()[simulation]

def stop_nodes(simulation, nodes): 
    u = simengine_host + "/simengine/rest/update/{}/stop?".format(simulation)
    node_list = []
    for node in nodes.keys():
        node_list.append("nodes={}".format(node))
    node_list = "&".join(node_list)
    u += node_list
    r = requests.put(u, auth=(virl_user, virl_password))
    return r.json()

def start_nodes(simulation, nodes): 
    u = simengine_host + "/simengine/rest/update/{}/start?".format(simulation)
    node_list = []
    for node in nodes.keys():
        node_list.append("nodes={}".format(node))
    node_list = "&".join(node_list)
    u += node_list
    r = requests.put(u, auth=(virl_user, virl_password))
    return r.json()

def test_node_state(simulation, target_state):
    nodes = get_nodes(simulation)
    for node in nodes.keys(): 
        if not nodes[node]["state"] == target_state:
            return False
    return True
    