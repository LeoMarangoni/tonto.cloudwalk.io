import threading
import config
from checks import http_check, tcp_check

from flask import Flask, render_template

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
    return render_template('dash.html', services=config.current_status, events=config.events)

#TODO: return a rss feed page instead of event listing
@app.route("/feed")
def feed():
    return render_template('feed.html', events=config.events)


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, threaded=True)