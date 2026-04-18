# Nginx Setup Checklist

Use this checklist to ensure your nginx SSL setup is complete and working correctly.

## Pre-Setup

- [ ] Reviewed `NGINX_SETUP_SUMMARY.md`
- [ ] Read `nginx/README.md` for configuration details
- [ ] Verified nginx folder exists: `ls nginx/`
- [ ] Docker and Docker Compose are installed

## Certificate Generation

- [ ] Generated SSL certificates: `cd nginx && ./generate-certs.sh && cd ..`
- [ ] Certificates exist: `ls -la nginx/ssl/` (should show `cert.pem` and `key.pem`)
- [ ] `.gitignore` in nginx folder excludes `ssl/`

## Docker Compose Updates

- [ ] Reviewed updated `docker-compose.yml`
- [ ] Nginx service is present
- [ ] Port mappings removed from individual services:
  - [ ] voice-separation: no ports
  - [ ] lyrics-extraction: no ports
  - [ ] orchestrator: no ports
  - [ ] frontend: no ports
  - [ ] minio: no ports
- [ ] Nginx depends on all main services
- [ ] docker-compose is valid: `docker-compose config` (no errors)

## First Run

- [ ] Run: `docker-compose up --build`
- [ ] All services show "healthy" in `docker-compose ps`
- [ ] No errors in nginx logs: `docker logs karaoke-nginx`

## Access Testing

### HTTPS Endpoints
- [ ] Frontend: `https://localhost/` (browser - ignore SSL warning)
- [ ] Health check: `curl -k https://localhost/health`
- [ ] Orchestrator: `https://localhost/api/orchestrator/health`
- [ ] MinIO Console: `https://localhost/minio-console/`

### From CLI
```bash
# All should return 200 or JSON response
curl -k https://localhost/health
curl -k https://localhost/api/orchestrator/health
curl -k https://localhost/api/voice-separation/health
curl -k https://localhost/api/lyrics-extraction/health
```

## Application Updates

### Frontend
- [ ] Environment variables updated:
  - [ ] `VITE_API_BASE_URL=https://localhost/api/orchestrator`
  - [ ] API calls use HTTPS
- [ ] Removed references to individual service ports
- [ ] Frontend builds successfully

### Backend (if applicable)
- [ ] Updated service URLs to use HTTPS through nginx
- [ ] SSL verification disabled for development (if needed)
- [ ] All internal Docker communication still uses HTTP
- [ ] Example: `ORCHESTRATOR_URL=https://localhost/api/orchestrator`

## Documentation Review

- [ ] Read `nginx/SETUP.md` for detailed setup instructions
- [ ] Read `nginx/CLIENT_CONFIGURATION.md` for code examples
- [ ] Reviewed rate limiting configuration in `nginx/nginx.conf`
- [ ] Understood WebSocket support configuration

## Docker Cleanup & Rebuild

- [ ] Stopped existing containers: `docker-compose down`
- [ ] Removed old images if needed: `docker image prune`
- [ ] Built fresh: `docker-compose up --build`
- [ ] All services start in correct order

## Production Preparation

- [ ] [ ] Certificate strategy planned (Let's Encrypt for prod)
- [ ] [ ] Rate limiting reviewed and adjusted if needed
- [ ] [ ] Security headers understood
- [ ] [ ] CORS configuration reviewed (if needed)
- [ ] [ ] Logging and monitoring strategy planned
- [ ] [ ] SSL renewal strategy planned (for Let's Encrypt)

## Monitoring & Logs

- [ ] View nginx logs: `docker logs karaoke-nginx`
- [ ] Follow logs: `docker logs -f karaoke-nginx`
- [ ] Check service health: `docker-compose ps`
- [ ] Verify upstreams responding: `docker exec karaoke-nginx curl http://orchestrator:8000/health`

## Troubleshooting Steps

If something doesn't work:

- [ ] Run `docker-compose ps` to check service health
- [ ] Check nginx logs: `docker logs karaoke-nginx`
- [ ] Verify SSL certs exist: `ls -la nginx/ssl/`
- [ ] Verify nginx config: `docker-compose config`
- [ ] Check individual service logs for errors
- [ ] Wait 30-60 seconds (services take time to start)
- [ ] Review `nginx/SETUP.md` troubleshooting section

## Verification Checklist - Complete

### Services Online
- [ ] nginx: healthy
- [ ] orchestrator: healthy
- [ ] frontend: healthy
- [ ] voice-separation: healthy
- [ ] lyrics-extraction: healthy
- [ ] minio: healthy
- [ ] redis: healthy
- [ ] postgres: healthy

### Network Access
- [ ] External (HTTPS through nginx):
  - [ ] https://localhost/ (frontend)
  - [ ] https://localhost/health (orchestrator)
  - [ ] https://localhost/api/orchestrator/ (orchestrator API)
  - [ ] https://localhost/minio-console/ (MinIO)

- [ ] Internal (HTTP within Docker):
  - [ ] Services communicate correctly
  - [ ] No SSL errors in service-to-service communication

### Configuration
- [ ] Rate limiting enabled
- [ ] WebSocket support enabled
- [ ] Security headers present
- [ ] Gzip compression enabled
- [ ] SSL/TLS properly configured

## Success Criteria

Your setup is successful when:

✅ All services show "healthy" in `docker-compose ps`
✅ `https://localhost/health` returns 200
✅ Frontend loads at `https://localhost/`
✅ Browser shows SSL warning (expected with self-signed cert)
✅ All API endpoints accessible through nginx
✅ No errors in `docker logs karaoke-nginx`
✅ Internal service communication works

## Next Steps After Setup

1. **Development**
   - [ ] Update frontend/backend code to use new URLs
   - [ ] Test all features through HTTPS
   - [ ] Verify rate limiting doesn't interfere
   - [ ] Test with actual YouTube videos

2. **Production Planning**
   - [ ] Plan certificate migration to Let's Encrypt
   - [ ] Set up domain name (instead of localhost)
   - [ ] Configure firewall rules
   - [ ] Plan monitoring and alerting
   - [ ] Document deployment procedures

3. **Team Documentation**
   - [ ] Share setup instructions with team
   - [ ] Document new API URLs
   - [ ] Create runbooks for troubleshooting
   - [ ] Update architecture documentation

## Support Resources

- `NGINX_SETUP_SUMMARY.md` - Quick overview
- `nginx/README.md` - Detailed configuration reference
- `nginx/SETUP.md` - Step-by-step instructions
- `nginx/CLIENT_CONFIGURATION.md` - Code examples
- `nginx/nginx.conf` - Full configuration file

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| SSL certs not found | `cd nginx && ./generate-certs.sh && cd ..` |
| Port already in use | `docker-compose down` & `lsof -i :80` |
| Services unhealthy | `docker logs <service>` & wait 30-60s |
| Nginx won't start | Check logs: `docker logs karaoke-nginx` |
| Browser SSL warning | Expected - click Advanced → Proceed |
| API connection refused | Verify services in `docker-compose ps` |
| WebSocket connection failed | Check `docker logs karaoke-nginx` |

---

**Setup completed successfully!** 🎉

Remember to generate certificates and start services:
```bash
cd nginx && ./generate-certs.sh && cd ..
docker-compose up --build
```

Access at: **https://localhost/**
