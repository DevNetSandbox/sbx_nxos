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
    '172.16.30.101': {'loopback': 'lo101', 'ip': '10.101.1.1/24', 'name': 'Loopback101'},
    '172.16.30.102': {'loopback': 'lo102', 'ip': '10.102.1.2/24', 'name': 'Loopback102'}
}
DEVICE_NAMES = {'172.16.30.101': '(nx-osv9000-1)',
                '172.16.30.102': '(nx-osv9000-2)' }
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


    for device in DEVICES:
        with manager.connect(host=device, port=PORT, username=USER,
                             password=PASS, hostkey_verify=False,
                             device_params={'name': 'nexus'},
                             look_for_keys=False, allow_agent=False) as m:

            # Add the loopback interface
            print("\nNow adding IP address {} to intf {} on device {} {}...\n".  format(LOOPBACK_IP[device]['ip'],
                              LOOPBACK_IP[device]['name'], DEVICE_NAMES[device],
                              device))

            new_ip = add_ip_interface.format(LOOPBACK_IP[device]['loopback'], LOOPBACK_IP[device]['ip'])
            netconf_response = m.edit_config(target='running', config=new_ip)
            # Parse the XML response
            print(netconf_response)


if __name__ == '__main__':
    sys.exit(main())
