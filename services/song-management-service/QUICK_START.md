# Quick Start: Multi-Search Implementation

## 🚀 Get Started in 5 Minutes

### 1. Apply Database Migration (30 seconds)

```bash
cd song-management-service
source .venv/bin/activate
alembic upgrade head
```

**Verify:**
```bash
psql $DATABASE_URL -c "SELECT title, creator FROM processing_results LIMIT 1;"
```

### 2. Test Search Endpoint (1 minute)

```bash
# Basic search
curl "http://localhost:8000/lyrics/search/all?query=imagine"

# With language filter
curl "http://localhost:8000/lyrics/search/all?query=hola&language=es"
```

**Expected:** JSON array of lyrics matching your search

### 3. Verify Elasticsearch (1 minute)

```bash
# Check Elasticsearch is running
curl http://localhost:9200/

# Count indexed lyrics
curl "http://localhost:9200/lyrics/_count"

# Test a search query
curl -X GET "http://localhost:9200/lyrics/_search" \
  -H 'Content-Type: application/json' \
  -d '{"query": {"match_all": {}}}'
```

### 4. Review Implementation (2 minutes)

```bash
# Read summary
cat IMPLEMENTATION_SUMMARY.md

# Read examples
cat ELASTICSEARCH_SEARCH_EXAMPLES.md
```

---

## 📋 What Changed

### New Fields in ProcessingResult
- `title` - Song title from YouTube
- `creator` - Artist/Creator from YouTube  
- `duration_seconds` - Duration in seconds
- `thumbnail_url` - Thumbnail URL

### New Search Endpoint
- **Path:** `GET /lyrics/search/all`
- **Parameters:** `query` (required), `language` (optional)
- **Response:** `List[LyricsSearchResponse]`

### Smart Search Features
- ✅ Full text search (complete lyrics)
- ✅ Chunk search (specific lines)
- ✅ Fuzzy matching (typo tolerance)
- ✅ Language filtering
- ✅ No data duplication

---

## 🎯 Usage Examples

### Python Client

```python
from services.lyrics_service import LyricsService

# Search lyrics
results = await lyrics_service.search_lyrics("hello world")

# With language filter
results = await lyrics_service.search_lyrics("hola", language="es")

# Iterate results
for lyrics in results:
    print(f"ID: {lyrics.id}")
    print(f"Text: {lyrics.full_text}")
    for chunk in lyrics.chunks:
        print(f"  [{chunk.start}s] {chunk.text}")
```

### cURL

```bash
# Search
curl "http://localhost:8000/lyrics/search/all?query=love"

# Language filter
curl "http://localhost:8000/lyrics/search/all?query=amor&language=es"

# Multiple words
curl "http://localhost:8000/lyrics/search/all?query=yesterday%20never"
```

---

## 📊 Architecture

```
Search Request
    ↓
FastAPI Endpoint (/lyrics/search/all)
    ↓
LyricsService.search_lyrics()
    ↓
ElasticsearchLyricsRepository (multi_match query)
    ↓
Elasticsearch Index (full_text + chunks.text)
    ↓
Results with Lyrics + Chunks
    ↓
LyricsSearchResponse (JSON)
```

---

## 🔧 Troubleshooting

### "No results found"
1. Check Elasticsearch: `curl http://localhost:9200/`
2. Check lyrics indexed: `curl "http://localhost:9200/lyrics/_count"`
3. Try simpler query

### "Slow responses"
1. Reduce fuzziness: Change `"AUTO"` to `"1"` in repository
2. Add language filter to narrow results
3. Check Elasticsearch performance

### "Database migration failed"
1. Check you're in song-management-service directory
2. Verify DATABASE_URL is set
3. Run: `alembic current` to check status

---

## 📚 Documentation

| Document | Content |
|----------|---------|
| **IMPLEMENTATION_SUMMARY.md** | Overview, changes, architecture |
| **ELASTICSEARCH_MULTISEARCH_GUIDE.md** | Design, performance, troubleshooting |
| **ELASTICSEARCH_SEARCH_EXAMPLES.md** | Practical examples, cURL, Python |
| **CHECKLIST.md** | Pre-deployment, testing, issues |
| **QUICK_START.md** | This file - quick reference |

---

## ✨ Key Features

### Data Architecture
- Lyrics text → Elasticsearch (optimized for search)
- Song metadata → PostgreSQL (single source of truth)
- **No duplication** = No sync problems

### Search Capabilities
- Search full lyrics text
- Search individual lyrics lines/chunks
- Typo tolerance (fuzzy matching)
- Language filtering
- Up to 100 results per query

### Response Format
```json
{
  "id": "uuid",
  "full_text": "Complete lyrics...",
  "chunks": [
    {"start": 0.0, "end": 2.5, "text": "Line 1"},
    {"start": 2.5, "end": 5.0, "text": "Line 2"}
  ],
  "language": "en",
  "confidence_score": 0.95,
  "last_updated": "2026-02-19T...",
  "title": null,  // Optional metadata fields
  "creator": null,
  "duration_seconds": null,
  "thumbnail_url": null
}
```

---

## 🎓 Learn More

### Understanding Multi-Match
- Searches multiple fields in one query
- `type: "best_fields"` returns best match
- `fuzziness: "AUTO"` handles typos
- Faster than running multiple queries

### Why No Data Duplication
- Update song title in Postgres → Done (no reindex)
- Update in Elasticsearch → Would need reindex
- Our approach: Single source of truth (Postgres)

### Performance Tips
1. Use language filter when possible
2. Be specific in search terms
3. Monitor Elasticsearch performance
4. Consider caching for frequent searches

---

## 🚀 Next Steps

### Immediate
- [x] Run migration: `alembic upgrade head`
- [x] Test search: `curl "http://localhost:8000/lyrics/search/all?query=test"`
- [x] Read documentation

### Future Enhancements
- [ ] Populate metadata from processing_results
- [ ] Add pagination (offset/limit)
- [ ] Add result highlighting
- [ ] Add aggregations
- [ ] Add sorting options
- [ ] Add caching

---

## 📞 Help

**Migration issues?**
→ Read CHECKLIST.md section "Potential Issues"

**Search not working?**
→ Read ELASTICSEARCH_SEARCH_EXAMPLES.md "Troubleshooting"

**Want more examples?**
→ Read ELASTICSEARCH_SEARCH_EXAMPLES.md "Usage Examples"

**Architecture questions?**
→ Read ELASTICSEARCH_MULTISEARCH_GUIDE.md "Architecture"

---

**You're all set! Happy searching! 🎉**
