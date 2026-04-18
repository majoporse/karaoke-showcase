class SongRelationships:
    VERSIONS = "song_versions"


class SongVersionRelationships:
    SONG = "song"
    PROCESSING_RESULTS = "processing_results"
    LYRICS = "lyrics"


class ProcessingResultRelationships:
    SONG_VERSION = "song_version"


class LyricsRelationships:
    SONG_VERSION = "song_version"
