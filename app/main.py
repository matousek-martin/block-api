import requests
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.core.config import settings
from app.schema import Block, FourBytesSignature, SignatureOut


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
        "x-api-key": settings.BLOCK_API_KEY,
        "content-type": "application/json",
    }
    response = requests.post(
        settings.BLOCK_API_URL, json=payload, headers=headers
    ).json()

    result = response.get("result")
    if result is None:
        raise HTTPException(status_code=404, detail="Block number not found")
    return result


@app.get("/signatures/{signature}", response_model=SignatureOut)
async def get_signature(
    signature: str,
    page_size: int = Query(default=10, ge=1, le=10),
    page_number: int = Query(default=1, ge=1),
    signature_model: BaseModel = FourBytesSignature,
):
    # type: ignore
    params = {
        "hex_signature": signature,
        "page_size": page_size,
        "page": page_number,
    }
    headers = {
        "content-type": "application/json",
    }
    response = requests.get(
        settings.SIGNATURES_API_URL,
        params=params,  # type: ignore
        headers=headers,
    )
    sm = signature_model.parse_obj(response.json())
    return SignatureOut(
        data=sm.data,
        page_size=page_size,
        is_last_page=sm.next is None,
    )
