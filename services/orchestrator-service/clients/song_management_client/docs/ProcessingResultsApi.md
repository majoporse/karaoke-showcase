# song_management_client.ProcessingResultsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_result_processing_results_post**](ProcessingResultsApi.md#create_result_processing_results_post) | **POST** /processing-results/ | Create Result
[**delete_result_processing_results_result_id_delete**](ProcessingResultsApi.md#delete_result_processing_results_result_id_delete) | **DELETE** /processing-results/{result_id} | Delete Result
[**get_result_processing_results_result_id_get**](ProcessingResultsApi.md#get_result_processing_results_result_id_get) | **GET** /processing-results/{result_id} | Get Result
[**search_processing_results_processing_results_get**](ProcessingResultsApi.md#search_processing_results_processing_results_get) | **GET** /processing-results/ | Search Processing Results
[**update_result_processing_results_result_id_put**](ProcessingResultsApi.md#update_result_processing_results_result_id_put) | **PUT** /processing-results/{result_id} | Update Result


# **create_result_processing_results_post**
> ProcessingResultResponse create_result_processing_results_post(processing_result_create)

Create Result

### Example


```python
import song_management_client
from song_management_client.models.processing_result_create import ProcessingResultCreate
from song_management_client.models.processing_result_response import ProcessingResultResponse
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
    api_instance = song_management_client.ProcessingResultsApi(api_client)
    processing_result_create = song_management_client.ProcessingResultCreate() # ProcessingResultCreate | 

    try:
        # Create Result
        api_response = api_instance.create_result_processing_results_post(processing_result_create)
        print("The response of ProcessingResultsApi->create_result_processing_results_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProcessingResultsApi->create_result_processing_results_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **processing_result_create** | [**ProcessingResultCreate**](ProcessingResultCreate.md)|  | 

### Return type

[**ProcessingResultResponse**](ProcessingResultResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_result_processing_results_result_id_delete**
> DeleteResponse delete_result_processing_results_result_id_delete(result_id)

Delete Result

### Example


```python
import song_management_client
from song_management_client.models.delete_response import DeleteResponse
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
    api_instance = song_management_client.ProcessingResultsApi(api_client)
    result_id = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | 

    try:
        # Delete Result
        api_response = api_instance.delete_result_processing_results_result_id_delete(result_id)
        print("The response of ProcessingResultsApi->delete_result_processing_results_result_id_delete:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProcessingResultsApi->delete_result_processing_results_result_id_delete: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **result_id** | **UUID**|  | 

### Return type

[**DeleteResponse**](DeleteResponse.md)

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

# **get_result_processing_results_result_id_get**
> ProcessingResultResponse get_result_processing_results_result_id_get(result_id)

Get Result

### Example


```python
import song_management_client
from song_management_client.models.processing_result_response import ProcessingResultResponse
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
    api_instance = song_management_client.ProcessingResultsApi(api_client)
    result_id = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | 

    try:
        # Get Result
        api_response = api_instance.get_result_processing_results_result_id_get(result_id)
        print("The response of ProcessingResultsApi->get_result_processing_results_result_id_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProcessingResultsApi->get_result_processing_results_result_id_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **result_id** | **UUID**|  | 

### Return type

[**ProcessingResultResponse**](ProcessingResultResponse.md)

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

# **search_processing_results_processing_results_get**
> PaginatedResponseProcessingResultResponse search_processing_results_processing_results_get(query, language=language, page=page, limit=limit)

Search Processing Results

### Example


```python
import song_management_client
from song_management_client.models.paginated_response_processing_result_response import PaginatedResponseProcessingResultResponse
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
    api_instance = song_management_client.ProcessingResultsApi(api_client)
    query = 'query_example' # str | Search query for lyrics content
    language = 'language_example' # str | Filter by language (optional)
    page = 1 # int | Page number (1-indexed) (optional) (default to 1)
    limit = 20 # int | Number of results per page (optional) (default to 20)

    try:
        # Search Processing Results
        api_response = api_instance.search_processing_results_processing_results_get(query, language=language, page=page, limit=limit)
        print("The response of ProcessingResultsApi->search_processing_results_processing_results_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProcessingResultsApi->search_processing_results_processing_results_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **query** | **str**| Search query for lyrics content | 
 **language** | **str**| Filter by language | [optional] 
 **page** | **int**| Page number (1-indexed) | [optional] [default to 1]
 **limit** | **int**| Number of results per page | [optional] [default to 20]

### Return type

[**PaginatedResponseProcessingResultResponse**](PaginatedResponseProcessingResultResponse.md)

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

# **update_result_processing_results_result_id_put**
> ProcessingResultResponse update_result_processing_results_result_id_put(result_id, processing_result_update)

Update Result

### Example


```python
import song_management_client
from song_management_client.models.processing_result_response import ProcessingResultResponse
from song_management_client.models.processing_result_update import ProcessingResultUpdate
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
    api_instance = song_management_client.ProcessingResultsApi(api_client)
    result_id = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | 
    processing_result_update = song_management_client.ProcessingResultUpdate() # ProcessingResultUpdate | 

    try:
        # Update Result
        api_response = api_instance.update_result_processing_results_result_id_put(result_id, processing_result_update)
        print("The response of ProcessingResultsApi->update_result_processing_results_result_id_put:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProcessingResultsApi->update_result_processing_results_result_id_put: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **result_id** | **UUID**|  | 
 **processing_result_update** | [**ProcessingResultUpdate**](ProcessingResultUpdate.md)|  | 

### Return type

[**ProcessingResultResponse**](ProcessingResultResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

