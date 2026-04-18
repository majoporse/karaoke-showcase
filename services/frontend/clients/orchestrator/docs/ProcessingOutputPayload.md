# ProcessingOutputPayload


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**current_step** | **number** | Current step number (0-5) | [default to undefined]
**total_steps** | **number** | Total number of steps | [optional] [default to 5]
**desc** | **string** | Progress or status message | [default to undefined]
**result** | [**ProcessingResult**](ProcessingResult.md) |  | [optional] [default to undefined]

## Example

```typescript
import { ProcessingOutputPayload } from './api';

const instance: ProcessingOutputPayload = {
    current_step,
    total_steps,
    desc,
    result,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
