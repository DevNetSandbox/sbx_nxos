#!/usr/bin/env python

from ncclient import manager
import sys
from lxml import etree


# Set the device variables
DEVICE = "sbx-nxos-mgmt.cisco.com"
USER = 'admin'
PASS = 'Admin_1234!'
PORT = 10000

LOOPBACK_IP = "10.99.99.1/24"

# create a main() method
def main():
    """
    Main method that adds an IP address to interface loopback 99 to
    switch.
    """

    loopback_ip_add = """
    <config>
    <System xmlns="http://cisco.com/ns/yang/cisco-nx-os-device">
    <ipv4-items>
        <inst-items>
            <dom-items>
                <Dom-list>
                    <name>default</name>
                    <if-items>
                        <If-list>
                            <id>lo99</id>
                            <addr-items>
                                <Addr-list>
                                    <addr>{}</addr>
                                </Addr-list>
                            </addr-items>
                        </If-list>
                    </if-items>
                </Dom-list>
            </dom-items>
        </inst-items>
    </ipv4-items>
    </System>
    </config>"""


    with manager.connect(host=DEVICE, port=PORT, username=USER,
                         password=PASS, hostkey_verify=False,
                         device_params={'name': 'nexus'},
                         look_for_keys=False, allow_agent=False) as m:

        # Add the loopback interface
        print("\nNow adding IP address {} to device {}...\n".format(LOOPBACK_IP, DEVICE))
        new_ip = loopback_ip_add.format(LOOPBACK_IP)
        netconf_response = m.edit_config(target='running', config=new_ip)
        # Parse the XML response
        print(netconf_response)

if __name__ == '__main__':
    sys.exit(main())
