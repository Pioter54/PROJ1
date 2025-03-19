resource "google_storage_bucket" "bucket" {
  name          = "terraform-bucket-example"
  location      = "US"
  force_destroy = true
}