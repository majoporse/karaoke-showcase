# DownloadsApi

All URIs are relative to *http://localhost*

|Method | HTTP request | Description|
|------------- | ------------- | -------------|
|[**downloadFileDownloadFilenameGet**](#downloadfiledownloadfilenameget) | **GET** /download/{filename} | Download processed file|

# **downloadFileDownloadFilenameGet**
> any downloadFileDownloadFilenameGet()

Download processed audio files (separated tracks or temporary files)

### Example

```typescript
import {
    DownloadsApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new DownloadsApi(configuration);

let filename: string; // (default to undefined)

const { status, data } = await apiInstance.downloadFileDownloadFilenameGet(
    filename
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **filename** | [**string**] |  | defaults to undefined|


### Return type

**any**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/zip


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | File downloaded successfully |  -  |
|**404** | File not found |  -  |
|**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

