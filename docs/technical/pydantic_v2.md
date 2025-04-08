# Pydantic v2 Compatibility Guide

This document outlines the Pydantic v2 compatibility features and changes in the Master Folder Manager project.

## Overview

Master Folder Manager uses Pydantic v2 for data validation and serialization. This version brings significant performance improvements and new features compared to Pydantic v1.

## Key Changes

### 1. Model Configuration

We now use `ConfigDict` instead of the older `Config` class:

```python
from pydantic import ConfigDict

class MyModel(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={...},
        arbitrary_types_allowed=True
    )
```

### 2. Serialization

Instead of using `json_encoders`, we now implement custom serialization through the `model_dump` method:

```python
def model_dump(self, **kwargs):
    data = super().model_dump(**kwargs)
    if isinstance(data.get('timestamp'), datetime):
        data['timestamp'] = data['timestamp'].isoformat()
    return data
```

### 3. Validation Decorators

- Using `@field_validator` instead of `@validator`
- New `mode='before'` option for pre-validation transformations

```python
@field_validator('field_name', mode='before')
@classmethod
def validate_field(cls, v):
    # validation logic here
    return v
```

### 4. Error Messages

Error messages have been standardized in Pydantic v2. Our test suite has been updated to match the new format:

- String length: "String should have at least/at most X characters"
- Numeric range: "Input should be greater than or equal to X"
- Pattern matching: "String should match pattern"

## Migration Guide

If you're upgrading from a previous version that used Pydantic v1:

1. Update your requirements:
   ```bash
   pip install "pydantic>=2.0.0"
   ```

2. Update model configurations:
   ```python
   # Old
   class Config:
       json_encoders = {...}
   
   # New
   model_config = ConfigDict(...)
   ```

3. Replace custom JSON encoders with `model_dump`:
   ```python
   # Old
   json_encoders = {datetime: lambda v: v.isoformat()}
   
   # New
   def model_dump(self, **kwargs):
       data = super().model_dump(**kwargs)
       if isinstance(data.get('date'), datetime):
           data['date'] = data['date'].isoformat()
       return data
   ```

4. Update validator decorators:
   ```python
   # Old
   @validator('field')
   
   # New
   @field_validator('field')
   ```

## Testing

Our test suite has been updated to handle Pydantic v2's error messages. Key changes include:

1. Using `errors()` method to get validation errors:
   ```python
   with pytest.raises(ValidationError) as exc_info:
       MyModel(invalid_data)
   error_dict = exc_info.value.errors()
   ```

2. Checking error messages:
   ```python
   assert any("expected message" in err["msg"] for err in error_dict)
   ```

## Best Practices

1. Always use type hints with your models
2. Implement custom serialization through `model_dump`
3. Use `Field()` for field metadata and validation
4. Keep validation logic in `@field_validator` methods
5. Use `ConfigDict` for model configuration

## Known Issues

1. Some IDE type hints might not work correctly with Pydantic v2
2. The `json_encoders` deprecation warning will appear until v3.0
3. Some third-party libraries might not be fully compatible with Pydantic v2

## Additional Resources

- [Pydantic v2 Documentation](https://docs.pydantic.dev/latest/)
- [Migration Guide](https://docs.pydantic.dev/latest/migration/)
- [API Reference](https://docs.pydantic.dev/latest/api/) 