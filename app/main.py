import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.schema import Block


def get_application():
    _app = FastAPI(title=settings.PROJECT_NAME)

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return _app


app = get_application()


@app.get("/blocks/{block_number}", response_model=Block)
async def get_block(block_number: int):
    payload = {
        "id": "getblock.io",
        "jsonrpc": "2.0",
        "method": "eth_getBlockByNumber",
        "params": [hex(block_number), True],
    }
    headers = {
        "x-api-key": settings.BLOCK_API,
        "content-type": "application/json",
    }
    response = requests.post(settings.BLOCK_URL, json=payload, headers=headers)
    result = response.json().get("result")
    if result is None:
        raise HTTPException(status_code=404, detail="Block number not found")
    return result


@app.get("/signatures/{signature}")
async def get_signature(signature: str, page_size: int = 10, page_number: int = 1):
    pass
