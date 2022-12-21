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


def test_read_signatures():
    response = client.get("/signatures/0x42dacf96")
    assert response.status_code == 200
    assert response.json() == {
        "data": [{"name": "setStakingManagerForPair(address,address)"}],
        "page_size": 10,
        "is_last_page": True,
    }


def test_read_signatures_pagination():
    response = client.get("/signatures/0x42d?page_size=5&page_number=2")
    assert response.status_code == 200
    assert response.json() == {
        "data": [
            {"name": "getDepositHistoryLength(address,address)"},
            {"name": "cancelExpenditure(uint256)"},
            {"name": "getNotificationReceiver(address)"},
            {"name": "updateBoxerNameConfigAddress(address)"},
            {"name": "claimNFT1155(address,uint256[],uint256[],uint256,uint256,bytes)"},
        ],
        "page_size": 5,
        "is_last_page": False,
    }


def test_read_signatures_nonexistent_signature():
    response = client.get("/signatures/tyz")
    assert response.status_code == 404
    assert response.json() == {"detail": "Signature not found"}


def test_read_signatures_invalid_page_number():
    response = client.get("/signatures/0x42dacf96?page_number=88")
    assert response.status_code == 404
    assert response.json() == {"detail": "Invalid page number"}
