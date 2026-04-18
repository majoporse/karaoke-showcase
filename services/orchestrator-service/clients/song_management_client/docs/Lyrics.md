# Lyrics


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**full_text** | **str** |  | [optional] [default to '']
**chunks** | [**List[DomainLyricsChunkLyricsChunk]**](DomainLyricsChunkLyricsChunk.md) |  | [optional] 
**language** | **str** |  | [optional] [default to 'en']
**confidence_score** | **float** |  | [optional] 
**last_updated** | **datetime** |  | [optional] 
**title** | **str** |  | [optional] 
**creator** | **str** |  | [optional] 
**duration_seconds** | **int** |  | [optional] 
**thumbnail_url** | **str** |  | [optional] 

## Example

```python
from song_management_client.models.lyrics import Lyrics

# TODO update the JSON string below
json = "{}"
# create an instance of Lyrics from a JSON string
lyrics_instance = Lyrics.from_json(json)
# print the JSON string representation of the object
print Lyrics.to_json()

# convert the object into a dict
lyrics_dict = lyrics_instance.to_dict()
# create an instance of Lyrics from a dict
lyrics_from_dict = Lyrics.from_dict(lyrics_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


