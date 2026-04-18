# LyricsResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**processing_id** | **UUID** |  | 
**full_text** | **str** |  | 
**chunks** | [**List[LyricsChunk]**](LyricsChunk.md) |  | [optional] [default to []]
**language** | **str** |  | [optional] [default to 'en']
**confidence_score** | **float** |  | [optional] 

## Example

```python
from song_management_client.models.lyrics_response import LyricsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of LyricsResponse from a JSON string
lyrics_response_instance = LyricsResponse.from_json(json)
# print the JSON string representation of the object
print(LyricsResponse.to_json())

# convert the object into a dict
lyrics_response_dict = lyrics_response_instance.to_dict()
# create an instance of LyricsResponse from a dict
lyrics_response_from_dict = LyricsResponse.from_dict(lyrics_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


