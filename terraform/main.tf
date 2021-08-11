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