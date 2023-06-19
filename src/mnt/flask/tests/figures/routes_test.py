from price_check import create_app
import pytest

@pytest.fixture
def app():
    yield create_app()

@pytest.fixture
def client(app):
    return app.test_client()

def test_figures_page(app, client):
    res = client.get('/market/figures')

    assert res.status_code == 200
    assert b"Figures" in res.data
    assert b"Sorted by" in res.data

def test_figures_details_page(app, client):
    res = client.get('/market/figures/1862')

    assert res.status_code == 200
    assert b"Figures" in res.data
    assert b"Min Price" in res.data
    assert b"Max Price" in res.data
    assert b"Avg Price" in res.data