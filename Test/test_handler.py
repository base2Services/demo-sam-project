import pytest
from src.demo.app import lambda_handler

def test_handler_returns_api_payload():
    assert lambda_handler(None, None) == {'body': '{"environment": "dev", "status": "success!!"}', 'headers': {'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json'}, 'statusCode': 200}
