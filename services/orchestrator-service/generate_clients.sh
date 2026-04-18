openapi-generator generate \
            -i ../voice-separation-service/openapi.json \
            -g python \
            -o clients/voice_separation_client \
            --package-name voice_separation_client

openapi-generator generate \
            -i ../lyrics-extraction-service/openapi.json \
            -g python \
            -o clients/lyrics_client \
            --package-name lyrics_client

openapi-generator generate \
            -i ../song-management-service/openapi.json \
            -g python \
            -o clients/song_management_client \
            --package-name song_management_client

