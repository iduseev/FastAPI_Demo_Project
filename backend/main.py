#!/usr/bin/env python3
import uvicorn

from .endpoints import app


# driver code
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
