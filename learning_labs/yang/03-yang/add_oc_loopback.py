#!/usr/bin/env python

from ncclient import manager
import sys
from lxml import etree


# Set the device variables

DEVICES = ['172.16.30.103', '172.16.30.104']
USER = 'admin'
PASS = 'admin'
PORT = 830
IP_INT = {'172.16.30.103': {'loopback': 'lo103', 'ip': '10.103.1.1', 'name': 'Loopback103'},
          '172.16.30.104': {'loopback': 'lo104', 'ip': '10.104.1.1', 'name': 'Loopback104'}}
DEVICE_NAMES = {'172.16.30.103': '(nx-osv9000-3)',
                '172.16.30.104': '(nx-osv9000-4)'}

# create a main() method
def main():
    """
    Main method that adds loopback interfaces to the leaf nodes using the OC model
    """

    add_oc_interface = """<config>
<interfaces xmlns="http://openconfig.net/yang/interfaces">
    <interface>
        <name>{0}</name>
        <config>
            <description> Configured using OpenConfig Model </description>
            <name>{0}</name>
            <type>ianaift:softwareLoopback</type>
        </config>
        <subinterfaces>
            <subinterface>
                <index>0</index>
                <ipv4>
                    <addresses>
                        <address>
                            <config>
                                <ip>{1}</ip>
                                <prefix-length>24</prefix-length>
                            </config>
                            <ip>{1}</ip>
                        </address>
                    </addresses>
                </ipv4>
            </subinterface>
        </subinterfaces>
    </interface>
</interfaces>
</config>"""


    for device in DEVICES:
        with manager.connect(host=device, port=PORT, username=USER,
                             password=PASS, hostkey_verify=False,
                             device_params={'name': 'nexus'},
                             look_for_keys=False, allow_agent=False) as m:

            # Add the loopback interface IP
            print("\nNow adding IP address {} to interface {} on device {} {}...\n".format(IP_INT[device]['ip'],
                                                                                           IP_INT[device]['name'], DEVICE_NAMES[device], device))
            
            
            new_intf = add_oc_interface.format(IP_INT[device]['loopback'], IP_INT[device]['ip'])
            netconf_response = m.edit_config(target='running', config=new_intf)
            # Parse the XML response
            print(netconf_response)

if __name__ == '__main__':
    sys.exit(main())
