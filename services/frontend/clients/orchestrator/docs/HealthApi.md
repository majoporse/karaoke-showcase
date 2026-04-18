# HealthApi

All URIs are relative to *http://localhost*

|Method | HTTP request | Description|
|------------- | ------------- | -------------|
|[**healthCheckHealthGet**](#healthcheckhealthget) | **GET** /health | Health check|

# **healthCheckHealthGet**
> any healthCheckHealthGet()

Check if the lyrics extraction service is healthy and model is loaded

### Example

```typescript
import {
    HealthApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new HealthApi(configuration);

const { status, data } = await apiInstance.healthCheckHealthGet();
```

### Parameters
This endpoint does not have any parameters.


### Return type

**any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

