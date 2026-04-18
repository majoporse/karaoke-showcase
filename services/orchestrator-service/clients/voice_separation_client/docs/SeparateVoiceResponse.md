# SeparateVoiceResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**vocals_path** | **str** | Object storage path to the separated vocals file | 
**accompaniment_path** | **str** | Object storage path to the separated accompaniment file | 

## Example

```python
from voice_separation_client.models.separate_voice_response import SeparateVoiceResponse

# TODO update the JSON string below
json = "{}"
# create an instance of SeparateVoiceResponse from a JSON string
separate_voice_response_instance = SeparateVoiceResponse.from_json(json)
# print the JSON string representation of the object
print(SeparateVoiceResponse.to_json())

# convert the object into a dict
separate_voice_response_dict = separate_voice_response_instance.to_dict()
# create an instance of SeparateVoiceResponse from a dict
separate_voice_response_from_dict = SeparateVoiceResponse.from_dict(separate_voice_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


