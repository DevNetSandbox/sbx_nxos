#!/usr/bin/env python

from ncclient import manager
import sys
from lxml import etree


# Set the device variables

DEVICES = ['172.16.30.101', '172.16.30.102']
USER = 'admin'
PASS = 'admin'
PORT = 830
DEVICE_NAMES = {'172.16.30.101': '(nx-osv9000-1)',
                '172.16.30.102': '(nx-osv9000-2)' }

# create a main() method
def main():
    """
    Main method that adds loopback interface 99 to both the spine switches.
    """

    loopback_add = """
    <config>
    <System xmlns="http://cisco.com/ns/yang/cisco-nx-os-device">
    <intf-items>
    <lb-items>
    <LbRtdIf-list>
    <id>lo99</id>
    <adminSt>up</up>
    <descr>Interface added via NETCONF</descr>
    </LbRtdIf-list>
    </lb-items>
    </intf-items>
    </System>
    </config>"""


    for device in DEVICES:
        with manager.connect(host=device, port=PORT, username=USER,
                             password=PASS, hostkey_verify=False,
                             device_params={'name': 'nexus'},
                             look_for_keys=False, allow_agent=False) as m:
            
            # Add the loopback interface 
            print("\nNow adding Loopback99 device {} {}...\n".format(DEVICE_NAMES[device], device))
            netconf_response = m.edit_config(target='running', config=loopback_add)
            # Parse the XML response
            print(netconf_response)

if __name__ == '__main__':
    sys.exit(main())
