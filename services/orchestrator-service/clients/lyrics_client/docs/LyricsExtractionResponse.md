# LyricsExtractionResponse

Response model for plain lyrics extraction.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**text** | **str** | Extracted lyrics as plain text | 
**duration_seconds** | **float** |  | [optional] 
**sample_rate** | **int** | Sample rate used for processing (Hz) | 

## Example

```python
from lyrics_client.models.lyrics_extraction_response import LyricsExtractionResponse

# TODO update the JSON string below
json = "{}"
# create an instance of LyricsExtractionResponse from a JSON string
lyrics_extraction_response_instance = LyricsExtractionResponse.from_json(json)
# print the JSON string representation of the object
print(LyricsExtractionResponse.to_json())

# convert the object into a dict
lyrics_extraction_response_dict = lyrics_extraction_response_instance.to_dict()
# create an instance of LyricsExtractionResponse from a dict
lyrics_extraction_response_from_dict = LyricsExtractionResponse.from_dict(lyrics_extraction_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


