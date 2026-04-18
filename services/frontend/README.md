# 🎹 Frontend Service

The web interface for Karaoke-Inator—a modern React application where users submit YouTube URLs, track processing progress in real-time, and enjoy interactive karaoke playback with synchronized lyrics.

## Overview

The frontend provides a complete user experience for the karaoke processing system. Built with React Router 7 for modern file-based routing and React Query for server state management, it delivers a responsive, real-time interface for audio processing and playback.

## Key Features

### 🎯 Create & Process Songs
- Submit YouTube URLs for karaoke processing
- Real-time progress tracking via WebSocket
- Visual queue position indicators
- Error handling and retry mechanisms
- Job persistence across browser refreshes

### 🔍 Search & Discovery
- Full-text search across processed songs
- Filter by artist, album, year
- Infinite scroll pagination
- Responsive grid layout
- Quick access to song details

### 🎵 Interactive Karaoke Player
- Dual-track audio playback (vocals + accompaniment)
- Independent volume controls for each track
- Real-time synchronized lyrics display
- Clickable lyrics for seeking to specific moments
- Keyboard shortcuts for playback control
- Manual/auto-sync toggle for lyrics

### 📊 Job Queue Management
- Live view of processing queue
- Job status tracking (queued, processing, completed, failed)
- Estimated time remaining
- Historical job list

### 🎨 User Interface
- Responsive design (mobile, tablet, desktop)
- Dark/light theme toggle
- Accessibility-first component design
- Loading states and skeleton screens

## Technology Stack

| Technology | Purpose |
|-----------|---------|
| **React 19** | UI component framework |
| **React Router 7** | File-based routing and navigation |
| **React Query** | Server state management and caching |
| **TypeScript 5.9** | Type-safe JavaScript |
| **Tailwind CSS 4** | Utility-first styling |
| **Vite 7** | Lightning-fast build tool |
| **Radix UI** | Accessible UI component library |
| **PartySocket** | WebSocket client with auto-reconnect |
| **MinIO SDK** | Direct S3 object storage access |
| **Axios** | HTTP client |
| **OpenAPI Generator** | Auto-generated API clients |

## Architecture

### Page Structure (React Router)

```
app/routes/
├── _app.tsx                      # Root layout
├── _index.tsx                    # Home page
├── create.search.tsx             # Create/process page
├── search.tsx                    # Browse/search page
└── songs.$id.tsx                 # Song detail & player
```

### Component Organization

```
app/components/
├── KaraokePlayer.tsx             # Main player component
├── LyricsDisplay.tsx             # Synchronized lyrics
├── SongCard.tsx                  # Song preview card
├── SearchBar.tsx                 # Search interface
├── JobQueue.tsx                  # Queue status
├── AudioControls.tsx             # Playback controls
└── ThemeToggle.tsx               # Dark/light mode
```

### State Management

- **Server State**: React Query handles API data, caching, and synchronization
- **UI State**: React Context for theme and user preferences
- **Real-time Updates**: WebSocket connection for job progress
- **Form State**: React Router form submission for URL input

## Pages Overview

### Home Page (`_index.tsx`)
- Project introduction and feature highlights
- Quick links to main features
- Recent/featured songs
- Call-to-action to create new song

### Create Song Page (`create.search.tsx`)
- YouTube URL input form
- Real-time job progress display
- Queue position tracking
- Processing time estimates
- Link to view completed song once ready

### Search Page (`search.tsx`)
- Search bar with typeahead
- Filter options (artist, album, year, quality)
- Infinite scroll song grid
- Sort options (newest, most popular, A-Z)
- Direct access to player from results

### Song Detail & Player (`songs.$id.tsx`)
- Full karaoke player with audio controls
- Synchronized lyrics display with auto-scroll
- Dual-track volume controls (vocals/accompaniment)
- Song metadata (title, artist, duration)
- Download options for separated audio
- Related songs recommendation

## Real-time Features

### WebSocket Connection
The frontend establishes a persistent WebSocket connection to the orchestrator for live updates:

```typescript
// Real-time job progress
ws.onmessage = (event) => {
  const update = JSON.parse(event.data);
  // { jobId, status, progress, eta, message }
  setJobStatus(update);
};
```

**Events received:**
- Job queued
- Processing started (voice/lyrics)
- Progress percentage
- Completion with results
- Errors with retry suggestions

### Auto-sync Lyrics
As audio plays, the lyrics component automatically scrolls to display the current line being sung. Word-level timing enables precise synchronization.

## Development Setup

### Prerequisites
- Node.js 18+
- npm or yarn

### Installation & Running

```bash
# Install dependencies
npm install

# Development server (hot reload)
cp .env.example .env
npm run dev

# Type checking
npm run typecheck

# Linting & formatting
npm run lint
npm run lint:fix
npm run format

# Production build
npm run build

# Preview production build locally
npm run preview
```

**Development server runs on**: http://localhost:5173

### Code Generation

The frontend auto-generates API clients from OpenAPI specs:

```bash
# Generate orchestrator API client
npm run client-gen

# Generate WebSocket AsyncAPI models
npm run asyncapi-gen
```

These commands create type-safe clients in the `clients/` directory, ensuring frontend requests always match backend contracts.

## API Integration

### Orchestrator Service Connection
All API calls go through the Orchestrator (port 8000), which coordinates the other services:

```typescript
// Example: Create a karaoke job
const createJob = async (youtubeUrl: string) => {
  const response = await apiClient.post('/api/process', {
    youtube_url: youtubeUrl
  });
  return response.data;
};
```

### Key Endpoints Used
- `POST /api/process` - Submit song for processing
- `GET /api/jobs/{id}` - Get job status
- `GET /api/songs` - Search songs
- `GET /api/songs/{id}` - Get song details
- `WS /ws/progress` - WebSocket progress updates
- `GET /api/download/{id}` - Download separated audio

## Performance Optimizations

### Code Splitting
React Router automatically code-splits per-route, loading only necessary JavaScript for each page.

### Image Optimization
Album art and thumbnails are lazy-loaded with blur-up placeholders.

### Caching Strategy
React Query caches:
- Song search results (5 minute stale time)
- Job status (30 second stale time)
- Song details (15 minute stale time)

### Network Efficiency
- Pagination limits API response size
- Infinite scroll loads data as needed
- WebSocket reduces polling overhead
- Browser caching for static assets

## Styling Approach

### Tailwind CSS

**Customization** in `tailwind.config.ts`:
- Brand colors and theme
- Custom spacing and typography
- Dark mode support
- Responsive breakpoints


## Deployment

### Production Build
```bash
npm run build     # Creates optimized dist/ folder
```

### Docker Deployment
The frontend is containerized with Node.js 20 Alpine:
- Multi-stage build (dependencies, source, production)
- Lightweight final image
- Health checks via `/health` endpoint
- Served via Nginx in production

### Environment Variables
Configure via `.env` file:
```
VITE_ORCHESTRATOR_URL=http://orchestrator:8000
VITE_MINIO_ENDPOINT=minio:9000
VITE_MINIO_REGION=us-east-1
```

## Troubleshooting

### WebSocket Connection Issues
If real-time updates aren't working:
1. Check browser DevTools Network tab for `/ws/progress`
2. Verify Orchestrator service is running
3. Check browser console for connection errors
4. Ensure firewall allows WebSocket

### Search Not Working
1. Verify Orchestrator is running
2. Check Elasticsearch is accessible
3. Ensure songs have been processed and indexed
4. Check browser DevTools Network tab

### Audio Playback Issues
1. Check browser allows audio playback (autoplay policy)
2. Verify audio files exist in MinIO
3. Check browser console for CORS errors
4. Ensure audio codec is supported (MP3, WAV, OGG)

---

**For system-wide architecture details**, see the main [README.md](../README.md) or [BLOG.md](../BLOG.md).

**For orchestrator/API details**, check [orchestrator-service/README.md](../orchestrator-service/README.md).
