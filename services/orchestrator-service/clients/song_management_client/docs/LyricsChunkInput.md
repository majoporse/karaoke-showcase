# LyricsChunkInput


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**start** | **float** |  | 
**end** | **float** |  | 
**text** | **str** |  | 

## Example

```python
from song_management_client.models.lyrics_chunk_input import LyricsChunkInput

# TODO update the JSON string below
json = "{}"
# create an instance of LyricsChunkInput from a JSON string
lyrics_chunk_input_instance = LyricsChunkInput.from_json(json)
# print the JSON string representation of the object
print LyricsChunkInput.to_json()

# convert the object into a dict
lyrics_chunk_input_dict = lyrics_chunk_input_instance.to_dict()
# create an instance of LyricsChunkInput from a dict
lyrics_chunk_input_from_dict = LyricsChunkInput.from_dict(lyrics_chunk_input_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


