import sys, logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/')
from poap_server import app as application
