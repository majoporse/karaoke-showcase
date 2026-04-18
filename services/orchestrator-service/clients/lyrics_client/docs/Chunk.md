# Chunk

A segment of lyrics with timestamp range.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**start** | **float** | Start time of the segment in seconds | 
**end** | **float** | End time of the segment in seconds | 
**text** | **str** | Lyrics text for this segment | 

## Example

```python
from lyrics_client.models.chunk import Chunk

# TODO update the JSON string below
json = "{}"
# create an instance of Chunk from a JSON string
chunk_instance = Chunk.from_json(json)
# print the JSON string representation of the object
print(Chunk.to_json())

# convert the object into a dict
chunk_dict = chunk_instance.to_dict()
# create an instance of Chunk from a dict
chunk_from_dict = Chunk.from_dict(chunk_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


