# voice_separation_client.VoiceSeparationApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_configuration_separate_voice_config_get**](VoiceSeparationApi.md#get_configuration_separate_voice_config_get) | **GET** /separate-voice/config | Get voice separation configuration
[**separate_voice_unified_separate_voice_post**](VoiceSeparationApi.md#separate_voice_unified_separate_voice_post) | **POST** /separate-voice | Separate vocals from music


# **get_configuration_separate_voice_config_get**
> object get_configuration_separate_voice_config_get()

Get voice separation configuration

Returns the current voice separation configuration including the active model

### Example


```python
import voice_separation_client
from voice_separation_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = voice_separation_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with voice_separation_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = voice_separation_client.VoiceSeparationApi(api_client)

    try:
        # Get voice separation configuration
        api_response = api_instance.get_configuration_separate_voice_config_get()
        print("The response of VoiceSeparationApi->get_configuration_separate_voice_config_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling VoiceSeparationApi->get_configuration_separate_voice_config_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Configuration information |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **separate_voice_unified_separate_voice_post**
> SeparateVoiceResponse separate_voice_unified_separate_voice_post(minio_path)

Separate vocals from music

Accepts an audio file and returns a path to object storage for the separated vocals and accompaniment tracks using the configured model

### Example


```python
import voice_separation_client
from voice_separation_client.models.separate_voice_response import SeparateVoiceResponse
from voice_separation_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = voice_separation_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with voice_separation_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = voice_separation_client.VoiceSeparationApi(api_client)
    minio_path = 'minio_path_example' # str | 

    try:
        # Separate vocals from music
        api_response = api_instance.separate_voice_unified_separate_voice_post(minio_path)
        print("The response of VoiceSeparationApi->separate_voice_unified_separate_voice_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling VoiceSeparationApi->separate_voice_unified_separate_voice_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **minio_path** | **str**|  | 

### Return type

[**SeparateVoiceResponse**](SeparateVoiceResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Voice separation successful - returns ZIP file |  -  |
**400** | Invalid file type (not an audio file) |  -  |
**500** | Error processing audio file |  -  |
**503** | Voice separation service not ready |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

