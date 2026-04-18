# Headlamp - Lightweight Kubernetes UI

This chart deploys Headlamp, a modern and lightweight Kubernetes UI, using the official Headlamp Helm chart as a dependency.

## Quick Start

```bash
# Update dependencies
helm dependency update ./helm/headlamp

# Install
helm install headlamp ./helm/headlamp -n kube-system

# Access via ingress
https://dashboard.hatal.cc
```

## Features

- Lightweight, responsive Kubernetes UI
- In-cluster deployment for full cluster access
- HTTPS via Let's Encrypt certificate
- Read-only cluster access (can be configured for write permissions)
- Plugin system for extensibility

## Configuration

All values are passed through to the official Headlamp chart. See values.yaml for available options.

Key configurations:
- `headlamp.ingress.hosts[0].host` - Set the domain (default: dashboard.hatal.cc)
- `headlamp.replicaCount` - Number of replicas (default: 1)
- `headlamp.resources` - CPU/memory limits

## References

- [Headlamp GitHub](https://github.com/headlamp-k8s/headlamp)
- [Headlamp Official Helm Chart](https://github.com/kubernetes-sigs/headlamp/tree/main/charts/headlamp)
