#import os
#from dotenv import load_dotenv

#TODO: use env vars instead setting in file

from datetime import datetime
import logging

#common
token='' # CloudWalk challenge access token
test_string='my text to check services' 
check_timeout=10
check_interval=2
health_threshold=3
unhealth_threshold=3

#http
http_ep='https://tonto-http.cloudwalk.io' #http endpoint

#tcp
tcp_ep='tonto.cloudwalk.io' #tcp endpoint
tcp_port=3000


#email
mail_server='smtp.gmail.com'
mail_port=465
mail_user='' # email used for sending notifications
mail_password=''
mail_notify='' # user that will be notified

#logger
loglevels = {
    'debug':logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING, 
    'error': logging.ERROR
}

loglevel = loglevels['debug'] # set log level to debug|info|warn|error


def init():
    """logger config and Global vars to store shared data of service status"""
    global current_status
    global events
    events = []
    current_status = {
        'http': {"status":'unhealthy',"updated":datetime.now()},
        'tcp': {"status":'unhealthy',"updated":datetime.now()}
    
    }
    logging.basicConfig(level=loglevel, format='%(asctime)s|%(levelname)s|%(funcName)s|%(message)s')
