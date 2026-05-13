terraform {
  required_version = ">= 1.6"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_storage_bucket" "tf_state" {
  name          = "${var.project_id}-tfstate"
  location      = "US"
  force_destroy = true
  versioning {
    enabled = true
  }
}

resource "google_storage_bucket" "logs" {
  name          = "${var.project_id}-logs"
  location      = "US"
  force_destroy = true
  versioning {
    enabled = true
  }
}