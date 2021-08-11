
variable "project" {
  description = "Project ID to use, example: tonto-cloudwalk1234"
  type    = string

}

variable "region" {
  description = "Region to create resources"
  type    = string
  default = "us-central"
}

variable "authtoken" {
  description = "Authentication token for tonto.cloudwalk.io"
  type    = string
}

variable "check_interval" {
  description = "Time between checks(in seconds)"
  type    = number
  default = 5
}

variable "check_timeout" {
  description = "Timeout in seconds"
  type    = number
  default = 20
}

variable "health_threshold" {
  description = "Number of sequential success checks to be considered Healthy"
  type    = number
  default = 3
}

variable "unhealth_threshold" {
  description = "Number of sequential failed checks to be considered Unhealthy"
  type    = number
  default = 3
}

variable "mail_notify" {
  description = "Mail To send the notification"
  type    = string
}

variable "mail_server" {
  description = "Mail provider SMTP Address"
  type    = string
}

variable "mail_port" {
  description = "Mail provider SMTP port"
  type    = number
  default = 465
}

variable "mail_user" {
  description = "Mail to login in SMTP server"
  type    = string
}

variable "mail_password" {
  description = "Mail Password"
  type    = string
  sensitive   = true
}

variable "loglevel" {
  description = "debug|info|warning|error"
  type    = string
  default = "debug"
}


