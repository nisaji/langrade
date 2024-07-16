# Troubleshooting

## Model Not Found

If you get a "model not found" error:

Check that you're using a valid model name for the chosen provider.

Ensure your API key has access to the specified model.

```python
from langrade import document_grader

try:
    grader = document_grader("openai", "your_api_key", "invalid-model-name")
except Exception as e:
    print(f"Error: {e}")
```

## Import Errors

If you're having trouble importing Langrade:

Ensure Langrade is installed: pip install langrade
Check your Python path:

```python
import sys
print(sys.path)
```

## Debugging

For detailed debugging, enable logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```
