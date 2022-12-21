from typing import Any, Dict, List, Optional

from pydantic import AnyHttpUrl, BaseModel, validator


class Block(BaseModel):
    number: int
    gasLimit: int
    gasUsed: int
    difficulty: int
    totalDifficulty: int

    @validator(
        "*",
        pre=True,
        always=True,
    )
    def set_int(cls, v):
        if isinstance(v, str):
            return int(v, 16)
        return v


class Signature(BaseModel):
    name: str


class SignatureOut(BaseModel):
    data: List[Signature]
    page_size: int
    is_last_page: bool


class FourBytesSignatureResult(BaseModel):
    id: int
    created_at: str
    text_signature: str
    hex_signature: str
    bytes_signature: str


class FourBytesSignature(BaseModel):
    count: int
    next: Optional[AnyHttpUrl]
    previous: Optional[AnyHttpUrl]
    results: List[FourBytesSignatureResult]
    data: Optional[List[Signature]] = None

    @validator("data", pre=True, always=True)
    def assemble_data(cls, _, values: Dict[str, Any]) -> List[Signature]:
        return [Signature(name=value.text_signature) for value in values["results"]]
