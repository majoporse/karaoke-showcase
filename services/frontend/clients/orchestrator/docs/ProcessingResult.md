# ProcessingResult


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**success** | **boolean** |  | [optional] [default to undefined]
**vocals_path** | **string** |  | [optional] [default to undefined]
**accompaniment_path** | **string** |  | [optional] [default to undefined]
**lyrics** | **string** |  | [optional] [default to undefined]
**chunks** | [**Array&lt;Chunk&gt;**](Chunk.md) |  | [optional] [default to undefined]
**yt_metadata** | [**YouTubeVideoMetadata**](YouTubeVideoMetadata.md) |  | [optional] [default to undefined]
**error** | **string** |  | [optional] [default to undefined]

## Example

```typescript
import { ProcessingResult } from './api';

const instance: ProcessingResult = {
    success,
    vocals_path,
    accompaniment_path,
    lyrics,
    chunks,
    yt_metadata,
    error,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
