#!/usr/bin/env python

from ncclient import manager
import sys
from lxml import etree


# Set the device variables

DEVICES = ['172.16.30.101', '172.16.30.102']
USER = 'admin'
PASS = 'admin'
PORT = 830
PREFIX = {'172.16.30.101': '10.101.1.0/24',
          '172.16.30.102': '10.102.1.0/24' }

DEVICE_NAMES = {'172.16.30.101': '(nx-osv9000-1)',
                '172.16.30.102': '(nx-osv9000-2)'}
# create a main() method
def main():
    """
    Main method that collects the BGP router-id from the spine switches using the native model
    """
    add_prefix = """ <config>
<System xmlns="http://cisco.com/ns/yang/cisco-nx-os-device">
    <bgp-items>
        <inst-items>
            <dom-items>
                <Dom-list>
                    <name>default</name>
                    <af-items>
                        <DomAf-list>
                            <type>ipv4-ucast</type>
                            <prefix-items>
                                <AdvPrefix-list>
                                    <addr>{}</addr>
                                </AdvPrefix-list>
                            </prefix-items>
                        </DomAf-list>
                    </af-items>
                </Dom-list>
            </dom-items>
        </inst-items>
    </bgp-items>
</System>
</config>"""
      

    for device in DEVICES:
        with manager.connect(host=device, port=PORT, username=USER,
                             password=PASS, hostkey_verify=False,
                             device_params={'name': 'nexus'},
                             look_for_keys=False, allow_agent=False) as m:
            
            # Add the prefix to BGP
            print("\nNow adding prefix {} to device {} {}..\n".format(PREFIX[device], DEVICE_NAMES[device], device))
            new_prefix = add_prefix.format(PREFIX[device])
            netconf_response = m.edit_config(target='running', config=new_prefix)
            # Parse the XML response
            print(netconf_response)

if __name__ == '__main__':
    sys.exit(main())
