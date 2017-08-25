#!/usr/bin/env python

from ncclient import manager
import sys
from lxml import etree


# Set the device variables

DEVICES = ['172.16.30.103', '172.16.30.104']
USER = 'admin'
PASS = 'admin'
PORT = 830
DEVICE_NAMES = {'172.16.30.103': '(nx-osv9000-3)',
                '172.16.30.104': '(nx-osv9000-4)'}

# create a main() method
def main():
    """
    Main method that collects the ASN from the spine switches using the OpenConfig model
    """
    get_oc_bgp = """
<bgp xmlns="http://openconfig.net/yang/bgp">
    <global>
        <state/>
    </global>
</bgp>
"""   

    for device in DEVICES:
        with manager.connect(host=device, port=PORT, username=USER,
                             password=PASS, hostkey_verify=False,
                             device_params={'name': 'nexus'},
                             look_for_keys=False, allow_agent=False) as m:
            
            # Add the loopback interface 
            netconf_response = m.get(('subtree', get_oc_bgp))
            # Parse the XML response
            xml_data = netconf_response.data_ele
            asn = xml_data.find(".//{http://openconfig.net/yang/bgp}as").text

            router_id = xml_data.find(".//{http://openconfig.net/yang/bgp}router-id").text

            print("ASN number:{}, Router ID: {} for {} {}".format(asn, router_id, DEVICE_NAMES[device], device))


if __name__ == '__main__':
    sys.exit(main())
