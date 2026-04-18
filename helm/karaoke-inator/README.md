# Karaoke-Inator Helm Chart

Production-ready Kubernetes Helm chart for deploying the Karaoke-Inator microservices application on on-premises infrastructure.

## Overview

This chart deploys a complete microservices stack for audio processing including:
- **Core Services**: Orchestrator, Voice Separation, Lyrics Extraction, Song Management
- **Infrastructure**: PostgreSQL, Redis, MinIO, nginx Ingress Controller
- **Observability**: Prometheus, Grafana, Tempo, OpenTelemetry Collector
- **Security**: Automatic SSL/TLS with Let's Encrypt (via cert-manager)

## Prerequisites

### Kubernetes Cluster
- Kubernetes 1.24+ installed
- kubectl configured with cluster access
- Minimum resources: 4 CPU cores, 12GB RAM, 1TB storage

### Required Components (Install Before Chart)
```bash
# 1. Install cert-manager for SSL/TLS
helm repo add jetstack https://charts.jetstack.io
helm repo update
helm install cert-manager jetstack/cert-manager \
  --namespace cert-manager \
  --create-namespace \
  --version v1.14.0

# 2. Install NGINX Ingress Controller (or use chart's built-in)
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update
helm install nginx-ingress ingress-nginx/ingress-nginx \
  --namespace ingress-nginx \
  --create-namespace
```

### Infrastructure Setup
Create required directories on each Kubernetes node:

```bash
sudo mkdir -p /data/{postgres,redis,minio,prometheus,tempo,grafana}
sudo mkdir -p /data/models/{voice-separation,lyrics-extraction}
sudo chown -R 1000:1000 /data  # Adjust UID/GID as needed
```

### Domain Configuration
Ensure your domain (default: `hatal.cc`) DNS points to your Kubernetes cluster's public IP.

## Installation

### Basic Installation
```bash
helm install karaoke ./helm/karaoke-inator \
  --namespace karaoke \
  --create-namespace \
  --set postgresql.auth.password="YOUR_SECURE_PASSWORD" \
  --set minio.auth.rootUser="minio" \
  --set minio.auth.rootPassword="YOUR_SECURE_PASSWORD"
```

### Production Installation
```bash
helm install karaoke ./helm/karaoke-inator \
  --namespace karaoke \
  --create-namespace \
  -f helm/karaoke-inator/values-prod.yaml \
  --set postgresql.auth.password="YOUR_SECURE_PASSWORD" \
  --set minio.auth.rootUser="minio" \
  --set minio.auth.rootPassword="YOUR_SECURE_PASSWORD"
```

### Custom Domain
```bash
helm install karaoke ./helm/karaoke-inator \
  --namespace karaoke \
  --create-namespace \
  --set global.domain="your-domain.com" \
  --set networking.ingress.host="your-domain.com" \
  --set networking.certManager.email="your-email@example.com" \
  --set postgresql.auth.password="YOUR_SECURE_PASSWORD" \
  --set minio.auth.rootUser="minio" \
  --set minio.auth.rootPassword="YOUR_SECURE_PASSWORD"
```

### Disable Observability Stack
```bash
helm install karaoke ./helm/karaoke-inator \
  --namespace karaoke \
  --create-namespace \
  --set observability.enabled=false \
  [other options]
```

## Configuration

### Key Values

| Parameter | Default | Description |
|-----------|---------|-------------|
| `global.namespace` | `karaoke` | Kubernetes namespace |
| `global.domain` | `hatal.cc` | Public domain name |
| `global.letsencryptEmail` | `admin@hatal.cc` | Let's Encrypt contact email |
| `postgresql.auth.password` | `""` | **REQUIRED** PostgreSQL password |
| `minio.auth.rootUser` | `""` | **REQUIRED** MinIO root user |
| `minio.auth.rootPassword` | `""` | **REQUIRED** MinIO root password |
| `observability.enabled` | `true` | Enable monitoring stack |

### Complete Configuration
See `values.yaml` for all configurable options including:
- Resource requests/limits for each service
- Persistence configuration
- Replica counts
- Health check settings
- OTEL collector configuration

## Accessing Your Application

### Public Access
Once deployed and certificate is issued:
```
https://hatal.cc
```

### Monitoring Dashboards (Port-Forward Only)

**Quick Start:**
```bash
# Start all port-forwards at once
./helm/karaoke-inator/scripts/port-forward-all.sh
```

**Individual Dashboards:**

Grafana (Visualization):
```bash
kubectl port-forward svc/grafana 3000:3000 -n observability
# http://localhost:3000 (admin/admin)
```

Prometheus (Raw Metrics):
```bash
kubectl port-forward svc/prometheus 9090:9090 -n observability
# http://localhost:9090
```

Tempo (Distributed Tracing):
```bash
kubectl port-forward svc/tempo 3200:3200 -n observability
# http://localhost:3200
```

## Architecture

### Services
- **Orchestrator** (8000): Main API gateway, coordinates processing pipeline
- **Voice Separation** (8001): ML service for separating vocals/instruments
- **Lyrics Extraction** (8002): ML service for extracting lyrics and timestamps
- **Song Management** (8003): Database management service
- **RQ Worker**: Background job processor for asynchronous tasks

### Infrastructure
- **PostgreSQL**: Relational database for metadata
- **Redis**: Cache and job queue
- **MinIO**: S3-compatible object storage for audio files
- **nginx**: Ingress controller with TLS termination

### Observability
- **Prometheus**: Metrics collection and storage
- **Grafana**: Visualization and dashboards
- **Tempo**: Distributed tracing backend
- **OTEL Collector**: Telemetry aggregation hub

## Storage

### Storage Class
Uses `local-storage` StorageClass for hostPath-based persistence.

Configure before installation:
```bash
kubectl apply -f - <<EOF
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: local-storage
provisioner: kubernetes.io/no-provisioner
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
EOF
```

### Persistent Volumes

| Component | Size | Path | Mount |
|-----------|------|------|-------|
| PostgreSQL | 100Gi | `/data/postgres` | `/var/lib/postgresql/data` |
| Redis | 10Gi | `/data/redis` | `/data` |
| MinIO | 500Gi | `/data/minio` | `/data` |
| Voice Separation | 50Gi | `/data/models/voice-separation` | `/app/.cache/huggingface` |
| Lyrics Extraction | 50Gi | `/data/models/lyrics-extraction` | `/app/.cache/huggingface` |
| Prometheus | 50Gi | `/data/prometheus` | `/prometheus` |
| Tempo | 30Gi | `/data/tempo` | `/var/tempo` |
| Grafana | 10Gi | `/data/grafana` | `/var/lib/grafana` |

## Troubleshooting

### Pods Not Starting
```bash
# Check pod status
kubectl get pods -n karaoke

# View logs
kubectl logs <pod-name> -n karaoke

# Describe pod for events
kubectl describe pod <pod-name> -n karaoke
```

### Certificate Not Issued
```bash
# Check cert-manager
kubectl logs -l app=cert-manager -n cert-manager

# Verify certificate
kubectl describe certificate karaoke-tls -n karaoke

# Check DNS
nslookup hatal.cc
```

### Services Not Communicating
```bash
# Test from pod
kubectl exec -it <pod> -n karaoke -- /bin/bash
curl http://orchestrator.karaoke.svc.cluster.local:8000/health
```

### Storage Issues
```bash
# Check PVCs
kubectl get pvc -n karaoke
kubectl describe pvc <pvc-name> -n karaoke

# Verify mount paths
kubectl exec -it <pod> -n karaoke -- ls -la /data
```

## Maintenance

### Upgrade
```bash
helm upgrade karaoke ./helm/karaoke-inator \
  -f values-prod.yaml \
  [options]
```

### Uninstall
```bash
helm uninstall karaoke -n karaoke
```

### Scaling
```bash
kubectl scale deployment <service> --replicas=3 -n karaoke
```

### Viewing Logs
```bash
# Last 100 lines
kubectl logs -n karaoke <pod-name> --tail=100

# Stream logs
kubectl logs -f -n karaoke deployment/<deployment>
```

### Resource Usage
```bash
kubectl top nodes
kubectl top pods -n karaoke
```

## Security Considerations

1. **Secrets Management**
   - Don't commit secrets to version control
   - Use `--set` at install time or external secret management
   - Rotate passwords regularly

2. **Network Policies**
   - Consider adding NetworkPolicies to restrict inter-pod communication
   - Observability is port-forward only (not publicly exposed)

3. **RBAC**
   - Chart creates minimal ServiceAccount for core functionality
   - Extend RBAC as needed for your environment

4. **TLS/SSL**
   - Automatic renewal via cert-manager
   - Monitor certificate expiry

## Performance Tuning

### Resource Requests
Adjust in `values-prod.yaml`:
```yaml
resources:
  requests:
    cpu: "500m"
    memory: "1Gi"
  limits:
    cpu: "1000m"
    memory: "2Gi"
```

### Database Optimization
- Add indexes for frequently queried columns
- Configure connection pooling
- Regular VACUUM/ANALYZE

### Redis Optimization
- Adjust `maxmemory-policy` in redis config
- Monitor memory usage
- Enable persistence (AOF)

## Support

Issues and questions: https://github.com/majoporse/karaoke-inator/issues

## License

See LICENSE in the main project repository.
