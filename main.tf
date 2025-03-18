provider "google" {
  project = "modern-rhythm-444518-n9"
  region  = "us-central1"
}

resource "google_compute_instance" "vm_instance" {
  name = "modern-rhythm-444518-n9-vm"
  machine_type = "e2-micro"
  zone = "us-central1-a"

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-12"
    }
  }

  network_interface {
    network = "default"
    access_config {
      // Ephemeral public IP
    }
  }
}
