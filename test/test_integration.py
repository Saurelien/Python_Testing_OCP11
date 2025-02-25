from test import mocks


def test_integration(client, mock_clubs, mock_competitions):
    response_index = client.get('/')
    assert response_index.status_code == 200
    assert b"Welcome to the GUDLFT Registration Portal!" in response_index.data

    response_invalid_email = client.post('/showSummary', data={'email': 'random@email.com'})
    assert response_invalid_email.status_code == 200
    expected_invalid_email_message = "Email non valide ou non existant, veuillez réessayer".encode('utf-8')
    assert expected_invalid_email_message in response_invalid_email.data

    response = client.post('/purchasePlaces', data={
        'competition': mocks.VALID_COMPETITIONS,
        'club': mocks.CLUB_VALID,
        'places': '-5'
    })
    assert response.status_code == 200
    expected_message = "Quantité de places invalide.".encode('utf-8')
    assert expected_message in response.data

    invalid_club_name = {
        "name": "Invalid Club"
    }
    response = client.post('/purchasePlaces', data={
        'competition': mocks.VALID_COMPETITIONS,
        'club': invalid_club_name,
        'places': '5'
    })
    assert response.status_code == 200
    assert b"Club invalide" in response.data

    invalid_competition_name = {
        "name": "Invalid Competition"
    }
    response = client.post('/purchasePlaces', data={
        'competition': invalid_competition_name,
        'club': mocks.CLUB_VALID,
        'places': '5'
    })
    assert response.status_code == 200
    expected_byte_message = "Compétition invalide".encode('utf-8')
    assert expected_byte_message in response.data

    """Test verifier si la date de la compétition est invalide"""
    response_invalid_competition = client.get(f"/book/{mocks.INVALID_COMPETITION}/club_name")
    assert response_invalid_competition.status_code == 200
    expected_invalid_comp_message = "La compétition a déjà eu lieu".encode('utf-8')
    assert expected_invalid_comp_message in response_invalid_competition.data

    """test maximum de reservation de 12 places"""
    response_max_reservation = client.post('/purchasePlaces', data={
        'competition': mocks.MAX_RESERVATION_COMPETITION,
        'club': mocks.CLUB_VALID,
        'places': '13'
    })
    assert response_max_reservation.status_code == 200
    expected_max_reservation_message = b"Le maximum de reservation est de 12."
    assert expected_max_reservation_message in response_max_reservation.data

    response = client.post('/purchasePlaces', data={
        'competition': mocks.ZERO_PLACES_COMPETITIONS,
        'club': mocks.CLUB_VALID,
        'places': '10'
    })
    assert response.status_code == 200
    expected_message = f"Pas assez de places disponibles.".encode('utf-8')
    assert expected_message in response.data

    response = client.post('/purchasePlaces', data={
        'competition': mocks.VALID_COMPETITIONS,
        'club': mocks.CLUB_INVALID_ZERO_PTS,
        'places': '10'
    })
    assert response.status_code == 200
    expected_message = "Pas assez de points disponibles pour réserver cette quantité de places.".encode('utf-8')
    assert expected_message in response.data

    response_welcome = client.post('/showSummary', data={'email': mocks.VALID_EMAIL})
    assert response_welcome.status_code == 200
    assert b"Welcome, " + mocks.VALID_EMAIL.encode('utf-8') in response_welcome.data

    response = client.post('/purchasePlaces', data={
        'competition': mocks.VALID_COMPETITIONS,
        'club': mocks.CLUB_VALID,
        'places': '12'
    })
    assert response.status_code == 200
    expected_message = "Super ! Réservation effectuée.".encode('utf-8')
    assert expected_message in response.data

    response_logout = client.get('/logout', follow_redirects=True)
    assert response_logout.status_code == 200
    expected_logout_content = b"Welcome to the GUDLFT Registration Portal!"
    assert expected_logout_content in response_logout.data
