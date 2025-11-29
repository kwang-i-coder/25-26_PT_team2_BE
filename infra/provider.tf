terraform {
    required_version = ">= 1.6"
    required_providers {
        google = {
            source = "hashicorp/google"
            version = "~> 5.7.0"
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