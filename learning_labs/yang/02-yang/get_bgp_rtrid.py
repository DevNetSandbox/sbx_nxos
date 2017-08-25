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
                '172.16.30.102': '(nx-osv9000-2)'}

# create a main() method
def main():
    """
    Main method that collects the BGP router-id from the spine switches using the native model
    """
    bgp_rtrid_filter = """
<System xmlns="http://cisco.com/ns/yang/cisco-nx-os-device">
    <bgp-items>
        <inst-items>
            <dom-items>
                <Dom-list>
                    <rtrId/>
                </Dom-list>
            </dom-items>
        </inst-items>
    </bgp-items>
</System>"""

      

    for device in DEVICES:
        with manager.connect(host=device, port=PORT, username=USER,
                             password=PASS, hostkey_verify=False,
                             device_params={'name': 'nexus'},
                             look_for_keys=False, allow_agent=False) as m:
            
            # Add the loopback interface 
            netconf_response = m.get(('subtree', bgp_rtrid_filter))
            # Parse the XML response
            xml_data = netconf_response.data_ele
            rtrid = xml_data.find(".//{http://cisco.com/ns/yang/cisco-nx-os-device}rtrId").text


            print("The BGP router-id for {} {} is {}".format(DEVICE_NAMES[device], device, rtrid))


if __name__ == '__main__':
    sys.exit(main())
