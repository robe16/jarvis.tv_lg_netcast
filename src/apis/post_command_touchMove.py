from bottle import HTTPResponse, HTTPError

from common_functions.request_enable_cors import enable_cors
from common_functions.request_log_args import get_request_log_args
from log.log import log_inbound
from resources.global_resources.log_vars import logPass, logFail, logException
from resources.global_resources.variables import *
from validation.validation import validate_touchMove


def post_command_touchMove(request, _tvlgnetcast):
    #
    args = get_request_log_args(request)
    #
    try:
        #
        data_dict = request.json
        #
        if validate_touchMove(data_dict):
            #
            x = data_dict['touchMoveX']
            y = data_dict['touchMoveY']
            r = _tvlgnetcast.sendTouchmove(x, y)
            #
            if not bool(r):
                status = httpStatusFailure
                result = logFail
            else:
                status = httpStatusSuccess
                result = logPass
        else:
            status = httpStatusBadrequest
            result = logFail
        #
        args['result'] = result
        args['http_response_code'] = status
        args['description'] = '-'
        log_inbound(**args)
        #
        response = HTTPResponse()
        response.status = status
        enable_cors(response)
        #
        return response
        #
    except Exception as e:
        #
        status = httpStatusServererror
        #
        args['result'] = logException
        args['http_response_code'] = status
        args['description'] = '-'
        args['exception'] = e
        log_inbound(**args)
        #
        raise HTTPError(status)
