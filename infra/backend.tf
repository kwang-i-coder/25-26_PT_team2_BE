terraform {
    backend "gcs" {
        bucket = "jandi-gdgoc-bucket-tfstate"
        prefix = "terraform/state"
    }
} 