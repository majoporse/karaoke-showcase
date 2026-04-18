# LyricsWithTimestampsResponse

Response model for lyrics extraction with timestamps.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**text** | **str** | Full transcribed text | 
**chunks** | [**List[Chunk]**](Chunk.md) | List of lyrics segments with timestamps | 
**total_duration_seconds** | **float** |  | [optional] 
**sample_rate** | **int** | Sample rate used for processing (Hz) | 

## Example

```python
from lyrics_client.models.lyrics_with_timestamps_response import LyricsWithTimestampsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of LyricsWithTimestampsResponse from a JSON string
lyrics_with_timestamps_response_instance = LyricsWithTimestampsResponse.from_json(json)
# print the JSON string representation of the object
print(LyricsWithTimestampsResponse.to_json())

# convert the object into a dict
lyrics_with_timestamps_response_dict = lyrics_with_timestamps_response_instance.to_dict()
# create an instance of LyricsWithTimestampsResponse from a dict
lyrics_with_timestamps_response_from_dict = LyricsWithTimestampsResponse.from_dict(lyrics_with_timestamps_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


