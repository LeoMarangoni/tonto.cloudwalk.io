import logging
from datetime import datetime

# Get configs stored in Google FireStore
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred)
db = firestore.client()
config = db.collection('tontocloudwalk').document('config').get()
###

#common
token=config.get('authtoken') # CloudWalk challenge access token
check_timeout=config.get('check_timeout')
check_interval=config.get('check_interval')
health_threshold=config.get('health_threshold')
unhealth_threshold=config.get('unhealth_threshold')
mail_notify=config.get('mail_notify') # user that will be notified
test_string='my text to check services' # String that would be send to the services

# Endpoints
##http
http_ep='https://tonto-http.cloudwalk.io' #http endpoint
##tcp
tcp_ep='tonto.cloudwalk.io' #tcp endpoint
tcp_port=3000


#email
mail_server='smtp.gmail.com'
mail_port=465
mail_user='' # email used for sending notifications
mail_password=''

#logger
loglevels = {
    'debug':logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING, 
    'error': logging.ERROR
}

loglevel = loglevels[config.get('loglevel')] # set log level to debug|info|warn|error


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
