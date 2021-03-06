import threading
import config
from checks import http_check, tcp_check

from flask import Flask, render_template, make_response, request

def create_app():
    '''We need this method to inicialize our checking services before starting
        Our http server.
    '''
    app = Flask(__name__)
    config.init()
    th_http = threading.Thread(
        target=http_check, args=(
            config.http_ep,
            config.token,
            config.test_string,
            config.check_timeout
        )
    )

    th_tcp = threading.Thread(
        target=tcp_check, args=(
            config.tcp_ep,
            config.tcp_port,
            config.token,
            config.test_string,
            config.check_timeout
        )
    )

    th_tcp.start()
    th_http.start()
    return app

app = create_app()

@app.route("/")
def index():
    return render_template(
        'dash.html',
        services=config.data.get().get('current_status'), # Get current_status from firestore 
        events=config.events)

@app.route("/feed")
def newfeed():
    template =  render_template('feed.xml', events=config.events, uri=request.host_url, mail=config.mail_user)
    response = make_response(template)
    response.headers['Content-Type'] = 'application/xml'
    return response


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, threaded=True)
