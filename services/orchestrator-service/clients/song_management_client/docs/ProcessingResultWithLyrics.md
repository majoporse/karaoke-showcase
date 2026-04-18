# ProcessingResultWithLyrics


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**youtube_url** | **str** |  | 
**youtube_video_id** | **str** |  | 
**title** | **str** |  | 
**uploader** | **str** |  | 
**uploader_url** | **str** |  | 
**thumbnail_url** | **str** |  | 
**thumbnail** | **str** |  | 
**vocals_minio_path** | **str** |  | 
**accompaniment_minio_path** | **str** |  | 
**created_at** | **datetime** |  | 
**error_message** | **str** |  | 
**lyrics_id** | **str** |  | 
**lyrics** | [**Lyrics**](Lyrics.md) |  | 

## Example

```python
from song_management_client.models.processing_result_with_lyrics import ProcessingResultWithLyrics

# TODO update the JSON string below
json = "{}"
# create an instance of ProcessingResultWithLyrics from a JSON string
processing_result_with_lyrics_instance = ProcessingResultWithLyrics.from_json(json)
# print the JSON string representation of the object
print ProcessingResultWithLyrics.to_json()

# convert the object into a dict
processing_result_with_lyrics_dict = processing_result_with_lyrics_instance.to_dict()
# create an instance of ProcessingResultWithLyrics from a dict
processing_result_with_lyrics_from_dict = ProcessingResultWithLyrics.from_dict(processing_result_with_lyrics_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


