#!/usr/bin/env python

from ncclient import manager
import sys
from lxml import etree


# Set the device variables

DEVICE = '172.16.30.101'
USER = 'admin'
PASS = 'admin'
PORT = 830



# create a main() method
def main():
    """
    Main method that updates the hostname of the remote device.
    """
    new_name = """
    <config>
    <System xmlns="http://cisco.com/ns/yang/cisco-nx-os-device">
    <name>nxos-spine1</name>
    </System>
    </config>
    """
    
    with manager.connect(host=DEVICE, port=PORT, username=USER,
                         password=PASS, hostkey_verify=False,
                         device_params={'name': 'nexus'},
                         look_for_keys=False, allow_agent=False) as m:
        
        # Update the running config
        netconf_response = m.edit_config(target='running', config=new_name)
        # Parse the XML response
        print(netconf_response)

                

if __name__ == '__main__':
    sys.exit(main())
