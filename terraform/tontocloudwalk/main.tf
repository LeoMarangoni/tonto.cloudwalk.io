provider "google" {
  region  = var.region
  project = var.project
}


resource "google_project" "tontoapp" {
  name       = "Tonto Test Appplication"
  project_id = var.project
}

resource "google_app_engine_application" "app" {
  project = google_project.tontoapp.project_id
  location_id = var.region
  database_type = "CLOUD_FIRESTORE"
}

resource google_project_service "firestore" {
  service = "firestore.googleapis.com"
  disable_dependent_services = true
  depends_on = [
    google_project.tontoapp
  ]
}

resource "time_sleep" "wait_30_seconds" {
  depends_on = [
    google_project_service.firestore, google_app_engine_application.app,
  ]

  create_duration = "30s"
}

resource "google_firestore_document" "config" {
  project     = var.project
  depends_on = [time_sleep.wait_30_seconds]
  collection  = "tontocloudwalk"
  document_id = "config"
  fields      = jsonencode(
            {
              authtoken          = {
                   stringValue = var.authtoken
                }
              check_interval     = {
                  integerValue = var.check_interval
                }
              check_timeout      = {
                  integerValue = var.check_timeout
                }
              health_threshold   = {
                  integerValue = var.health_threshold
                }
              loglevel           = {
                  stringValue = var.loglevel
                }
              mail_notify        = {
                  stringValue = var.mail_notify
                }
              unhealth_threshold = {
                  integerValue = var.unhealth_threshold
                }
              mail               = {
                  mapValue = {
                      fields = {
                          password = {
                              stringValue = var.mail_password
                            }
                          port     = {
                              integerValue = var.mail_port
                            }
                          server   = {
                              stringValue = var.mail_server
                            }
                          user     = {
                              stringValue = var.mail_user
                            }
                        }
                    }
                }
            }
        )
}

resource "google_firestore_document" "data" {
  project     = var.project
  collection  = "tontocloudwalk"
  depends_on = [time_sleep.wait_30_seconds]

  document_id = "data"
  fields      = jsonencode(
          {
              current_status = {
                  mapValue = {
                      fields = {
                          http = {
                              mapValue = {
                                  fields = {
                                      status  = {
                                          stringValue = "unhealthy"
                                        }
                                      updated = {
                                          timestampValue = timestamp()
                                        }
                                    }
                                }
                            }
                          tcp  = {
                              mapValue = {
                                  fields = {
                                      status  = {
                                          stringValue = "unhealthy"
                                        }
                                      updated = {
                                          timestampValue = timestamp()
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        )
}
