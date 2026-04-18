# lyrics_client.LyricsExtractionApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**extract_lyrics_extract_lyrics_post**](LyricsExtractionApi.md#extract_lyrics_extract_lyrics_post) | **POST** /extract-lyrics | Extract plain lyrics
[**extract_lyrics_with_timestamps_extract_lyrics_with_timestamps_post**](LyricsExtractionApi.md#extract_lyrics_with_timestamps_extract_lyrics_with_timestamps_post) | **POST** /extract-lyrics/with-timestamps | Extract lyrics with timestamps


# **extract_lyrics_extract_lyrics_post**
> LyricsExtractionResponse extract_lyrics_extract_lyrics_post(minio_path)

Extract plain lyrics

Extract lyrics as plain text from an audio file using Whisper speech recognition

### Example


```python
import lyrics_client
from lyrics_client.models.lyrics_extraction_response import LyricsExtractionResponse
from lyrics_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = lyrics_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with lyrics_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = lyrics_client.LyricsExtractionApi(api_client)
    minio_path = 'minio_path_example' # str | 

    try:
        # Extract plain lyrics
        api_response = api_instance.extract_lyrics_extract_lyrics_post(minio_path)
        print("The response of LyricsExtractionApi->extract_lyrics_extract_lyrics_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LyricsExtractionApi->extract_lyrics_extract_lyrics_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **minio_path** | **str**|  | 

### Return type

[**LyricsExtractionResponse**](LyricsExtractionResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Lyrics extracted successfully |  -  |
**400** | Invalid file type (not an audio file) |  -  |
**500** | Error processing audio file |  -  |
**503** | Speech recognition model not available |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **extract_lyrics_with_timestamps_extract_lyrics_with_timestamps_post**
> LyricsWithTimestampsResponse extract_lyrics_with_timestamps_extract_lyrics_with_timestamps_post(minio_path)

Extract lyrics with timestamps

Extract lyrics with timestamps from an audio file using chunked Whisper processing

### Example


```python
import lyrics_client
from lyrics_client.models.lyrics_with_timestamps_response import LyricsWithTimestampsResponse
from lyrics_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = lyrics_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with lyrics_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = lyrics_client.LyricsExtractionApi(api_client)
    minio_path = 'minio_path_example' # str | 

    try:
        # Extract lyrics with timestamps
        api_response = api_instance.extract_lyrics_with_timestamps_extract_lyrics_with_timestamps_post(minio_path)
        print("The response of LyricsExtractionApi->extract_lyrics_with_timestamps_extract_lyrics_with_timestamps_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LyricsExtractionApi->extract_lyrics_with_timestamps_extract_lyrics_with_timestamps_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **minio_path** | **str**|  | 

### Return type

[**LyricsWithTimestampsResponse**](LyricsWithTimestampsResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Lyrics with timestamps extracted successfully |  -  |
**400** | Invalid file type (not an audio file) |  -  |
**500** | Error processing audio file |  -  |
**503** | Speech recognition model not available |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

