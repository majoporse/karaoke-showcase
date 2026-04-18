# ProcessingResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**youtube_url** | **string** |  | [optional] [default to undefined]
**youtube_video_id** | **string** |  | [optional] [default to undefined]
**title** | **string** |  | [optional] [default to undefined]
**uploader** | **string** |  | [optional] [default to undefined]
**uploader_url** | **string** |  | [optional] [default to undefined]
**thumbnail_url** | **string** |  | [optional] [default to undefined]
**thumbnail** | **string** |  | [optional] [default to undefined]
**vocals_minio_path** | **string** |  | [optional] [default to undefined]
**accompaniment_minio_path** | **string** |  | [optional] [default to undefined]
**lyrics** | [**Lyrics**](Lyrics.md) |  | [optional] [default to undefined]
**error_message** | **string** |  | [optional] [default to undefined]
**id** | **string** |  | [default to undefined]
**created_at** | **string** |  | [optional] [default to undefined]

## Example

```typescript
import { ProcessingResponse } from './api';

const instance: ProcessingResponse = {
    youtube_url,
    youtube_video_id,
    title,
    uploader,
    uploader_url,
    thumbnail_url,
    thumbnail,
    vocals_minio_path,
    accompaniment_minio_path,
    lyrics,
    error_message,
    id,
    created_at,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
