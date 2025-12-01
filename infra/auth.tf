module "gke_auth" {
    source = "terraform-google-modules/kubernetes-engine/google//modules/auth"
    version = "37.0.0"
    project_id = var.project_id
    location = module.gke.location
    cluster_name = module.gke.name
    use_private_endpoint = true
    depends_on = [module.gke]
    # module.gk에 의존. 
}

resource "local_file" "kubeconfig" {
    content = module.gke_auth.kubeconfig_raw
    filename = "kubeconfig-${var.env_name}"
}