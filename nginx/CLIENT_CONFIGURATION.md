# Nginx Configuration - Environment & Client Updates

This document explains how to update your application code to work with the new nginx setup.

## Frontend Configuration

### Environment Variables

Create or update `.env` in `services/frontend/`:

```env
# API Configuration
VITE_API_BASE_URL=https://localhost/api/orchestrator
VITE_MINIO_API_URL=https://localhost/minio-api
VITE_MINIO_CONSOLE_URL=https://localhost/minio-console

# In development, you may need to disable SSL verification:
# NODE_TLS_REJECT_UNAUTHORIZED=0

# Other configs
VITE_APP_NAME=Karaoke-Inator
VITE_ENVIRONMENT=development
```

### JavaScript/TypeScript Example

```typescript
// services/api.ts
const API_BASE = import.meta.env.VITE_API_BASE_URL || 'https://localhost/api/orchestrator';

export async function processYoutubeUrl(url: string) {
  const response = await fetch(`${API_BASE}/process`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ youtube_url: url })
  });
  return response.json();
}

// For development with self-signed certs:
export const fetchWithSslBypass = (url: string, options: RequestInit = {}) => {
  // Note: This only works in Node.js environments, not in browsers
  // Browsers will show SSL warning - user must click "Advanced" -> "Proceed"
  return fetch(url, options);
};
```

### React Example

```tsx
// hooks/useApi.ts
import { useCallback } from 'react';

const API_BASE = import.meta.env.VITE_API_BASE_URL;

export function useApi() {
  const request = useCallback(async (endpoint: string, options: RequestInit = {}) => {
    const url = `${API_BASE}${endpoint}`;
    
    try {
      const response = await fetch(url, {
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
        },
        ...options,
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error(`API request failed to ${url}:`, error);
      throw error;
    }
  }, []);

  return {
    processVideo: (url: string) => request('/process', {
      method: 'POST',
      body: JSON.stringify({ youtube_url: url }),
    }),
    getHealth: () => request('/health'),
    searchSongs: (query: string) => request(`/search?q=${encodeURIComponent(query)}`),
  };
}
```

### Vue Example

```vue
<!-- services/api.ts -->
<script setup lang="ts">
const API_BASE = import.meta.env.VITE_API_BASE_URL;

async function processVideo(youtubeUrl: string) {
  const response = await fetch(`${API_BASE}/process`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ youtube_url: youtubeUrl })
  });
  return response.json();
}
</script>
```

## Backend Configuration

### Python (FastAPI/Requests)

```python
# config.py
import os
from typing import Optional

class Config:
    # Nginx-based URLs (with SSL)
    ORCHESTRATOR_URL = os.getenv(
        'ORCHESTRATOR_URL',
        'https://localhost/api/orchestrator'
    )
    VOICE_SEPARATION_URL = os.getenv(
        'VOICE_SEPARATION_URL',
        'https://localhost/api/voice-separation'
    )
    LYRICS_EXTRACTION_URL = os.getenv(
        'LYRICS_EXTRACTION_URL',
        'https://localhost/api/lyrics-extraction'
    )
    
    # SSL verification (disable for development with self-signed certs)
    VERIFY_SSL = os.getenv('VERIFY_SSL', 'false').lower() == 'true'

# Usage in your service
# services/client.py
import requests
from urllib3.exceptions import InsecureRequestWarning
from config import Config

if not Config.VERIFY_SSL:
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def call_orchestrator(endpoint: str, **kwargs):
    url = f"{Config.ORCHESTRATOR_URL}{endpoint}"
    response = requests.get(
        url,
        verify=Config.VERIFY_SSL,
        **kwargs
    )
    return response.json()
```

### Node.js/Express

```javascript
// config.js
module.exports = {
  // Nginx-based URLs
  ORCHESTRATOR_URL: process.env.ORCHESTRATOR_URL || 'https://localhost/api/orchestrator',
  VOICE_SEPARATION_URL: process.env.VOICE_SEPARATION_URL || 'https://localhost/api/voice-separation',
  LYRICS_EXTRACTION_URL: process.env.LYRICS_EXTRACTION_URL || 'https://localhost/api/lyrics-extraction',
  
  // SSL verification
  VERIFY_SSL: process.env.VERIFY_SSL === 'true' ? true : false,
};

// client.js
const https = require('https');
const config = require('./config');

// For development with self-signed certificates
const agent = config.VERIFY_SSL 
  ? new https.Agent() 
  : new https.Agent({ rejectUnauthorized: false });

async function callOrchestrator(endpoint, options = {}) {
  const url = new URL(config.ORCHESTRATOR_URL + endpoint);
  
  return new Promise((resolve, reject) => {
    https.get(url, { agent }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => resolve(JSON.parse(data)));
    }).on('error', reject);
  });
}
```

## Environment Variables for docker-compose

When running with docker-compose, services communicate internally using the Docker network. You generally don't need to change these, but they're shown for reference:

```yaml
# docker-compose.yml - Internal Service URLs (unchanged)
services:
  orchestrator:
    environment:
      - VOICE_SEPARATION_URL=http://voice-separation:8001
      - LYRICS_EXTRACTION_URL=http://lyrics-extraction:8002
      - REDIS_URL=redis://redis:6379/0

  rq-worker:
    environment:
      - VOICE_SEPARATION_URL=http://voice-separation:8001
      - LYRICS_EXTRACTION_URL=http://lyrics-extraction:8002
      - REDIS_URL=redis://redis:6379/0
```

**Note:** Services use HTTP internally (no SSL) because they communicate through a private Docker network. Only external clients use HTTPS through nginx.

## Testing Configuration

### cURL Examples

```bash
# Test with self-signed certificate bypass
curl -k https://localhost/health

# Test with custom headers
curl -k -H "Content-Type: application/json" \
  -d '{"youtube_url":"https://..."}' \
  https://localhost/api/orchestrator/process

# Get verbose output (including headers)
curl -k -v https://localhost/health
```

### Postman Configuration

1. **Base URL:** `https://localhost`
2. **Disable SSL verification:**
   - Settings → SSL certificate verification → OFF
3. **Add API requests:**
   - `GET` → `{{base_url}}/health`
   - `POST` → `{{base_url}}/api/orchestrator/process`

### Python Testing

```python
import requests
from urllib3.exceptions import InsecureRequestWarning

# Disable SSL warnings for development
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Test health
response = requests.get('https://localhost/health', verify=False)
print(response.json())

# Test process
response = requests.post(
    'https://localhost/api/orchestrator/process',
    json={'youtube_url': 'https://www.youtube.com/watch?v=...'},
    verify=False
)
print(response.json())
```

## Browser HTTPS Warnings

When accessing `https://localhost` in your browser with self-signed certificates:

1. You'll see "Your connection is not private" warning
2. Click **Advanced** → **Proceed to localhost (unsafe)**
3. The browser will cache this decision

**For production:** Use certificates from a trusted CA (Let's Encrypt recommended).

## CORS Configuration

If your frontend is on a different port/domain, you may need CORS headers. Add to `nginx/nginx.conf`:

```nginx
location /api/orchestrator/ {
    # ... existing config ...
    
    # Add CORS headers if needed
    add_header Access-Control-Allow-Origin "https://your-domain.com";
    add_header Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS";
    add_header Access-Control-Allow-Headers "Content-Type, Authorization";
    
    if ($request_method = 'OPTIONS') {
        return 204;
    }
}
```

## MinIO Configuration

For MinIO bucket access through the nginx proxy:

```python
# services/minio_client.py
from minio import Minio

client = Minio(
    endpoint="localhost/minio-api",  # Through nginx
    access_key="minioadmin",
    secret_key="minioadmin",
    secure=True,  # Use HTTPS
)

# Or internally within Docker:
client_internal = Minio(
    endpoint="minio:9000",  # Internal Docker network
    access_key="minioadmin",
    secret_key="minioadmin",
    secure=False,  # HTTP is fine internally
)
```

## Development Tips

### Skip SSL in Development

**Python environment variable:**
```bash
export VERIFY_SSL=false
```

**Node.js environment variable:**
```bash
export VERIFY_SSL=false
```

### Docker Compose Override

Create `docker-compose.override.yml` for local development:

```yaml
services:
  frontend:
    environment:
      - VITE_API_BASE_URL=https://localhost/api/orchestrator
      - VITE_SKIP_SSL_VERIFY=true
  
  orchestrator:
    environment:
      - VERIFY_SSL=false
```

### Local SSL Certificate Bypass

For testing without browser warnings, use:

```python
# Python: Use requests-unixsocket or similar
import os
os.environ['PYTHONHTTPSVERIFY'] = '0'
```

```javascript
// Node.js: Set this early in your app
process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';
```

## Summary

| Layer | Old URL | New URL | Protocol |
|-------|---------|---------|----------|
| External Client | `http://localhost:8000` | `https://localhost/api/orchestrator` | HTTPS |
| Frontend | `http://localhost:5173` | `https://localhost/` | HTTPS |
| Internal (Docker) | `http://orchestrator:8000` | `http://orchestrator:8000` | HTTP (unchanged) |

External clients always use HTTPS through nginx. Internal Docker services still use HTTP over the private network for efficiency.
