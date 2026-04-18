# LyricsCreate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**full_text** | **str** |  | 
**chunks** | [**List[LyricsChunk]**](LyricsChunk.md) |  | [optional] [default to []]
**language** | **str** |  | [optional] [default to 'en']
**confidence_score** | **float** |  | [optional] 

## Example

```python
from song_management_client.models.lyrics_create import LyricsCreate

# TODO update the JSON string below
json = "{}"
# create an instance of LyricsCreate from a JSON string
lyrics_create_instance = LyricsCreate.from_json(json)
# print the JSON string representation of the object
print(LyricsCreate.to_json())

# convert the object into a dict
lyrics_create_dict = lyrics_create_instance.to_dict()
# create an instance of LyricsCreate from a dict
lyrics_create_from_dict = LyricsCreate.from_dict(lyrics_create_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


