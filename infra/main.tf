# GKE 클러스터와, 별도로 관리되는 노드 풀을 생성
data "google_client_config" "default" {}

provider "kubernetes" {
    host = "https://${module.gke.endpoint}"
    token = data.google_client_config.default.access_token
    cluster_ca_certificate = base64decode(module.gke.ca_certificate)
}

resource "google_service_account" "default" {
    # google_service_account 리소스의 account_id에는 서비스 계정의 전체 이메일이 아닌 고유 ID 부분만 포함
    account_id = "jandi-gke-sa"
    project = var.project_id
    display_name = "Jandi GKE Service Account"
    description = "Service Account for Jandi GKE cluster"
}

module "gke" {
    source = "terraform-google-modules/kubernetes-engine/google//modules/private-cluster"
    version = "37.0.0"
    project_id = var.project_id
    name = var.cluster_name
    region = var.region
    zones = var.zones
    network = module.vpc.network_name
    subnetwork = module.vpc.subnets_names[0]
    ip_range_pods = var.ip_range_pods_name
    ip_range_services = var.ip_range_services_name
    http_load_balancing = true
    network_policy = true
    # private_cluster_config = true
    horizontal_pod_autoscaling = true
    filestore_csi_driver = false
    enable_private_endpoint = false
    enable_private_nodes = true
    master_ipv4_cidr_block = "10.0.0.0/28"
    deletion_protection = false

    service_account = "jandi-gke-sa@${var.project_id}.iam.gserviceaccount.com"
    
    node_pools = [
        {
            name = "default-node-pool"
            machine_type = "e2-standard-4"
            # node_locations = ["asia-northeast3-b", "asia-northeast3-c"]
            #node_count = 2
            #min_count = 2
            #max_count = 5
            #disk_size_gb = 30
            #spot = false
            #image_type = "COS_CONTAINERD"
            #disk_type = "pd-standard"
            #logging_variant = "DEFAULT"
            #auto_repair = true
            #auto_upgrade = true

        }
    ]

    node_pools_labels = {
        all = {}
        default-node-pool = {
            default-node-pool = true
        }
    }

    node_pools_metadata = {
        all = {}
        default-node-pool = {
            # 노드가 종료될 때, kubectl drain 명령어를 사용하여 파드를 안전하게 제거하고 필요하면 다른 노드로 재스케줄링
            shutdown-script = "kubectl --kubeconfig=/var/lib/kubelet/kubeconfig drain --force=true --ignore-daemonsets=true --delete-local-data \"$HOSTNAME\""
            node-pool-metadata-custom-value = "default-node-pool"
        }
    }

    node_pools_taints = {
        all = []

        default-node-pool = [
            {
                key = "default-node-pool"
                value = true
                effect = "PREFER_NO_SCHEDULE"
            }
        ]
    }

    node_pools_tags = {
        all = []

        default-node-pool = [
            "default-node-pool",
        ]
    }

    depends_on = [module.vpc, google_service_account.default]
}