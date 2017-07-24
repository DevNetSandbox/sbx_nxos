#!/bin/env python
#md5sum="309cc767dce45cae304f1f48884adffc"
"""
If any changes are made to this script, please run the below command
in bash shell to update the above md5sum. This is used for integrity check.
f=poap_nexus_script.py ; cat $f | sed '/^#md5sum/d' > $f.md5 ; sed -i \
"s/^#md5sum=.*/#md5sum=\"$(md5sum $f.md5 | sed 's/ .*//')\"/" $f
"""

import urllib2
import urllib
import json
import syslog
import sys
import signal
from time import gmtime, strftime
import re
import glob
# Libraries to allow cli commands from python
try:
    from cisco import cli
    from cisco import transfer
    legacy = True
except ImportError:
    from cli import *
    legacy = False

##
# USER INPUT SECTION - DEFINE POAP SERVER IP
#

options = {
    "poap_server": "172.16.30.1",
    "port": "5000"
}

##
# GLOBAL
##

INSTALL_INFO = {}

##
# HELPER FUNCTIONS
##

def setup_logging():
    """
    Configures the log file this script uses
    """
    global log_hdl
    poap_script_log = "/bootflash/%s_poap.log" % (strftime("%Y%m%d%H%M%S", gmtime()))
    log_hdl = open(poap_script_log, "w+")
    poap_log("Logfile name: %s" % poap_script_log)
    poap_cleanup_script_logs()

    
def poap_log(info):
    """
    Log the trace into console and poap_script log file in bootflash
    Args:
        file_hdl: poap_script log bootflash file handle
        info: The information that needs to be logged.
    """
    global log_hdl
    # Don't syslog passwords
    parts = re.split("\s+", info.strip())
    for (index, part) in enumerate(parts):
        # blank out the password after the password keyword (terminal password *****, etc.)
        if part == "password" and len(parts) >= index+2:
            parts[index+1] = "<removed>"
    # Recombine for syslogging
    info = " ".join(parts)
    # We could potentially get a traceback (and trigger this) before
    # we have called init_globals. Make sure we can still log successfully
    try:
        info = "%s" % (info)
    except NameError:
        info = " - %s" % info
    syslog.syslog(9, info)
    if "log_hdl" in globals() and log_hdl is not None:
        log_hdl.write("\n")
        log_hdl.write(info)
        log_hdl.flush()

        
def poap_cleanup_script_logs():
    """
    Deletes all the POAP log files in bootflash leaving
    recent 4 files.
    """
    file_list = sorted(glob.glob(os.path.join("/bootflash", '*poap.log')), reverse=True)
    poap_log("Found %d POAP script logs" % len(file_list))
    logs_for_removal = file_list[4:]
    for old_log in logs_for_removal:
        remove_file(old_log)

        
def remove_file(filename):
    """
    Removes a file if it exists and it's not a directory.
    """
    if os.path.isfile(filename):
        try:
            os.remove(filename)
        except (IOError, OSError) as e:
            poap_log("Failed to remove %s: %s" % (filename, str(e)))

def abort(msg=None):
    """
    Aborts the POAP script execution with an optional message.
    """
    global log_hdl

    if msg is not None:
        poap_log(msg)

    # Remove config _file(<path to config file>)
    s_no = cli('show inventory chassis | grep SN:').rstrip().split(" ")[-1]
    remove_file(os.path.join("/bootflash", s_no + ".cfg" ))
    # Close the log file
    if log_hdl is not None: 
        log_hdl.close()
    exit(1)            

def sigterm_handler(signum, stack):
    """
    A signal handler for the SIGTERM signal. Cleans up and exits
    """
    abort("INFO: SIGTERM Handler")


## END HELPER FUNCTIONS

def poap_collect():
    """This function register back to the  poap server, the switch mac and
    serial number  which is  then used to  render the  device specific
    config file, as defined in the podvars.yml file. It returns the IP
    address of the tftp server, name  of the config file, protocol the
    server is  listening on(to download  the configuration) and the
    system/kickstart image needed to be installed on this device
    """
    global options
    poap_log("Collecting system S.No and MAC...")
    # Collect the mac address of the mgmt interface
    mgmt = cli('show interface mgmt0').strip()
    match = re.search(r'.+address:\s+(\S{4}\.\S{4}\.\S{4})', mgmt)
    mac = match.group(1)
    poap_log("System MAC address is: {}".format(mac))
    # Collect the device serial number
    s_no = cli('show inventory chassis | grep SN:').rstrip().split(" ")[-1]
    poap_log("System Serial NO is: {}".format(s_no))

    # Send the mac and serial number to the flask server over http
    poap_log("Sending API request to the POAP server {}:{}".format(options['poap_server'], options['port']))
    url = 'http://' + options['poap_server'] + ":" + options['port'] + '/' + s_no
    poap_log("Requesting {}...".format(url))
    data = dict(data=mac)
    opener = urllib2.build_opener(urllib2.HTTPHandler)
    req = urllib2.Request(url, data=urllib.urlencode(data))
    req.get_method = lambda: 'PUT'
    # In [61]: print resp.read()
    # {
    #     "config_file": "xxxx.cfg", 
    #     "system_image": "nxos_v6", 
    #     "tftp_server": "172.16.30.1",
    #     "kickstart_image": ""
    #     "config_protocol" : "http"  <-- Currently HTTP and TFTP are
    #     supported
    #     "hostname" : "nxosv-9000-1"
    # }

    info = opener.open(req).read()
    return json.loads(info)


def image_install(kickstart="", system="", tftp_server=""):
    """Copies the user requested image if different and install"""
    # TODO Kickstart image (research criteria for 7.x)    
    # 1. Check the current install image
    poap_log("Checking the current image...")
    try:
        show_ver = cli("show version")
        _version = re.search(r'NXOS\simage.+\/(.+bin)', show_ver)
        current_version = _version.group(1)
    except Exception:
        poap_log("Unable to identify current running version")
    
    # 2. If the current image is different from the target image, download target
    if current_version == system:
        poap_log("Target already matches current image. Skipping....")
        return
    else:
        vrf = "Management"
        poap_log("Transferring file {} over TFTP".format(system))
        copy_cmd = "terminal dont-ask ; "
        copy_cmd += "copy tftp://%s/%s bootflash:/%s vrf %s" % (tftp_server, system, system , vrf)
    try:
        cli(copy_cmd)
    except Exception as e:
        # Remove extra junk in the message
        if "no such file" in str(e):
            abort("Copy of %s failed: no such file" % system)
        elif "Permission denied" in str(e):
            abort("Copy of %s failed: permission denied" % system)
        elif "No space left on device" in str(e):
            abort("No space left on device")
        else:
            raise
    # TODO: MD5 sum validation
    # TODO: Loop to repeat for kickstart image 
    poap_log("Copy over TFTP, complete")

    # 3. Set the boot variable
    try:
        poap_log("config terminal ; boot nxos %s" % system)
        cli("config terminal ; boot nxos bootflash:///%s" % system)
        cli("copy running-config startup-config")
    except Exception as e:
        poap_log("Failed to set NXOS boot variable to %s" % system)
        abort(str(e))

def copy_config(**kwargs):
    """Copies over the desired start up configuration"""
    protocol = kwargs['config_protocol']
    hostname = kwargs['hostname']
    filename = kwargs['config_file']
    vrf = "Management"
    if protocol == "tftp":
        host = kwargs['tftp_server']
        poap_log("Transfering config file {} over TFTP".format(filename))
        copy_cmd = "terminal dont-ask ; "
        copy_cmd += "copy tftp://%s/%s bootflash:/%s vrf %s" % (host, filename, filename , vrf)
        poap_log("Command is : %s" % copy_cmd)
        try:
            cli(copy_cmd)
        except Exception as e:
            # Remove extra junk in the message
            if "no such file" in str(e):
                abort("Copy of %s failed: no such file" % filename)
            elif "Permission denied" in str(e):
                abort("Copy of %s failed: permission denied" % filename)
            elif "No space left on device" in str(e):
                abort("No space left on device")
            else:
                raise
            # TODO: MD5 sum validation 
            poap_log("Copy over TFTP, complete")
    elif protocol == "http":
        host = kwargs['http_server']
        s_no = filename.split('.')[0]
        poap_log("Transfering config file over HTTP...")
        try: 
            response = urllib2.urlopen('http://{}/conf/{}'.format(host, s_no)).read()
        except Exception:
            e_type, e_val, e_trace = sys.exc_info()
            poap_log("Exception: {0} {1}".format(e_type, e_val))
            while e_trace is not None:
                fname = os.path.split(e_trace.tb_frame.f_code.co_filename)[1]
                poap_log("Stack - File: {0} Line: {1}"
                         .format(fname, e_trace.tb_lineno))
                e_trace = e_trace.tb_next
                abort()
        poap_log("Data collected from HTTP request")
        # Write the config locally to a file
        dest = '/bootflash/{}'.format(filename)
        try: 
            with open(dest, 'w') as fh:
                fh.write(response)
        except Exception:
            e_type, e_val, e_trace = sys.exc_info()
            poap_log("Exception: {0} {1}".format(e_type, e_val))
            while e_trace is not None:
                fname = os.path.split(e_trace.tb_frame.f_code.co_filename)[1]
                poap_log("Stack - File: {0} Line: {1}"
                         .format(fname, e_trace.tb_lineno))
                e_trace = e_trace.tb_next
                abort()
        # TODO: MD5 sum validation 
        poap_log("Config data copied successfully to bootflash")

    cmd = "terminal dont-ask ;"
    cmd += "copy bootflash:/" + filename + " scheduled-config "
    poap_log("INFO: Ready to execute {}".format(cmd))
    try:
        cli(cmd)
    except Exception:
        e_type, e_val, e_trace = sys.exc_info()
        poap_log("Exception: {0} {1}".format(e_type, e_val))
        while e_trace is not None:
            fname = os.path.split(e_trace.tb_frame.f_code.co_filename)[1]
            poap_log("Stack - File: {0} Line: {1}"
                     .format(fname, e_trace.tb_lineno))
            e_trace = e_trace.tb_next
            abort()


        
def main():
    # Register the SIG TERM handler
    signal.signal(signal.SIGTERM, sigterm_handler)
    # Collect the switch details for POAP
    INSTALL_INFO = poap_collect()
    poap_log("Install info collected successfully...")
    # Download and Install the user requested image
    image_install(kickstart=INSTALL_INFO['kickstart_image'],
                  system=INSTALL_INFO['system_image'],
                  tftp_server=INSTALL_INFO['tftp_server'])
    # Download the POAP target configuration to NVRAM and reboot
    copy_config(**INSTALL_INFO)

        
if __name__ == "__main__":
    #Start logging 
    setup_logging()
    try:
        main()
    except Exception:
        e_type, e_val, e_trace = sys.exc_info()
        poap_log("Exception: {0} {1}".format(e_type, e_val))
        while e_trace is not None:
            fname = os.path.split(e_trace.tb_frame.f_code.co_filename)[1]
            poap_log("Stack - File: {0} Line: {1}"
                     .format(fname, e_trace.tb_lineno))
            e_trace = e_trace.tb_next
            abort()
