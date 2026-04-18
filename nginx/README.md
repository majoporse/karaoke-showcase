# Nginx Configuration for Karaoke-Inator

This directory contains the nginx reverse proxy configuration for the Karaoke-Inator project.

## Overview

Nginx serves three key functions:
1. **Frontend Serving** - Serves React app as static files (SPA with client-side routing)
2. **API Proxy** - Proxies orchestrator API requests
3. **SSL/TLS Termination** - Handles HTTPS encryption for all traffic

## Features

- **HTTPS/SSL** - TLSv1.2 and TLSv1.3 support
- **SPA Routing** - Client-side routing works correctly (try_files fallback)
- **Rate Limiting** - 10 req/s general, 50 req/s for API
- **WebSocket Support** - Real-time connections supported
- **Security Headers** - HSTS, X-Frame-Options, CSP, etc.
- **Gzip Compression** - Reduces bandwidth usage
- **HTTP/2** - Better performance
- **Static Caching** - Browser caching for assets

## File Structure

```
nginx/
├── nginx.conf              # Configuration file
├── Dockerfile             # Alpine-based nginx image
├── generate-certs.sh      # SSL certificate generator
├── .gitignore             # Excludes ssl/ directory
├── ssl/                   # Generated certificates (git-ignored)
│   ├── cert.pem
│   └── key.pem
├── README.md              # This file
├── SETUP.md               # Setup instructions
├── CLIENT_CONFIGURATION.md # Code examples
└── CHECKLIST.md           # Verification checklist
```

## Quick Start

```bash
# 1. Generate certificates
cd nginx && ./generate-certs.sh && cd ..

# 2. Start services
docker-compose up --build

# 3. Access
https://localhost/
```

## Configuration Details

### Frontend Serving

Frontend static files are served from `/usr/share/nginx/html`:

```nginx
root /usr/share/nginx/html;
index index.html;

location / {
    try_files $uri $uri/ /index.html;  # SPA routing
    add_header Cache-Control "public, max-age=0, must-revalidate";
}
```

Files are mounted from the docker-compose volume:
```yaml
volumes:
  - ./services/frontend/build/client:/usr/share/nginx/html
```

### API Proxy

Only the orchestrator API is exposed externally:

```nginx
location /api/ {
    limit_req zone=api burst=30 nodelay;
    proxy_pass http://orchestrator/;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_set_header Upgrade $http_upgrade;      # WebSocket
    proxy_set_header Connection "upgrade";       # WebSocket
    proxy_read_timeout 300s;
}
```

All requests to `/api/*` are proxied internally to `http://orchestrator:8000/`.

### Health Check

```nginx
location /health {
    access_log off;
    proxy_pass http://orchestrator/health;
}
```

### Static Assets

```nginx
location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
    expires 30d;
    add_header Cache-Control "public, immutable";
}
```

### Rate Limiting

```nginx
limit_req_zone $binary_remote_addr zone=general:10m rate=10r/s;
limit_req_zone $binary_remote_addr zone=api:10m rate=50r/s;

location / {
    limit_req zone=general burst=20 nodelay;
}

location /api/ {
    limit_req zone=api burst=30 nodelay;
}
```

### SSL/TLS

```nginx
ssl_certificate /etc/nginx/ssl/cert.pem;
ssl_certificate_key /etc/nginx/ssl/key.pem;
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers HIGH:!aNULL:!MD5;
ssl_session_cache shared:SSL:10m;
ssl_session_timeout 10m;
```

### Security Headers

```nginx
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
```

### Gzip Compression

```nginx
gzip on;
gzip_vary on;
gzip_proxied any;
gzip_comp_level 6;
gzip_types text/plain text/css text/xml text/javascript 
            application/json application/javascript application/xml+rss;
```

## Routing

| Path | Destination | Purpose |
|------|-----------|---------|
| `/` | Static files | Frontend HTML, CSS, JS, assets |
| `/api/*` | Orchestrator (8000) | Backend API |
| `/health` | Orchestrator (8000) | Health check |
| `.*\.js, .*\.css, etc` | Static files | Cached assets |

## Frontend Configuration

Frontend should use relative API paths or `https://localhost/api/`:

```javascript
// Good - relative paths work
const API_URL = '/api';

// Or absolute
const API_URL = 'https://localhost/api';

// Frontend code
fetch(`${API_URL}/process`, { ... })
```

## Docker Integration

### Build Process

1. Frontend is built during docker-compose startup
2. Output goes to `./services/frontend/build/client/`
3. Nginx mounts these files via volume
4. Nginx serves them as static files

### Rebuilding Frontend

```bash
# Rebuild all including frontend
docker-compose up --build

# Or just frontend
cd services/frontend && npm run build && cd ../../
docker-compose restart nginx
```

## SSL Certificates

### Development (Self-Signed)

```bash
cd nginx
./generate-certs.sh          # Default: 365 days, US, California
./generate-certs.sh 730      # Custom days
./generate-certs.sh 365 "US" "NY" "New York" "Company"
cd ..
```

### Production (Let's Encrypt)

```bash
# Get certificates
certbot certonly --webroot -w /etc/nginx/html \
  -d your-domain.com \
  -d www.your-domain.com

# Copy to nginx/ssl/
sudo cp /etc/letsencrypt/live/your-domain.com/fullchain.pem nginx/ssl/cert.pem
sudo cp /etc/letsencrypt/live/your-domain.com/privkey.pem nginx/ssl/key.pem

# Restart nginx
docker-compose restart nginx
```

## Common Issues

### Frontend not showing

- Check files exist: `ls services/frontend/build/client/`
- Rebuild: `docker-compose up --build`
- Check logs: `docker logs karaoke-nginx`

### API calls failing

- Check orchestrator is healthy: `docker-compose ps`
- Test health: `curl -k https://localhost/health`
- View logs: `docker logs karaoke-orchestrator`

### SSL certificate errors

- Generate certs: `cd nginx && ./generate-certs.sh && cd ..`
- Verify files: `ls -la nginx/ssl/`
- Restart: `docker-compose restart nginx`

### Port already in use

```bash
docker-compose down
lsof -i :80
lsof -i :443
# Kill process if needed
```

## Performance Tuning

### Increase Worker Connections

```nginx
events {
    worker_connections 2048;  # Default 1024
}
```

### Adjust Rate Limiting

```nginx
limit_req_zone $binary_remote_addr zone=api:10m rate=100r/s;  # More permissive
```

### Disable Gzip (if CPU-bound)

```nginx
gzip off;
```

### Enable Caching

Already configured - static assets cached 30 days.

## Monitoring

### View Logs

```bash
docker logs karaoke-nginx              # Recent logs
docker logs -f karaoke-nginx           # Follow in real-time
docker logs --tail 50 karaoke-nginx    # Last 50 lines
```

### Check Health

```bash
docker-compose ps                      # All container status
curl -k https://localhost/health       # API health check
```

### Monitor Resources

```bash
docker stats karaoke-nginx
```

## Troubleshooting Commands

```bash
# Check nginx config validity
docker exec karaoke-nginx nginx -t

# View running config
docker exec karaoke-nginx nginx -T

# Check if listening on ports
docker exec karaoke-nginx netstat -tlnp

# Test upstream connectivity
docker exec karaoke-nginx curl http://orchestrator:8000/health
```

## Advanced Configuration

### Add Custom Location

Edit `nginx.conf` and add:

```nginx
location /custom {
    proxy_pass http://some-service:port;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
}
```

Then restart:
```bash
docker-compose up -d --build nginx
```

### Restrict IP Access

```nginx
location /api/admin {
    allow 192.168.1.0/24;
    deny all;
}
```

### Enable CORS Headers

```nginx
add_header Access-Control-Allow-Origin "*" always;
add_header Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS" always;
add_header Access-Control-Allow-Headers "Content-Type" always;

if ($request_method = 'OPTIONS') {
    return 204;
}
```

## Production Deployment

- [ ] Replace self-signed certs with production certificates
- [ ] Update domain name in nginx.conf
- [ ] Configure rate limits for your traffic
- [ ] Enable and monitor access logs
- [ ] Set up SSL certificate renewal (for Let's Encrypt)
- [ ] Configure firewall (allow only 80, 443)
- [ ] Test all endpoints
- [ ] Set up monitoring/alerting

## Support & Documentation

- **SETUP.md** - Step-by-step setup guide (start here!)
- **CHECKLIST.md** - Verification checklist
- **CLIENT_CONFIGURATION.md** - Frontend/backend code examples
- **nginx.conf** - Full configuration file with comments

## External Resources

- [Nginx Official Documentation](http://nginx.org/en/docs/)
- [Let's Encrypt](https://letsencrypt.org/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
