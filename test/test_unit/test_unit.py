from datetime import datetime, timedelta
from http.client import responses

from test import mocks
from server import get_competition_by_name, get_club_by_name


def test_get_competition_success(mock_competitions):
    competition = get_competition_by_name(mocks.VALID_COMPETITIONS)
    assert competition["name"] == mocks.VALID_COMPETITIONS
    assert competition["date"] == mocks.VALID_COMPETITION_DATE


def test_get_competition_error(mock_competitions):
    competition = get_competition_by_name("Does not exist")
    assert competition is None


def test_get_club_success(mock_clubs):
    club = get_club_by_name(mocks.CLUB_VALID)
    assert club["name"] == mocks.CLUB_VALID
    assert club["email"] == mocks.VALID_EMAIL


def test_get_club_error(mock_clubs):
    club = get_club_by_name("random_email.com")
    assert club is None

def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"GUDLFT" in response.data

def test_show_summary_valid_email(client, mock_clubs):
    response = client.post('/showSummary', data={'email': mocks.VALID_EMAIL})
    assert response.status_code == 200
    assert b"Welcome" in response.data

def test_show_summary_invalid_email(client, mock_clubs):
    response = client.post('/showSummary', data={'email': 'fake@email.com'})
    assert response.status_code == 200
    assert b"Email non valide ou non existant" in response.data


def test_book(client, mock_clubs, mock_competitions):
    future_competition = {
        'name': 'Future Competition',
        'date': (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S'),
        'numberOfPlaces': 10
    }
    mocks.MOCK_COMPETITIONS.append(future_competition)

    response = client.get(f'/book/{future_competition["name"]}/{mocks.CLUB_VALID}')
    assert response.status_code == 200
    assert 'How many places?' in response.data.decode('utf-8')

    past_competition = {
        'name': 'Past Competition',
        'date': (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S'),
        'numberOfPlaces': 5
    }
    mocks.MOCK_COMPETITIONS.append(past_competition)

    response = client.get(f'/book/{past_competition["name"]}/{mocks.CLUB_VALID}')
    assert response.status_code == 200
    assert 'La compétition a déjà eu lieu' in response.data.decode('utf-8')
    assert 'How many places?' not in response.data.decode('utf-8')