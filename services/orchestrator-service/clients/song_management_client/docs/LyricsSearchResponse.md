# LyricsSearchResponse

Extended lyrics response for search results. Includes lyrics data and optional metadata about the source.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**full_text** | **str** | Full lyrics text | 
**chunks** | [**List[LyricsChunk]**](LyricsChunk.md) | Lyrics chunks with timing | [optional] 
**language** | **str** | Language code | [optional] [default to 'en']
**confidence_score** | **float** |  | [optional] 
**title** | **str** |  | [optional] 
**creator** | **str** |  | [optional] 
**duration_seconds** | **int** |  | [optional] 
**thumbnail_url** | **str** |  | [optional] 
**id** | **str** | Lyrics ID | 
**last_updated** | **datetime** |  | [optional] 

## Example

```python
from song_management_client.models.lyrics_search_response import LyricsSearchResponse

# TODO update the JSON string below
json = "{}"
# create an instance of LyricsSearchResponse from a JSON string
lyrics_search_response_instance = LyricsSearchResponse.from_json(json)
# print the JSON string representation of the object
print LyricsSearchResponse.to_json()

# convert the object into a dict
lyrics_search_response_dict = lyrics_search_response_instance.to_dict()
# create an instance of LyricsSearchResponse from a dict
lyrics_search_response_from_dict = LyricsSearchResponse.from_dict(lyrics_search_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


