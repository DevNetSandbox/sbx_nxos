#!/usr/bin/env python

'''
This script stops, and then starts all the nodes in the 
sandbox using the VIRL APIs.  
'''

from time import sleep
from virlutils import *

if __name__ == "__main__": 
    
    # Get simulation list
    nx_os_simulation = get_simulations()
    nx_os_simulation_name = nx_os_simulation.keys()[0]
    
    print("VIRL Simulation Name: {}\n".format(nx_os_simulation_name))
    
    # Get Simulation Node List     
    nodes = get_nodes(nx_os_simulation_name)
    for node in nodes.keys():
        print("{}: Status {}".format(node, nodes[node]["state"]))
    print(" ")
        
    # Stop Nodes
    print("Stopping Nodes")
    action = stop_nodes(nx_os_simulation_name, nodes)
    print(action["stopped"])
    print("")
    
    # Wait for nodes to be fully stopped (state = ABSENT)
    while not test_node_state(nx_os_simulation_name, "ABSENT"):
        print("Nodes note stopped yet")
        sleep(10)
    
    # Start Nodes
    print("Starting Nodes")
    action = start_nodes(nx_os_simulation_name, nodes)
    print(action["started"])
    print("")
    
    # Wait for nodes to be fully started (state = ACTIVE)
    while not test_node_state(nx_os_simulation_name, "ACTIVE"):
        print("Nodes note started yet")
        sleep(10)
    
    # Done
    print("Nodes have been restarted, however it can take up to 15 minutes for all switches to fully boot and be ready.")
    
    