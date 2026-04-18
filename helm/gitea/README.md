# Gitea Installation & Configuration

This directory contains the Gitea Helm chart configuration for self-hosted Git and Docker Registry.

## Overview

**Gitea** provides:
- Self-hosted Git repository management
- Built-in Docker/Container Registry
- Web UI for repository management
- SSH access for Git operations
- User and access token management

The registry is accessible at `git.hatal.cc:5000` for Docker operations.

## Files

- **values.yaml**: Helm chart configuration for Gitea deployment
- **README.md**: This file

## Configuration Details

### Key Settings

| Setting | Value | Purpose |
|---------|-------|---------|
| `admin.username` | `admin` | Default admin user |
| `admin.password` | `lokoloko_karaoke` | Admin password (change in production!) |
| `admin.email` | `admin@hatal.cc` | Admin email address |
| `DOMAIN` | `git.hatal.cc` | Domain for web access |
| `SSH_DOMAIN` | `git.hatal.cc` | Domain for SSH (e.g., `git clone ssh://...`) |
| `ROOT_URL` | `https://git.hatal.cc` | External URL (used for redirects, webhooks) |
| `PROTOCOL` | `http` | Internal protocol (Traefik handles HTTPS) |
| `HTTP_PORT` | `3000` | Internal port inside container |
| `persistence.size` | `20Gi` | Storage for repositories and data |
| `postgresql.enabled` | `true` | Use PostgreSQL backend |
| `postgresql-ha.enabled` | `false` | Don't use HA version (not needed for single-node) |

## Quick Start

### Prerequisites

- k3s cluster running
- Helm installed and configured
- cert-manager deployed (for HTTPS)
- DNS configured: `git.hatal.cc` points to your VPS IP

### 1. Add Gitea Helm Repository

```bash
helm repo add gitea-charts https://dl.gitea.io/charts
helm repo update
```

### 2. Install Gitea

```bash
helm install gitea gitea-charts/gitea \
  --namespace gitea \
  --create-namespace \
  -f helm/gitea/values.yaml
```

### 3. Wait for Deployment

```bash
# Check pod status
kubectl get pods -n gitea -w

# Wait for gitea pod to be ready
kubectl wait --for=condition=ready pod \
  -l app.kubernetes.io/name=gitea \
  -n gitea \
  --timeout=120s
```

### 4. Verify Installation

```bash
# Check all components are running
kubectl get pods -n gitea

# Check services
kubectl get svc -n gitea

# Check ingress and certificate
kubectl get ingress -n gitea
kubectl get certificate -n gitea
```

### 5. Access Gitea

Open browser to: `https://git.hatal.cc`

Login with:
- **Username**: `admin`
- **Password**: `lokoloko_karaoke`

## Docker Registry Access

Once Gitea is running, the Docker registry is automatically available.

### Login to Registry

```bash
# From your local machine
docker login git.hatal.cc:5000 -u admin -p lokoloko_karaoke

# Success message: Login Successful
```

### Push an Image

```bash
# Tag an image
docker tag myimage:latest git.hatal.cc:5000/admin/myimage:latest

# Push to registry
docker push git.hatal.cc:5000/admin/myimage:latest
```

### Pull an Image

```bash
# Pull from registry
docker pull git.hatal.cc:5000/admin/myimage:latest
```

## Kubernetes Integration

To use Gitea registry images in Kubernetes:

### 1. Create ImagePullSecret

```bash
kubectl create secret docker-registry gitea-registry \
  --docker-server=git.hatal.cc:5000 \
  --docker-username=admin \
  --docker-password=lokoloko_karaoke \
  --docker-email=admin@hatal.cc \
  -n karaoke
```

### 2. Reference in Pod Spec

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
  namespace: karaoke
spec:
  imagePullSecrets:
    - name: gitea-registry
  containers:
    - name: app
      image: git.hatal.cc:5000/admin/myimage:latest
```

## Redeployment

### Update Configuration

Edit `values.yaml` and redeploy:

```bash
helm upgrade gitea gitea-charts/gitea \
  --namespace gitea \
  -f helm/gitea/values.yaml
```

### Complete Redeployment

```bash
# 1. Delete existing deployment
helm uninstall gitea -n gitea

# 2. Delete PVCs (WARNING: This deletes data!)
kubectl delete pvc -n gitea --all

# 3. Delete namespace (optional)
kubectl delete namespace gitea

# 4. Redeploy
helm install gitea gitea-charts/gitea \
  --namespace gitea \
  --create-namespace \
  -f helm/gitea/values.yaml
```

## Storage Management

Gitea stores data in:
- **Git repositories**: PVC (20Gi by default)
- **PostgreSQL database**: PVC (managed by PostgreSQL chart)
- **SSH keys, avatars, etc.**: Same PVC as repositories

### Check Storage Usage

```bash
kubectl get pvc -n gitea

kubectl exec -it gitea-<pod-id> -n gitea -- du -sh /data
```

### Resize Storage

Edit `values.yaml` and change `persistence.size`:

```yaml
persistence:
  size: 50Gi  # Increased from 20Gi
```

Then upgrade:

```bash
helm upgrade gitea gitea-charts/gitea \
  --namespace gitea \
  -f helm/gitea/values.yaml
```

## Troubleshooting

### Pod not starting

```bash
# Check logs
kubectl logs -n gitea gitea-<pod-id>

# Check pod events
kubectl describe pod -n gitea gitea-<pod-id>
```

### HTTPS not working

```bash
# Check certificate
kubectl get certificate -n gitea
kubectl describe certificate -n gitea gitea-tls

# Check ingress
kubectl describe ingress -n gitea gitea
```

### Can't push images to registry

```bash
# Test registry connectivity
docker login git.hatal.cc:5000 -u admin -p lokoloko_karaoke

# Check if pod is running
kubectl get pods -n gitea

# Check logs
kubectl logs -n gitea gitea-<pod-id>
```

### Database connection issues

```bash
# Check PostgreSQL
kubectl logs -n gitea gitea-postgresql-0

# Check if database is accessible
kubectl exec -it gitea-<pod-id> -n gitea -- pg_isready -h gitea-postgresql -U gitea
```

## Security Notes

⚠️ **IMPORTANT**: The password in `values.yaml` is stored in Git. In production:

1. **Use Sealed Secrets or External Secrets** to manage sensitive data
2. **Rotate the admin password** after first login
3. **Create strong passwords** for production use
4. **Use SSH keys** instead of passwords for authentication
5. **Enable 2FA** for admin account
6. **Restrict repository access** with proper permissions

## Customization

To customize Gitea configuration, edit `values.yaml`:

- Change admin credentials
- Modify domain/URL
- Adjust storage size
- Configure PostgreSQL settings
- Enable/disable features

See [Gitea Helm Chart Documentation](https://gitea.com/gitea/helm-chart) for all available options.

## Quick Reference Commands

```bash
# Get Gitea status
helm status gitea -n gitea

# Get Gitea values
helm get values gitea -n gitea

# Edit values and upgrade
helm upgrade gitea gitea-charts/gitea \
  --namespace gitea \
  -f helm/gitea/values.yaml

# Get admin password
kubectl get secret -n gitea gitea -o jsonpath='{.data.admin-password}' | base64 -d

# Check registry endpoint
kubectl get svc -n gitea
```
