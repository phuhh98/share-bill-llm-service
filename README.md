# Share bill service

## Useful command

```bash
# Scan for package and add to requirements.txt
pipreqs . --force

# Install all packages from requirements.txt
pip install -r requirements.txt

# Run application with fastapi dev mode
fastapi dev src/main.py --reload

```

## Required env variables

```env
ENVIRONMENT=        # dev | prod
GEMINI_API_KEY=
```


## Common error
### Generated bill content does not match with total number of items
Look for configuration of thinking budget and output token limit. Increase thinking limit and output token limit should be at least 5x of thinking budget
