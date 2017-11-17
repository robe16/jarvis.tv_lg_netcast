import sys
from multiprocessing import Process
from discovery.broadcast import broadcast_service
from portlistener import start_bottle
from lgtv_netcast.lgtv_netcast import tv_lg_netcast
from config.config import get_cfg_serviceid
from resources.global_resources.variables import *
from log.log import Log

_log = Log()


try:

    _log.new_entry(logCategoryProcess, '-', 'Starting micro service', '-', 'starting')

    ################################
    # Receive sys arguments

    # Argument 1: Port of self exposed on host
    try:
        self_port = sys.argv[1]
    except Exception as e:
        raise Exception('self_port not available - {e}'.format(e=e))

    # Argument 1: Port of self exposed on host
    try:
        self_port = sys.argv[1]
        self_broadcastPort = sys.argv[2]
    except Exception as e:
        raise Exception('self_broadcastPort not available - {e}'.format(e=e))

    ################################
    # Initiate service broadcast

    process_broadcast = Process(target=broadcast_service, args=(get_cfg_serviceid, self_port, self_broadcastPort, ))
    process_broadcast.start()

    ################################
    # Create 'object'

    _device = tv_lg_netcast()

    _log.new_entry(logCategoryProcess, '-', 'Device object created',
                   'service_id-{service_id}'.format(service_id=get_cfg_serviceid()), 'success')

    ################################
    # Port_listener

    _log.new_entry(logCategoryProcess, '-', 'Port listener', 'port-{port}'.format(port=self_port), 'starting')

    start_bottle(self_port, _device)

    process_broadcast.terminate()

    _log.new_entry(logCategoryProcess, '-', 'Port listener', '-'.format(port=self_port), 'stopped')

except Exception as e:
    print('An error has occurred starting micro service: {e}'.format(e=e))
    _log.new_entry(logCategoryProcess, '-', 'Starting micro service', e, 'fail', level=logLevelError)
