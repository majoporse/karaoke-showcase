# Cert-Manager Deployment Guide

## Prerequisites

- k3s cluster running (includes Traefik ingress controller)
- `kubectl` and `helm` configured
- Domain pointing to your VPS IP (e.g., `hatal.cc` → `91.98.139.195`)
- (Optional) ZeroSSL account with EAB credentials for `zerossl-prod` issuer

## Installation Steps

### Step 1: Add Helm Repository

```bash
helm repo add jetstack https://charts.jetstack.io
helm repo update
```

### Step 2: Install CRDs

```bash
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.14.1/cert-manager.crds.yaml
```

### Step 3: Install Cert-Manager via Helm

```bash
helm install cert-manager jetstack/cert-manager \
  --namespace cert-manager \
  --create-namespace \
  --version v1.14.1
```

### Step 4: Wait for Cert-Manager to be Ready

```bash
kubectl wait --for=condition=ready pod \
  -l app.kubernetes.io/instance=cert-manager \
  -n cert-manager \
  --timeout=120s
```

### Step 5: Apply ZeroSSL Secret (Optional)

If you plan to use the ZeroSSL issuer with EAB credentials:

```bash
# Apply the ZeroSSL EAB HMAC secret
kubectl apply -f helm/cert-manager/zerossl-secret.yaml
```

Skip this step if you only plan to use Let's Encrypt.

### Step 6: Apply ClusterIssuer

```bash
# Apply both Let's Encrypt and ZeroSSL ClusterIssuers
kubectl apply -f helm/cert-manager/cert-manager.yaml
```

### Step 6: Verify Installation

```bash
# Check all cert-manager pods are running
kubectl get pods -n cert-manager

# Check both ClusterIssuers are ready
kubectl get clusterissuer
```

Expected output:
```
NAME                 READY   STATUS    RESTARTS   AGE
cert-manager-...     1/1     Running   0          2m
cert-manager-webhook-...  1/1     Running   0          2m
cert-manager-cainjector-... 1/1     Running   0          2m

NAME                 READY   AGE
letsencrypt-prod     True    30s
zerossl-prod         True    30s
```

If `zerossl-prod` shows `False`, verify the ZeroSSL secret was applied:
```bash
kubectl get secret -n cert-manager zerossl-eab-hmac
```

## Redeployment

To redeploy everything (in case of disaster recovery):

```bash
# 1. Delete existing cert-manager
helm uninstall cert-manager -n cert-manager

# 2. Delete namespace (optional, but recommended)
kubectl delete namespace cert-manager

# 3. Repeat steps 1-6 above
```

## Testing Certificate Creation

Once deployed, certificates are automatically created when you deploy an Ingress with either issuer:

**Using Let's Encrypt:**
```yaml
annotations:
  cert-manager.io/cluster-issuer: "letsencrypt-prod"
tls:
  - secretName: my-cert
    hosts:
      - example.com
```

**Using ZeroSSL:**
```yaml
annotations:
  cert-manager.io/cluster-issuer: "zerossl-prod"
tls:
  - secretName: my-cert-zerossl
    hosts:
      - example.com
```

Check certificate status:

```bash
# List all certificates
kubectl get certificate -A

# Get details of a specific certificate
kubectl describe certificate <name> -n <namespace>

# Watch certificate creation in real-time
kubectl get certificate -n <namespace> -w
```

## Important Notes

- **Email**: Change `admin@hatal.cc` in `cert-manager.yaml` to your email (used by both issuers)
- **Domain**: Ensure DNS is properly configured before applying ClusterIssuers
- **Traefik**: k3s includes Traefik by default, which handles HTTPS termination
- **Reapply**: You can safely reapply the YAML files multiple times (idempotent)
- **Issuer Choice**: Use `letsencrypt-prod` by default; use `zerossl-prod` if you need ZeroSSL certificates
- **ZeroSSL Secret**: Only required if using the `zerossl-prod` issuer

## Quick Reference Commands

```bash
# Get ClusterIssuer status
kubectl get clusterissuer
kubectl describe clusterissuer letsencrypt-prod

# Get all certificates
kubectl get certificate -A

# View cert-manager logs
kubectl logs -n cert-manager -l app=cert-manager -f

# Get certificate secret
kubectl get secret -n <namespace> <secret-name> -o yaml

# Delete certificate (will be recreated)
kubectl delete certificate -n <namespace> <name>

# Verify HTTPS works
curl -v https://your-domain.com
```
