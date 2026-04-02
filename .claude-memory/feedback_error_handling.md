---
name: Error Handling and Debugging Approach
description: Fix root causes systematically - proper null checks, specific exceptions, encoding handling
type: feedback
---

When encountering errors, diagnose and fix the root cause rather than masking symptoms.

**Why**: Multiple errors during development revealed patterns that needed systematic fixes:
1. NoneType errors from inadequate null checking (`article.get('source', {}).get('name')` when source is None)
2. Bare except clauses hiding actual error types
3. Unicode encoding errors from Windows console cp1252 limitations with emojis

**How to apply**:

**Null Safety Pattern**:
```python
# Bad
source_name = article.get('source', {}).get('name', 'Unknown')

# Good
source_obj = article.get('source')
source_name = 'Unknown'
if source_obj and isinstance(source_obj, dict):
    source_name = source_obj.get('name', 'Unknown')
```

**Exception Handling**:
```python
# Bad
except:
    pass

# Good
except (KeyError, IndexError, TypeError) as e:
    logger.warning(f"Failed to parse item: {e}")
    continue
```

**Unicode Handling on Windows**:
```python
def safe_print(text):
    try:
        print(text)
    except UnicodeEncodeError:
        safe_text = text.encode('ascii', errors='replace').decode('ascii')
        print(safe_text)
```

**Debugging Process**: When API integration fails, use WebSearch to find official documentation, WebFetch to read it, then verify HTTP method, auth headers, and response structure match documentation exactly. Don't guess.
