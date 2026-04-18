# LyricsChunk


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**start** | **float** |  | 
**end** | **float** |  | 
**text** | **str** |  | 

## Example

```python
from song_management_client.models.lyrics_chunk import LyricsChunk

# TODO update the JSON string below
json = "{}"
# create an instance of LyricsChunk from a JSON string
lyrics_chunk_instance = LyricsChunk.from_json(json)
# print the JSON string representation of the object
print(LyricsChunk.to_json())

# convert the object into a dict
lyrics_chunk_dict = lyrics_chunk_instance.to_dict()
# create an instance of LyricsChunk from a dict
lyrics_chunk_from_dict = LyricsChunk.from_dict(lyrics_chunk_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


