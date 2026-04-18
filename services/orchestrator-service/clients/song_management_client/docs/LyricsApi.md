# song_management_client.LyricsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_lyrics_lyrics_post**](LyricsApi.md#create_lyrics_lyrics_post) | **POST** /lyrics/ | Create Lyrics
[**delete_lyrics_lyrics_lyrics_id_delete**](LyricsApi.md#delete_lyrics_lyrics_lyrics_id_delete) | **DELETE** /lyrics/{lyrics_id} | Delete Lyrics
[**get_lyrics_lyrics_lyrics_id_get**](LyricsApi.md#get_lyrics_lyrics_lyrics_id_get) | **GET** /lyrics/{lyrics_id} | Get Lyrics
[**search_lyrics_lyrics_search_all_get**](LyricsApi.md#search_lyrics_lyrics_search_all_get) | **GET** /lyrics/search/all | Search Lyrics
[**update_lyrics_lyrics_lyrics_id_put**](LyricsApi.md#update_lyrics_lyrics_lyrics_id_put) | **PUT** /lyrics/{lyrics_id} | Update Lyrics


# **create_lyrics_lyrics_post**
> LyricsResponse create_lyrics_lyrics_post(lyrics_create, vocal_file_path=vocal_file_path, accompaniment_file_path=accompaniment_file_path)

Create Lyrics

Create a new lyrics entry with optional vocal and accompaniment audio files.

Accepts multipart/form-data. Text fields are form fields; files are uploaded to MinIO.
Files are stored with deterministic paths based on the lyrics ID.

- vocal_file: Optional vocal track audio file (e.g., MP3, WAV)
- accompaniment_file: Optional accompaniment/ instrumental track

### Example

```python
import time
import os
import song_management_client
from song_management_client.models.lyrics_create import LyricsCreate
from song_management_client.models.lyrics_response import LyricsResponse
from song_management_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = song_management_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with song_management_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = song_management_client.LyricsApi(api_client)
    lyrics_create = song_management_client.LyricsCreate() # LyricsCreate | 
    vocal_file_path = 'vocal_file_path_example' # str |  (optional)
    accompaniment_file_path = 'accompaniment_file_path_example' # str |  (optional)

    try:
        # Create Lyrics
        api_response = api_instance.create_lyrics_lyrics_post(lyrics_create, vocal_file_path=vocal_file_path, accompaniment_file_path=accompaniment_file_path)
        print("The response of LyricsApi->create_lyrics_lyrics_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LyricsApi->create_lyrics_lyrics_post: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **lyrics_create** | [**LyricsCreate**](LyricsCreate.md)|  | 
 **vocal_file_path** | **str**|  | [optional] 
 **accompaniment_file_path** | **str**|  | [optional] 

### Return type

[**LyricsResponse**](LyricsResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_lyrics_lyrics_lyrics_id_delete**
> object delete_lyrics_lyrics_lyrics_id_delete(lyrics_id)

Delete Lyrics



### Example

```python
import time
import os
import song_management_client
from song_management_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = song_management_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with song_management_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = song_management_client.LyricsApi(api_client)
    lyrics_id = 'lyrics_id_example' # str | 

    try:
        # Delete Lyrics
        api_response = api_instance.delete_lyrics_lyrics_lyrics_id_delete(lyrics_id)
        print("The response of LyricsApi->delete_lyrics_lyrics_lyrics_id_delete:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LyricsApi->delete_lyrics_lyrics_lyrics_id_delete: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **lyrics_id** | **str**|  | 

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
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_lyrics_lyrics_lyrics_id_get**
> LyricsResponse get_lyrics_lyrics_lyrics_id_get(lyrics_id)

Get Lyrics



### Example

```python
import time
import os
import song_management_client
from song_management_client.models.lyrics_response import LyricsResponse
from song_management_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = song_management_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with song_management_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = song_management_client.LyricsApi(api_client)
    lyrics_id = 'lyrics_id_example' # str | 

    try:
        # Get Lyrics
        api_response = api_instance.get_lyrics_lyrics_lyrics_id_get(lyrics_id)
        print("The response of LyricsApi->get_lyrics_lyrics_lyrics_id_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LyricsApi->get_lyrics_lyrics_lyrics_id_get: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **lyrics_id** | **str**|  | 

### Return type

[**LyricsResponse**](LyricsResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **search_lyrics_lyrics_search_all_get**
> List[LyricsSearchResponse] search_lyrics_lyrics_search_all_get(query, language=language)

Search Lyrics

Advanced multi-field search across lyrics.

Searches across:
- Full lyrics text (complete song lyrics)
- Individual chunk text (specific lines/verses/choruses)
- Language filter (optional)

Supports fuzzy matching for typos.

Example: /lyrics/search/all?query=hello&language=en

### Example

```python
import time
import os
import song_management_client
from song_management_client.models.lyrics_search_response import LyricsSearchResponse
from song_management_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = song_management_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with song_management_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = song_management_client.LyricsApi(api_client)
    query = 'query_example' # str | Search query across lyrics and song metadata
    language = 'language_example' # str | Optional language filter (e.g., 'en', 'es') (optional)

    try:
        # Search Lyrics
        api_response = api_instance.search_lyrics_lyrics_search_all_get(query, language=language)
        print("The response of LyricsApi->search_lyrics_lyrics_search_all_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LyricsApi->search_lyrics_lyrics_search_all_get: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **query** | **str**| Search query across lyrics and song metadata | 
 **language** | **str**| Optional language filter (e.g., &#39;en&#39;, &#39;es&#39;) | [optional] 

### Return type

[**List[LyricsSearchResponse]**](LyricsSearchResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_lyrics_lyrics_lyrics_id_put**
> LyricsResponse update_lyrics_lyrics_lyrics_id_put(lyrics_id, lyrics_create, vocal_file_path=vocal_file_path, accompaniment_file_path=accompaniment_file_path)

Update Lyrics



### Example

```python
import time
import os
import song_management_client
from song_management_client.models.lyrics_response import LyricsResponse
from song_management_client.models.lyrics_update import LyricsUpdate
from song_management_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = song_management_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with song_management_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = song_management_client.LyricsApi(api_client)
    lyrics_id = 'lyrics_id_example' # str | 
    lyrics_create = song_management_client.LyricsUpdate() # LyricsUpdate | 
    vocal_file_path = 'vocal_file_path_example' # str |  (optional)
    accompaniment_file_path = 'accompaniment_file_path_example' # str |  (optional)

    try:
        # Update Lyrics
        api_response = api_instance.update_lyrics_lyrics_lyrics_id_put(lyrics_id, lyrics_create, vocal_file_path=vocal_file_path, accompaniment_file_path=accompaniment_file_path)
        print("The response of LyricsApi->update_lyrics_lyrics_lyrics_id_put:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LyricsApi->update_lyrics_lyrics_lyrics_id_put: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **lyrics_id** | **str**|  | 
 **lyrics_create** | [**LyricsUpdate**](LyricsUpdate.md)|  | 
 **vocal_file_path** | **str**|  | [optional] 
 **accompaniment_file_path** | **str**|  | [optional] 

### Return type

[**LyricsResponse**](LyricsResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

