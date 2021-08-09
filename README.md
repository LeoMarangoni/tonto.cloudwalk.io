# Cloudwalk Challenge

### Get Started
This app will perform http and tcp tests as described in [Cloudwalk Challenge](https://gist.github.com/dgvcwk/919a6fcca40f4e314b2dc135b47d4a5e)
You need to inform an username and password in config file to be able to receive email notifications

```sh
git clone https://github.com/LeoMarangoni/tonto.cloudwalk.io.git
cd tonto.cloudwalk.io.git
# edit config.py

```


this app is ready to be deployed in [Google Cloud App Engine](https://console.cloud.google.com/appengine)
```sh
gcloud init
gcloud components install app-engine-python
gcloud app create --project tonto-cloudwalk
gcloud app deploy
```
You can check system logs using `gcloud app logs tail -s default`


running localy:
```
python3 -m venv .
source bin/activate
pip install -r requirements.txt
python main.py
```

Note: For use GMAIL account for sending notification, maybe you need to change settings in
[google security page](https://myaccount.google.com/security). There you may look for "third party apps" or "app password"

### TODOs
- TODO: import configs from env vars instead setting in config.py
- TODO: Adjust '/feed' endpoint to return RSS feed instead of list of events
- TODO: Improve this README
- TODO: Adjust notify to handle SSL and Non SSL connections via SMTP
- TODO: Test different mail providers besides gmail
- TODO: Refact some pieces of code