#!/usr/bin/env python

from ncclient import manager
import sys


# Set the device variables
DEVICE = "sbx-nxos-mgmt.cisco.com"
USER = 'admin'
PASS = 'Admin_1234!'
PORT = 10000

# create a main() method
def main():
    """
    Main method that prints netconf capabilities of remote device.
    """
    with manager.connect(host=DEVICE, port=PORT, username=USER,
                         password=PASS, hostkey_verify=False,
                         device_params={'name': 'nexus'},
                         look_for_keys=False, allow_agent=False) as m:

        # print all NETCONF capabilities
        print('\n***Remote Devices Capabilities for device {}***\n'.format(DEVICE))
        for capability in m.server_capabilities:
            print(capability.split('?')[0])


if __name__ == '__main__':
    sys.exit(main())
