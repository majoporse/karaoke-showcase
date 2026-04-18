# LyricsUpdate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**full_text** | **str** |  | [optional] 
**chunks** | [**List[LyricsChunk]**](LyricsChunk.md) |  | [optional] 
**language** | **str** |  | [optional] 
**confidence_score** | **float** |  | [optional] 
**title** | **str** |  | [optional] 
**creator** | **str** |  | [optional] 
**duration_seconds** | **int** |  | [optional] 
**thumbnail_url** | **str** |  | [optional] 

## Example

```python
from song_management_client.models.lyrics_update import LyricsUpdate

# TODO update the JSON string below
json = "{}"
# create an instance of LyricsUpdate from a JSON string
lyrics_update_instance = LyricsUpdate.from_json(json)
# print the JSON string representation of the object
print(LyricsUpdate.to_json())

# convert the object into a dict
lyrics_update_dict = lyrics_update_instance.to_dict()
# create an instance of LyricsUpdate from a dict
lyrics_update_from_dict = LyricsUpdate.from_dict(lyrics_update_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


