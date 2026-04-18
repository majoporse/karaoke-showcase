# Cert-Manager Installation & Configuration

This directory contains the cert-manager setup for automated HTTPS certificate management using multiple ACME providers.

## Overview

**cert-manager** is a Kubernetes add-on that automates TLS certificate provisioning and renewal. It supports:
- **Let's Encrypt** - Free HTTPS certificates (production-ready)
- **ZeroSSL** - Free ACME certificates with EAB authentication
- **Traefik ingress controller** (bundled with k3s) to handle HTTPS termination
- Both issuers can coexist for redundancy and gradual migration

## Files

- **cert-manager.yaml**: ClusterIssuer configurations for both Let's Encrypt and ZeroSSL
- **zerossl-secret.yaml**: Kubernetes Secret containing ZeroSSL EAB HMAC key
- **usage.md**: Detailed deployment instructions

## Quick Start

### 1. Install Cert-Manager Helm Chart

```bash
# Add Helm repository
helm repo add jetstack https://charts.jetstack.io
helm repo update

# Install cert-manager (one-time, cluster-wide)
helm install cert-manager jetstack/cert-manager \
  --namespace cert-manager \
  --create-namespace \
  --version v1.14.1
```

### 2. Install CRDs (Custom Resource Definitions)

```bash
# Apply cert-manager CRDs
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.14.1/cert-manager.crds.yaml
```

### 3. Apply ClusterIssuer

```bash
# Apply the Let's Encrypt issuer configuration
kubectl apply -f helm/cert-manager/cert-manager.yaml
```

### 4. Verify Installation

```bash
# Check cert-manager is running
kubectl get pods -n cert-manager

# Check ClusterIssuer is ready
kubectl get clusterissuer
# Should show: letsencrypt-prod   True    <age>
```

## Configuration Details

### Available ClusterIssuers

You now have two issuers available:

#### 1. Let's Encrypt Production (`letsencrypt-prod`)

| Setting | Value | Purpose |
|---------|-------|---------|
| `name` | `letsencrypt-prod` | Issuer name for Ingress annotation |
| `server` | `acme-v02.api.letsencrypt.org` | Let's Encrypt production server |
| `email` | `admin@hatal.cc` | Email for Let's Encrypt notifications |
| `solvers[].http01` | `traefik` | HTTP-01 ACME challenge solver (via Traefik) |

**Use when**: You want free certificates with no additional setup or credentials

#### 2. ZeroSSL Production (`zerossl-prod`)

| Setting | Value | Purpose |
|---------|-------|---------|
| `name` | `zerossl-prod` | Issuer name for Ingress annotation |
| `server` | `acme.zerossl.com/v2/DV90` | ZeroSSL ACME server |
| `email` | `admin@hatal.cc` | Email for ZeroSSL account |
| `externalAccountBinding` | Configured via Secret | EAB credentials for authentication |
| `solvers[].http01` | `traefik` | HTTP-01 ACME challenge solver (via Traefik) |

**Use when**: You prefer ZeroSSL or need their specific features

### How It Works

1. **Ingress Creation**: When an Ingress with `cert-manager.io/cluster-issuer: <issuer-name>` is created
2. **Certificate Request**: cert-manager detects the annotation and requests a certificate from the specified issuer
3. **HTTP Challenge**: cert-manager creates a temporary HTTP endpoint to prove domain ownership
4. **Certificate Issued**: The ACME provider issues the certificate
5. **Secret Created**: cert-manager stores the certificate as a Kubernetes Secret
6. **Traefik Uses It**: Traefik ingress controller automatically uses the secret for HTTPS

### Using Different Issuers in Ingresses

**Example using Let's Encrypt:**
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod  # Use Let's Encrypt
spec:
  tls:
  - secretName: ingress-tls
    hosts:
    - example.com
```

**Example using ZeroSSL:**
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  annotations:
    cert-manager.io/cluster-issuer: zerossl-prod  # Use ZeroSSL
spec:
  tls:
  - secretName: ingress-tls-zerossl
    hosts:
    - example.com
```

## DNS Requirements

For cert-manager to work, your domain must:
- Be publicly accessible via DNS
- Resolve to your VPS IP address
- Have proper A records (e.g., `git.hatal.cc` → `91.98.139.195`)

## Troubleshooting

### Certificate not created
```bash
# Check cert-manager logs
kubectl logs -n cert-manager -l app=cert-manager --tail=100

# Check ClusterIssuer status (both issuers)
kubectl describe clusterissuer letsencrypt-prod
kubectl describe clusterissuer zerossl-prod

# Check Certificate resource
kubectl get certificate -A
kubectl describe certificate <name> -n <namespace>
```

### ACME challenge failing
```bash
# Check order and challenge status
kubectl get orders -A
kubectl describe order <name> -n <namespace>

# Check if ZeroSSL secret exists (if using zerossl-prod)
kubectl get secret -n cert-manager zerossl-eab-hmac
```

### Certificate stuck in pending
```bash
# Delete the certificate to retry
kubectl delete certificate -n <namespace> <cert-name>

# cert-manager will automatically recreate it
```

### ZeroSSL specific issues

**Secret not found error:**
```bash
# Ensure the Secret is created in cert-manager namespace
kubectl apply -f helm/cert-manager/zerossl-secret.yaml

# Verify the secret
kubectl get secret -n cert-manager zerossl-eab-hmac -o yaml
```

**EAB authentication failed:**
- Verify the EAB Key ID and HMAC key match your ZeroSSL account
- Check the Secret contains the correct base64-encoded HMAC key
- See the Secret management section below

## Secret Management

### ZeroSSL EAB Secret

The ZeroSSL issuer requires the EAB (External Account Binding) HMAC key stored as a Kubernetes Secret.

**Viewing the secret:**
```bash
kubectl get secret -n cert-manager zerossl-eab-hmac -o yaml
```

**Updating the secret** (if your EAB credentials change):
```bash
# 1. Update the base64-encoded value in zerossl-secret.yaml
# 2. Reapply the secret
kubectl apply -f helm/cert-manager/zerossl-secret.yaml

# 3. (Optional) Force cert-manager to refresh
kubectl delete secret -n cert-manager zerossl-prod-key  # Deletes the issuer's cache
```

## Certificate Renewal

Certificates are automatically renewed 30 days before expiration. You don't need to do anything.

## Updating Email

To change the notification email for either issuer:

```bash
# Edit the ClusterIssuer
kubectl edit clusterissuer letsencrypt-prod
# or
kubectl edit clusterissuer zerossl-prod

# Change the email field, then save
```

## Production Considerations

- **Rate Limiting**: Let's Encrypt has rate limits. Don't repeatedly delete/recreate certificates
- **Staging Server**: For testing, use `https://acme-staging-v02.api.letsencrypt.org/directory` instead
- **Multiple Domains**: One certificate can cover multiple domains (SANs)
- **Issuer Choice**: Start with Let's Encrypt (no credentials needed), migrate to ZeroSSL if needed

## Quick Reference Commands

```bash
# Get ClusterIssuer status (both issuers)
kubectl get clusterissuer
kubectl describe clusterissuer letsencrypt-prod
kubectl describe clusterissuer zerossl-prod

# Get all certificates
kubectl get certificate -A

# View cert-manager logs
kubectl logs -n cert-manager -l app=cert-manager -f

# Get certificate secret
kubectl get secret -n <namespace> <secret-name> -o yaml

# Check ZeroSSL EAB secret
kubectl get secret -n cert-manager zerossl-eab-hmac -o yaml

# Delete certificate (will be recreated)
kubectl delete certificate -n <namespace> <name>

# Verify HTTPS works
curl -v https://your-domain.com
```

## References

- [cert-manager Documentation](https://cert-manager.io/docs/)
- [Let's Encrypt](https://letsencrypt.org/)
- [Traefik Ingress](https://doc.traefik.io/traefik/routing/providers/kubernetes-crd/)
