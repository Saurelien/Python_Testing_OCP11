import pytest

import server
from test.mocks import MOCK_CLUBS, MOCK_COMPETITIONS


@pytest.fixture
def client():
    app = server.app
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def mock_clubs(client):
    server.clubs = MOCK_CLUBS


@pytest.fixture
def mock_competitions(client):
    server.competitions = MOCK_COMPETITIONS
