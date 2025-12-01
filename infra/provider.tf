terraform {
    required_version = ">= 1.5.7"
    required_providers {
        google = {
            source = "hashicorp/google"
            version = ">= 6.19.0, < 7.0.0"
        }
        local = {
            source = "hashicorp/local"
            version = "2.4.0"
        }
        kubernetes = {
            source = "hashicorp/kubernetes"
            version = "2.24.0"
        }
    }
}

provider "google" {
    project = var.project_id
    region = var.region
    credentials = file("calm-scarab-478705-c7-b25fdd5670c3.json")
}