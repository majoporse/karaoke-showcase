# PaginatedResponseProcessingResultResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**items** | [**List[ProcessingResultResponse]**](ProcessingResultResponse.md) | List of items for this page | 
**total** | **int** | Total number of items across all pages | 
**page** | **int** | Current page number (1-indexed) | 
**limit** | **int** | Number of items per page | 
**total_pages** | **int** | Total number of pages | 

## Example

```python
from song_management_client.models.paginated_response_processing_result_response import PaginatedResponseProcessingResultResponse

# TODO update the JSON string below
json = "{}"
# create an instance of PaginatedResponseProcessingResultResponse from a JSON string
paginated_response_processing_result_response_instance = PaginatedResponseProcessingResultResponse.from_json(json)
# print the JSON string representation of the object
print(PaginatedResponseProcessingResultResponse.to_json())

# convert the object into a dict
paginated_response_processing_result_response_dict = paginated_response_processing_result_response_instance.to_dict()
# create an instance of PaginatedResponseProcessingResultResponse from a dict
paginated_response_processing_result_response_from_dict = PaginatedResponseProcessingResultResponse.from_dict(paginated_response_processing_result_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


