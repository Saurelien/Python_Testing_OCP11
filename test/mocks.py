from datetime import datetime, timedelta

CLUB_INVALID_ZERO_PTS = "Club Valid Zero Pts"
CLUB_VALID = "Club Valid"
VALID_EMAIL = "valid@aa.aa"
MOCK_CLUBS = [
    {
        "name": CLUB_VALID,
        "email": VALID_EMAIL,
        "points": "53"
    },
    {
        "name": CLUB_INVALID_ZERO_PTS,
        "email": "invalid-zero-points@aa.aa",
        "points": "0"
    },
    {
        "name": "Club Invalid",
        "email": "invalid@aa.aa",
        "points": "0"
    }
]
next_week_date = datetime.now() + timedelta(days=7)
VALID_COMPETITION_DATE = next_week_date.isoformat()
MAX_RESERVATION_COMPETITION = "Max Reservation Competition"
ZERO_PLACES_COMPETITIONS = "Zero Place Competition"
VALID_COMPETITIONS = "Valid Competition"
INVALID_COMPETITION = "Invalid Competition"
MOCK_COMPETITIONS = [
    {
        "name": VALID_COMPETITIONS,
        "date": VALID_COMPETITION_DATE,
        "numberOfPlaces": "57"
    },
    {
        "name": ZERO_PLACES_COMPETITIONS,
        "date": VALID_COMPETITION_DATE,
        "numberOfPlaces": "0"
    },
    {
        "name": INVALID_COMPETITION,
        "date": "2020-10-22 13:30:00",
        "numberOfPlaces": "0"
    },
    {
        "name": MAX_RESERVATION_COMPETITION,
        "date": VALID_COMPETITION_DATE,
        "numberOfPlaces": "13"
    }
]
