from pydantic import BaseModel, validator


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
