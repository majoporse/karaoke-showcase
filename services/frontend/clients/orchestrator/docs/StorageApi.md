# StorageApi

All URIs are relative to *http://localhost*

|Method | HTTP request | Description|
|------------- | ------------- | -------------|
|[**presignUrlPresignGet**](#presignurlpresignget) | **GET** /presign | Presign URL|

# **presignUrlPresignGet**
> PresignResponse presignUrlPresignGet()

Get a presigned URL for a file in the storage bucket

### Example

```typescript
import {
    StorageApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new StorageApi(configuration);

let key: string; // (default to undefined)

const { status, data } = await apiInstance.presignUrlPresignGet(
    key
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **key** | [**string**] |  | defaults to undefined|


### Return type

**PresignResponse**

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

