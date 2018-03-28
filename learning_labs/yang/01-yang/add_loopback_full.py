#!/usr/bin/env python

from ncclient import manager
import sys
from lxml import etree


# Set the device variables
DEVICE = "sbx-nxos-mgmt.cisco.com"
USER = 'admin'
PASS = 'Admin_1234!'
PORT = 10000

LOOPBACK_IP = {'loopback': 'lo101', 'ip': '10.101.1.1/24', 'name': 'Loopback101'}


# create a main() method
def main():
    """
    Main method that adds loopback interfaces and configures an IP address to
    both the spine switches.
    """

    add_ip_interface = """<config>
    <System xmlns="http://cisco.com/ns/yang/cisco-nx-os-device">
    <intf-items>
        <lb-items>
            <LbRtdIf-list>
                <id>{0}</id>
                <adminSt>up</up>
                <descr>Full intf config via NETCONF</descr>
            </LbRtdIf-list>
        </lb-items>
    </intf-items>
    <ipv4-items>
        <inst-items>
            <dom-items>
                <Dom-list>
                    <name>default</name>
                    <if-items>
                        <If-list>
                            <id>{0}</id>
                            <addr-items>
                                <Addr-list>
                                    <addr>{1}</addr>
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
        print("\nNow adding IP address {} to intf {} on device {}...\n".format(
                        LOOPBACK_IP['ip'],
                        LOOPBACK_IP['name'],
                        DEVICE)
                        )

        new_ip = add_ip_interface.format(
                LOOPBACK_IP['loopback'],
                LOOPBACK_IP['ip']
            )

        netconf_response = m.edit_config(target='running', config=new_ip)
        # Parse the XML response
        print(netconf_response)


if __name__ == '__main__':
    sys.exit(main())
