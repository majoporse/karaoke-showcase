# ProcessingResultResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **UUID** |  | 
**youtube_url** | **str** |  | 
**youtube_video_id** | **str** |  | 
**title** | **str** |  | 
**uploader** | **str** |  | 
**uploader_url** | **str** |  | 
**thumbnail_url** | **str** |  | 
**thumbnail** | **str** |  | 
**vocals_minio_path** | **str** |  | 
**accompaniment_minio_path** | **str** |  | 
**error_message** | **str** |  | [optional] 
**created_at** | **datetime** |  | 
**lyrics** | [**LyricsResponse**](LyricsResponse.md) |  | [optional] 

## Example

```python
from song_management_client.models.processing_result_response import ProcessingResultResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ProcessingResultResponse from a JSON string
processing_result_response_instance = ProcessingResultResponse.from_json(json)
# print the JSON string representation of the object
print(ProcessingResultResponse.to_json())

# convert the object into a dict
processing_result_response_dict = processing_result_response_instance.to_dict()
# create an instance of ProcessingResultResponse from a dict
processing_result_response_from_dict = ProcessingResultResponse.from_dict(processing_result_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


