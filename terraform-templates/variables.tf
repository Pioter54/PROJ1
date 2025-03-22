variable "project_id" {
  description = "ID projektu w Google Cloud"
  type        = string
}

variable "region" {
  description = "Region dla zasobów"
  type        = string
  default     = "us-central1"
}

variable "machine_type" {
  description = "Typ maszyny wirtualnej"
  type        = string
  default     = "e2-medium"
}

variable "bucket_name" {
  description = "Nazwa bucketu storage"
  type        = string
}