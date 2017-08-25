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
    Main method that collects the ASN from the spine switches using the native model
    """

    asn_filter = """
    <System xmlns="http://cisco.com/ns/yang/cisco-nx-os-device">
    <bgp-items>
    <inst-items>
    <asn/>
    </inst-items>
    </bgp-items>
    </System>
    """
   

    for device in DEVICES:
        with manager.connect(host=device, port=PORT, username=USER,
                             password=PASS, hostkey_verify=False,
                             device_params={'name': 'nexus'},
                             look_for_keys=False, allow_agent=False) as m:
            
            # Add the loopback interface 
            netconf_response = m.get(('subtree', asn_filter))
            # Parse the XML response
            xml_data = netconf_response.data_ele
            asn = xml_data.find(".//{http://cisco.com/ns/yang/cisco-nx-os-device}asn").text

            print("The ASN number for {} {} is {}".format(DEVICE_NAMES[device], device, asn))


if __name__ == '__main__':
    sys.exit(main())
