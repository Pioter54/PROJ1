terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
  }
}

provider "google" {
  project = "my-project"
  zone    = "us-central1-a"
}

resource "null_resource" "delete_vm" {
  provisioner "local-exec" {
    command = "gcloud compute instances delete ${var.name} --project=${var.project} --zone=${var.zone} --quiet"
  }
}

variable "project" {
  description = "The GCP project ID"
  type        = string
}

variable "zone" {
  description = "The zone where the VM is located"
  type        = string
}

variable "name" {
  description = "The name of the VM to delete"
  type        = string
} 