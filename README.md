# Cloudwalk Challenge

### Get Started
This app will perform http and tcp tests as described in [Cloudwalk Challenge](https://gist.github.com/dgvcwk/919a6fcca40f4e314b2dc135b47d4a5e)

This app is ready to go for GCP, you can login via [gcloud sdk](https://cloud.google.com/sdk/gcloud) and deploy it using [terraform](https://www.terraform.io/)

#### Terraform: v1.0.4


```sh
git clone https://github.com/LeoMarangoni/tonto.cloudwalk.io.git
cd tonto.cloudwalk.io/terraform
gcloud init # Login with your GCP credentials
```

- Edit the main.tf file. Example:
```hcl
# tonto.cloudwalk.io/terraform/main.tf
module "tontocloudwalk" {
  source = "./tontocloudwalk"
  project = "tonto-cloudwalk-example123" # Project ID
  authtoken = "" # Set here the authentication token
  mail_notify = "user2@example.com" 
  mail_port = 465
  mail_server = "smtp.gmail.com"
  mail_user = "user@gmail.com" # Mail account that would be used for sending mail
  mail_password = "custom_password" # Password of mail account
  check_interval = 5 # Time between checks (in seconds)
  check_timeout = 10 # Timeout in seconds
  health_threshold = 3 # "Number of sequential successful checks to be considered Healthy"
  unhealth_threshold = 3 # Number of sequential failed checks to be considered Unhealthy
}




Deploying to [Google Cloud App Engine](https://console.cloud.google.com/appengine)
```sh
gcloud components install app-engine-python
gcloud config set project tonto-cloudwalk-example123
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
If you get this error on logs: `Please log in via your web browser and then try again`
Maybe you need to bypass your email [here](https://accounts.google.com/DisplayUnlockCaptcha)

### TODOs
- [X] import configs from env vars instead setting in config.py
- [X] Adjust '/feed' endpoint to return RSS feed instead of list of events
- [X] Improve this README
- [X] Adjust notify to handle SSL and Non SSL connections via SMTP
- [X] Test different mail providers besides gmail(Validated against outlook, and zimbra mail)
- [ ] Refact some pieces of code
- [ ] CI/CD
