# Harbor Registry

Enterprise-grade container registry with vulnerability scanning and replication using the official Harbor Helm chart.

## Quick Start

```bash
# Update dependencies
helm dependency update ./helm/harbor

# Install
helm install harbor ./helm/harbor -n harbor --create-namespace

# Access via ingress
https://harbor.hatal.cc

# Default credentials
username: admin
password: Harbor12345
```

## Configuration

All values are passed through to the official Harbor chart. Key configurations in `values.yaml`:

- `harbor.externalURL` - External URL for Harbor (default: https://harbor.hatal.cc)
- `harbor.harborAdminPassword` - Admin password
- `harbor.persistence.persistentVolumeClaim.*.storageClass` - Storage class for volumes
- `harbor.expose.ingress.hosts.core` - Domain name

## Storage

Default storage allocation:
- Registry: 50Gi
- Database: 10Gi
- Job logs: 10Gi
- Redis: 5Gi
- Trivy: 5Gi

## Features

- Full-featured container registry
- Vulnerability scanning with Trivy
- Image replication
- RBAC and authentication
- HTTPS via Let's Encrypt certificate
- Built-in database and Redis

## References

- [Harbor GitHub](https://github.com/goharbor/harbor)
- [Harbor Official Helm Chart](https://github.com/goharbor/harbor-helm)
