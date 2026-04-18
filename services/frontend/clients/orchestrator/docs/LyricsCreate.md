# LyricsCreate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**full_text** | **string** | Full lyrics text | [default to undefined]
**chunks** | [**Array&lt;Chunk&gt;**](Chunk.md) | Lyrics chunks with timing | [optional] [default to undefined]
**language** | **string** | Language code | [optional] [default to 'en']
**confidence_score** | **number** |  | [optional] [default to undefined]
**title** | **string** |  | [optional] [default to undefined]
**creator** | **string** |  | [optional] [default to undefined]
**thumbnail_url** | **string** |  | [optional] [default to undefined]

## Example

```typescript
import { LyricsCreate } from './api';

const instance: LyricsCreate = {
    full_text,
    chunks,
    language,
    confidence_score,
    title,
    creator,
    thumbnail_url,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
