# example usage:
# python3 sample_main.py -config docker/sample-config.toml
from rest_service.config import Config
from rest_service.service import RestService
import argparse
import sys
import time

CMD_DESC = 'start the rest service.'
parser = argparse.ArgumentParser(description=CMD_DESC)
parser.add_argument('-config', type=str, default=None,
                    help='config file containing client information')

args = parser.parse_args()

if args.config is None:
    print ('config file is required')
    sys.exit(1)

Config.parse_config(args.config)
service = RestService.from_config()
service.run()

try:
    while True:
        time.sleep(60)
except KeyboardInterrupt:
    pass

service.stop()
sys.exit(0)

