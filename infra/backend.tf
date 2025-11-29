terraform {
    backend "gcs" {
        bucket = "k8s-standard-bucket-tfstate"
        prefix = "terraform/state"
    }
}