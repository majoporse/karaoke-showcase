# ProcessingResultCreate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
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
**lyrics** | [**LyricsCreate**](LyricsCreate.md) |  | 

## Example

```python
from song_management_client.models.processing_result_create import ProcessingResultCreate

# TODO update the JSON string below
json = "{}"
# create an instance of ProcessingResultCreate from a JSON string
processing_result_create_instance = ProcessingResultCreate.from_json(json)
# print the JSON string representation of the object
print(ProcessingResultCreate.to_json())

# convert the object into a dict
processing_result_create_dict = processing_result_create_instance.to_dict()
# create an instance of ProcessingResultCreate from a dict
processing_result_create_from_dict = ProcessingResultCreate.from_dict(processing_result_create_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


