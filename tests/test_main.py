from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_read_blocks():
    response = client.get("/blocks/26803")
    assert response.status_code == 200
    assert response.json() == {
        "number": 26803,
        "gasLimit": 8000000,
        "gasUsed": 0,
        "difficulty": 1,
        "totalDifficulty": 46589,
    }


def test_read_blocks_invalid_block_num():
    response = client.get("/blocks/abc123!@")
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["path", "block_number"],
                "msg": "value is not a valid integer",
                "type": "type_error.integer",
            }
        ]
    }


def test_read_blocks_nonexistent_block_num():
    response = client.get("/blocks/12345678987654321")
    assert response.status_code == 404
    assert response.json() == {"detail": "Block number not found"}
