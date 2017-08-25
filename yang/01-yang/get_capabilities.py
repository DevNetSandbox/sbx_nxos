#!/usr/bin/env python

from ncclient import manager
import sys


# Set the device variables

DEVICES = ['172.16.30.101', '172.16.30.102']
USER = 'admin'
PASS = 'admin'
PORT = 830
DEVICE_NAMES = {'172.16.30.101': '(nx-osv9000-1)',
                '172.16.30.102': '(nx-osv9000-2)' }


# create a main() method
def main():
    """
    Main method that prints netconf capabilities of remote device.
    """
    for device in DEVICES:
        with manager.connect(host=device, port=PORT, username=USER,
                             password=PASS, hostkey_verify=False,
                             device_params={'name': 'nexus'},
                             look_for_keys=False, allow_agent=False) as m:

            # print all NETCONF capabilities
            print('\n***Remote Devices Capabilities for device {} {}***\n'.format(DEVICE_NAMES[device], device))
            for capability in m.server_capabilities:
                print(capability.split('?')[0])
                

if __name__ == '__main__':
    sys.exit(main())
