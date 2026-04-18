# ApiCommonLyricsChunk


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**start** | **float** |  | 
**end** | **float** |  | 
**text** | **str** |  | 

## Example

```python
from song_management_client.models.api_common_lyrics_chunk import ApiCommonLyricsChunk

# TODO update the JSON string below
json = "{}"
# create an instance of ApiCommonLyricsChunk from a JSON string
api_common_lyrics_chunk_instance = ApiCommonLyricsChunk.from_json(json)
# print the JSON string representation of the object
print ApiCommonLyricsChunk.to_json()

# convert the object into a dict
api_common_lyrics_chunk_dict = api_common_lyrics_chunk_instance.to_dict()
# create an instance of ApiCommonLyricsChunk from a dict
api_common_lyrics_chunk_from_dict = ApiCommonLyricsChunk.from_dict(api_common_lyrics_chunk_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


