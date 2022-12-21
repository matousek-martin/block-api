# Block API
A simple service to retrieve block and signature information on the Ethereum mainnet written in FastAPI.

# Blocks
Retrieve information about a given block number using `getblock.io`

### Endpoint
```
GET /blocks/{block_number}
```

### Response Model
```
class Block(BaseModel):
    number: int
    gasLimit: int
    gasUsed: int
    difficulty: int
    totalDifficulty: int
```

# Signatures
Retrieve EVM function signatures
### Endpoint
```
GET /signatures/{signature}
```
### Response Model
```
class SignatureOut(BaseModel):
    data: List[Signature]
    page_size: int
    is_last_page: bool
```

# Environment Variables
The docker-compose and Pydantic config gets all the values from a `.env` file.
Get the `BLOCK_API_KEY` from [GetBlock](https://getblock.io/). Example `.env` file below.
```
PROJECT_NAME=block-api
BACKEND_CORS_ORIGINS=["http://localhost:8000", "https://localhost:8000", "http://localhost", "https://localhost"]

POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_SERVER=database
POSTGRES_DB=app

BLOCK_API_KEY=<your-api-key>
```

# Run
Run the uvicorn service together with a PostgresSQL database on port 8000 by default
```
docker-compose up -d --build
```

# Next steps
- Create `blocks` and `signature` tables and record calls in a transactional PostgresSQL/MySQL database
- Add a caching solution, like `Redis`, and cache 'hottest' `block_numbers`/`signaturs` to improve performance
- Deploy to a Kubernetes cluster
