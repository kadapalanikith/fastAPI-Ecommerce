# FastAPI Project

A modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.

## Features

- **Fast**: Very high performance, on par with **NodeJS** and **Go**.
- **Fast to code**: Increase the speed to develop features by about 200% to 300%.
- **Fewer bugs**: Reduce about 40% of human (developer) induced errors.
- **Intuitive**: Great editor support. Completion everywhere. Less time debugging.
- **Easy**: Designed to be easy to use and learn. Less time reading docs.
- **Short**: Minimize code duplication. Multiple features from each parameter declaration.
- **Robust**: Get production-ready code. With automatic interactive documentation.
- **Standards-based**: Based on (and fully compatible with) the open standards for APIs: **OpenAPI** and **JSON Schema**.

## Installation

```bash
pip install fastapi
pip install "uvicorn[standard]"
```

## Quick Start

1. Create a file `main.py`:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}
```

2. Run the server:

```bash
uvicorn main:app --reload
```

3. Interactive API docs:
- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## License

This project is licensed under the terms of the MIT license.
