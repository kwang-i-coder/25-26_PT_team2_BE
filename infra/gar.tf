resource "google_artifact_registry_repository" "jandi-images-repo" { # 리소스 이름 변경
  location      = "asia-northeast3" # GKE 리전에 맞게 변경
  repository_id = "jandi-images-repo"  # 저장소 이름 변경
  description   = "Repository for all backend microservice Docker images"
  format        = "DOCKER"

  docker_config {
    immutable_tags = true
  }
}