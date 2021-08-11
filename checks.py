import time
import requests
import socket
import config
import select
import logging
from datetime import datetime
from functools import wraps
from notify import Notify

def keep(func, service_name, interval, health_th, unhealth_th):
    """Decorator to keep checking services forever
    Triggers notification after reaching threashold

    func -> Check function to keep running
    service_name -> Name of the service checked
    interval -> Interval in seconds between checks
    health_th -> Number of consecutive health checks to be considered healthy
    unhealth_th -> Number of consecutive unhealth checks to be considered healthy
    """

    @wraps(func)
    def ret_func(*args, **kwargs):
        notify = Notify(config.mail_server, config.mail_port, config.mail_user,config.mail_password, config.mail_notify)
        #config.events.append({**config.current_status[service_name], **{'service':service_name}})
        h_counter=0
        uh_counter=0
        while True:
            current_status = config.data.get().get('current_status') 
            is_up = func(*args, **kwargs)
            if current_status[service_name]['status']=='unhealthy':
                if not is_up:
                    h_counter=0
                else:
                    h_counter+=1
            if current_status[service_name]['status']=='healthy':
                if is_up:
                    uh_counter=0
                else:
                    uh_counter+=1  
            if uh_counter==unhealth_th:
                current_status[service_name]['status']='unhealthy'
                current_status[service_name]['updated']=datetime.now()
                config.data.set({'current_status': current_status})
                uh_counter=0
                logging.info("reached threashold(%s), %s is DOWN" %(unhealth_th, service_name))
                myemail = notify.create_email(service_name,'unhealthy')
                notify.send_email(myemail)
                config.events.append({**current_status[service_name], **{'service':service_name}})

            if h_counter==health_th:
                current_status[service_name]['status']='healthy'
                current_status[service_name]['updated']=datetime.now()
                config.data.set({'current_status': current_status})
                h_counter=0
                logging.info("reached threashold(%s), %s is UP" %(health_th, service_name))
                myemail = notify.create_email(service_name,'healthy')
                notify.send_email(myemail)
                config.events.append({**current_status[service_name], **{'service':service_name}})
          
            logging.debug("health count: %s - unhealth count: %s" %(h_counter, uh_counter))
            logging.debug(current_status)
            time.sleep(interval)

    return ret_func


def http_check(url, token, msg, timeout):
    """Get message returned in an HTTP endpoint, then compares with expected
        If gets what it expected, then return True, else return False 
    """
    expected_msg="CLOUDWALK %s" %(msg)
    is_up = False
    clean_text=""
    try:
        r = requests.get('%s/?auth=%s&buf=%s' %(url, token, msg), timeout=timeout)
        raw_text=r.text
        #remove line breaks and tabs from response
        clean_text=raw_text.replace("\n","").replace("\t","")
        is_up = clean_text==expected_msg
    except Exception as e:
        logging.warning(e)
    finally:
        logging.debug(
            "received: %s - expected: %s - UP: %s"
             %(clean_text, expected_msg, is_up)
        )
        return is_up





def tcp_check(host, port, token, msg, timeout):
    """Get message returned in a TCP endpoint, then compares with expected
        If gets what it expected, then return True, else return False 
    """
    is_up = False
    msg = msg.encode()
    expected_msg=b'CLOUDWALK ' + msg
    try:
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp.settimeout(timeout)
        tcp.connect((host, port))
        tcp.send(str.encode('auth ' + token))
        data = tcp.recv(16)
        if data==b"auth ok\n":
            logging.debug("authenticated via tcp")
            data=b''
            try:
                logging.debug('sending "%s"' % msg)
                tcp.sendall(msg)
                ready = select.select([tcp], [], [], timeout)
                if ready[0]:
                    data = tcp.recv(len(expected_msg) + 10)
            except Exception as e:
                logging.warning(e)
            finally:
                tcp.close()
                clean_text = data.replace(b'\x00',b'').replace(b"\n",b"").replace(b"\t",b"")
                is_up = clean_text==expected_msg
                logging.debug(
                    "received: %s - expected: %s - UP: %s"
                    %(clean_text, expected_msg, is_up)
                )

        else:
            logging.info("Auth Failure: %s" %(data))
            tcp.close()
    except Exception as e:
        logging.warning(e)
    finally:
        return is_up

#Decorating checks
http_check = keep(
    http_check, 'http',
    config.check_interval,
    config.health_threshold,
    config.unhealth_threshold
    )
tcp_check = keep(
    tcp_check, 'tcp', 
    config.check_interval, 
    config.health_threshold, 
    config.unhealth_threshold
    )
