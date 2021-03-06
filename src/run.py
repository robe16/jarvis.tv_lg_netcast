from multiprocessing import Process
from discovery.broadcast import broadcast_service
from portlistener import start_bottle
from config.config import get_cfg_serviceid, get_cfg_port
from log.log import log_internal
from resources.global_resources.log_vars import logPass, logException
from resources.lang.enGB.logs import *


try:

    ################################

    log_internal(logPass, logDescStartingService, description='started')

    ################################
    # Initiate service broadcast

    process_broadcast = Process(target=broadcast_service, args=(get_cfg_serviceid(), get_cfg_port(), ))
    process_broadcast.start()

    ################################
    # Port_listener

    log_internal(logPass, logDescPortListener.format(port=get_cfg_port()), description='starting')

    start_bottle()

    process_broadcast.terminate()

    log_internal(logPass, logDescPortListener.format(port=get_cfg_port()), description='stopped')

except Exception as e:
    log_internal(logException, logDescStartingService, description='fail', exception=e)
