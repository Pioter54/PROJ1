resource "google_storage_bucket" "bucket" {
  name          = "terraform-bucket-example"
  location      = "US"
  storage_class = "STANDARD"
}