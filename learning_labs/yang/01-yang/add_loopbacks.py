#!/usr/bin/env python

from ncclient import manager
import sys
from lxml import etree


# Set the device variables
DEVICE = "sbx-nxos-mgmt.cisco.com"
USER = 'admin'
PASS = 'Admin_1234!'
PORT = 10000

# create a main() method
def main():
    """
    Main method that adds loopback interface 99 to both the switch.
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


    with manager.connect(host=DEVICE, port=PORT, username=USER,
                         password=PASS, hostkey_verify=False,
                         device_params={'name': 'nexus'},
                         look_for_keys=False, allow_agent=False) as m:

        # Add the loopback interface
        print("\nNow adding Loopback99 device {}...\n".format(DEVICE))
        netconf_response = m.edit_config(target='running', config=loopback_add)
        # Parse the XML response
        print(netconf_response)

if __name__ == '__main__':
    sys.exit(main())
