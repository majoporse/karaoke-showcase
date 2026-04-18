# ProcessingResultUpdate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**youtube_url** | **str** |  | [optional] 
**youtube_video_id** | **str** |  | [optional] 
**title** | **str** |  | [optional] 
**uploader** | **str** |  | [optional] 
**uploader_url** | **str** |  | [optional] 
**thumbnail_url** | **str** |  | [optional] 
**thumbnail** | **str** |  | [optional] 
**vocals_minio_path** | **str** |  | [optional] 
**accompaniment_minio_path** | **str** |  | [optional] 
**error_message** | **str** |  | [optional] 
**lyrics** | [**LyricsUpdate**](LyricsUpdate.md) |  | [optional] 

## Example

```python
from song_management_client.models.processing_result_update import ProcessingResultUpdate

# TODO update the JSON string below
json = "{}"
# create an instance of ProcessingResultUpdate from a JSON string
processing_result_update_instance = ProcessingResultUpdate.from_json(json)
# print the JSON string representation of the object
print(ProcessingResultUpdate.to_json())

# convert the object into a dict
processing_result_update_dict = processing_result_update_instance.to_dict()
# create an instance of ProcessingResultUpdate from a dict
processing_result_update_from_dict = ProcessingResultUpdate.from_dict(processing_result_update_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


