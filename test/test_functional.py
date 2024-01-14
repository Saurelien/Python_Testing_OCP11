
from test.mocks import VALID_EMAIL, VALID_COMPETITIONS, ZERO_PLACES_COMPETITIONS,\
    CLUB_INVALID_ZERO_PTS, MAX_RESERVATION_COMPETITION, CLUB_VALID, INVALID_COMPETITION


def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    exped = f"Welcome to the GUDLFT Registration Portal!".encode('utf-8')
    assert exped in response.data


def test_valid_email(client, mock_clubs):
    #  Etape 1 email valide
    url = "/showSummary"
    data = {
        'email': VALID_EMAIL
    }
    response = client.post(url, data=data)
    assert response.status_code == 200
    exped = f"Welcome, {data['email']}"
    assert exped in str(response.data)


def test_invalid_email(client, mock_clubs):
    # Etape 2 email invalide
    url = "/showSummary"
    invalid_email = 'random@email.com'
    data = {
        'email': invalid_email
    }
    response = client.post(url, data=data)
    assert response.status_code == 200
    expected_response = f"Email non valide ou non existant, veuillez réessayer".encode('utf-8')
    assert expected_response in response.data


def test_booking_for_invalid_date(client, mock_competitions):
    data = {
        'name': INVALID_COMPETITION
    }
    response = client.get(f"/book/{data['name']}/club_name")
    assert response.status_code == 200
    expected_response = "La compétition a déjà eu lieu"
    expected_bytes_response = expected_response.encode('utf-8')
    assert expected_bytes_response in response.data


def test_reservation_13_places(client, mock_clubs, mock_competitions):
    response = client.post('/purchasePlaces', data={
        'competition': MAX_RESERVATION_COMPETITION,
        'club': CLUB_VALID,
        'places': '13'
    })
    assert response.status_code == 200
    expected_message = f"Le maximum de reservation est de 12.".encode('utf-8')
    assert expected_message in response.data


def test_reservation_between_1_and_12_places(client, mock_clubs, mock_competitions):
    response = client.post('/purchasePlaces', data={
        'competition': VALID_COMPETITIONS,
        'club': CLUB_VALID,
        'places': '12'
    })
    assert response.status_code == 200
    expected_message = "Super ! Réservation effectuée.".encode('utf-8')
    assert expected_message in response.data


def test_not_enough_places_in_competition(client, mock_clubs, mock_competitions):
    response = client.post('/purchasePlaces', data={
        'competition': ZERO_PLACES_COMPETITIONS,
        'club': CLUB_VALID,
        'places': '10'
    })
    assert response.status_code == 200
    expected_message = f"Pas assez de places disponibles.".encode('utf-8')
    assert expected_message in response.data


def test_not_enought_points_in_club(client, mock_clubs, mock_competitions):
    response = client.post('/purchasePlaces', data={
        'competition': VALID_COMPETITIONS,
        'club': CLUB_INVALID_ZERO_PTS,
        'places': '10'
    })
    assert response.status_code == 200
    expected_message = "Pas assez de points disponibles pour réserver cette quantité de places.".encode('utf-8')
    assert expected_message in response.data


def test_negative_competitions_places_reservation(client, mock_clubs, mock_competitions):
    response = client.post('/purchasePlaces', data={
        'competition': VALID_COMPETITIONS,
        'club': CLUB_VALID,
        'places': '-5'
    })
    assert response.status_code == 200
    expected_message = "Quantité de places invalide.".encode('utf-8')
    assert expected_message in response.data


def test_invalid_club(client, mock_clubs, mock_competitions):
    invalid_club_name = {
        "name": "Invalid Club"
    }
    response = client.post('/purchasePlaces', data={
        'competition': VALID_COMPETITIONS,
        'club': invalid_club_name,
        'places': '5'
    })
    assert response.status_code == 200
    assert b"Club invalide" in response.data


def test_invalid_competition(client, mock_clubs, mock_competitions):
    invalid_competition_name = {
        "name": "Invalid Competition"
    }
    response = client.post('/purchasePlaces', data={
        'competition': invalid_competition_name,
        'club': CLUB_VALID,
        'places': '5'
    })
    assert response.status_code == 200
    expected_byte_message = "Compétition invalide".encode('utf-8')
    assert expected_byte_message in response.data


def test_logout(client):
    logout_response = client.get('/logout', follow_redirects=True)
    expected_message = "Welcome to the GUDLFT Registration Portal!".encode('utf-8')
    assert expected_message in logout_response.data



