from price_check import create_app
import pytest

@pytest.fixture
def app():
    yield create_app()

@pytest.fixture
def client(app):
    return app.test_client()

def test_def_page(app, client):
    res = client.get('/')
    assert res.status_code == 200

def test_home_page(app, client):
    res = client.get('/home')
    assert res.status_code == 200

def test_market_page(app, client):
    res = client.get('/market')

    assert res.status_code == 200
    assert b"Figures" in res.data