#!/usr/bin/env python

from ncclient import manager
import sys
from lxml import etree


# Set the device variables

DEVICES = ['172.16.30.101', '172.16.30.102']
USER = 'admin'
PASS = 'admin'
PORT = 830
LOOPBACK_IP = {
    '172.16.30.101': '10.99.99.1/24',
    '172.16.30.102': '10.99.99.2/24'
}
DEVICE_NAMES = {'172.16.30.101': '(nx-osv9000-1)',
                '172.16.30.102': '(nx-osv9000-2)' }
# create a main() method
def main():
    """
    Main method that adds an IP address to interface loopback 99 to
    both the spine switches.
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


    for device in DEVICES:
        with manager.connect(host=device, port=PORT, username=USER,
                             password=PASS, hostkey_verify=False,
                             device_params={'name': 'nexus'},
                             look_for_keys=False, allow_agent=False) as m:
            
            # Add the loopback interface 
            print("\nNow adding IP address {} to device {} {}...\n".format(LOOPBACK_IP[device], DEVICE_NAMES[device],
                            device))
            new_ip = loopback_ip_add.format(LOOPBACK_IP[device])
            netconf_response = m.edit_config(target='running', config=new_ip)
            # Parse the XML response
            print(netconf_response)

if __name__ == '__main__':
    sys.exit(main())
