# ProcessingApi

All URIs are relative to *http://localhost*

|Method | HTTP request | Description|
|------------- | ------------- | -------------|
|[**getLatestJobMessageProcessJobJobIdLatestMessageGet**](#getlatestjobmessageprocessjobjobidlatestmessageget) | **GET** /process/job/{job_id}/latest-message | Get the latest message from a job\&#39;s progress stream for reconnection|
|[**getProcessingResultByIdProcessProcessingIdGet**](#getprocessingresultbyidprocessprocessingidget) | **GET** /process/processing/{id} | Get Processing Result By Id|
|[**getQueuePositionProcessQueuePositionTaskIdGet**](#getqueuepositionprocessqueuepositiontaskidget) | **GET** /process/queue/position/{task_id} | Get the position of a task in the Redis queue|
|[**queueAudioProcessingProcessQueuePost**](#queueaudioprocessingprocessqueuepost) | **POST** /process/queue | Queue audio processing from YouTube URL|
|[**searchResultsByQueryProcessSearchGet**](#searchresultsbyqueryprocesssearchget) | **GET** /process/search | Search processing results by lyrics query|

# **getLatestJobMessageProcessJobJobIdLatestMessageGet**
> LatestMessageResponse getLatestJobMessageProcessJobJobIdLatestMessageGet()


### Example

```typescript
import {
    ProcessingApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new ProcessingApi(configuration);

let jobId: string; // (default to undefined)

const { status, data } = await apiInstance.getLatestJobMessageProcessJobJobIdLatestMessageGet(
    jobId
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **jobId** | [**string**] |  | defaults to undefined|


### Return type

**LatestMessageResponse**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Successful Response |  -  |
|**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **getProcessingResultByIdProcessProcessingIdGet**
> ProcessingResponse getProcessingResultByIdProcessProcessingIdGet()


### Example

```typescript
import {
    ProcessingApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new ProcessingApi(configuration);

let id: string; // (default to undefined)

const { status, data } = await apiInstance.getProcessingResultByIdProcessProcessingIdGet(
    id
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **id** | [**string**] |  | defaults to undefined|


### Return type

**ProcessingResponse**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Successful Response |  -  |
|**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **getQueuePositionProcessQueuePositionTaskIdGet**
> QueuePositionResponse getQueuePositionProcessQueuePositionTaskIdGet()


### Example

```typescript
import {
    ProcessingApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new ProcessingApi(configuration);

let taskId: string; // (default to undefined)

const { status, data } = await apiInstance.getQueuePositionProcessQueuePositionTaskIdGet(
    taskId
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **taskId** | [**string**] |  | defaults to undefined|


### Return type

**QueuePositionResponse**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Successful Response |  -  |
|**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **queueAudioProcessingProcessQueuePost**
> JobResponse queueAudioProcessingProcessQueuePost()


### Example

```typescript
import {
    ProcessingApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new ProcessingApi(configuration);

let youtubeUrl: string; // (default to undefined)

const { status, data } = await apiInstance.queueAudioProcessingProcessQueuePost(
    youtubeUrl
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **youtubeUrl** | [**string**] |  | defaults to undefined|


### Return type

**JobResponse**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Successful Response |  -  |
|**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **searchResultsByQueryProcessSearchGet**
> SearchResultsResponse searchResultsByQueryProcessSearchGet()


### Example

```typescript
import {
    ProcessingApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new ProcessingApi(configuration);

let query: string; // (default to undefined)
let limit: number; // (optional) (default to 10)
let page: number; // (optional) (default to 0)

const { status, data } = await apiInstance.searchResultsByQueryProcessSearchGet(
    query,
    limit,
    page
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **query** | [**string**] |  | defaults to undefined|
| **limit** | [**number**] |  | (optional) defaults to 10|
| **page** | [**number**] |  | (optional) defaults to 0|


### Return type

**SearchResultsResponse**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Successful Response |  -  |
|**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

