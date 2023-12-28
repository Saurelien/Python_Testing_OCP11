import json
from flask import Flask, render_template, request, redirect, flash, url_for
from datetime import datetime


def loadclubs():
    with open('clubs.json') as c:
        listofclubs = json.load(c)['clubs']
    return listofclubs


def loadcompetitions():
    with open('competitions.json') as comps:
        listofcompetitions = json.load(comps)['competitions']

    return listofcompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadcompetitions()
clubs = loadclubs()
club_reservations = {}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def showsummary():
    email = request.form['email']

    matching_clubs = [club for club in clubs if club.get('email') == email]
    club_data = [{'name': club['name'], 'points': club['points']} for club in clubs if club.get('email') != email]

    if not email or not any(matching_clubs):
        return "Email non valide ou non existant, veuillez réessayer"

    club = matching_clubs[0]
    return render_template('welcome.html', club=club, club_data=club_data, competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundclub = next((c for c in clubs if c['name'] == club), None)
    foundcompetition = next((c for c in competitions if c['name'] == competition), None)
    competition_date = datetime.strptime(foundcompetition['date'], '%Y-%m-%d %H:%M:%S')
    current_date = datetime.now()
    if competition_date < current_date:
        flash(f"La compétition a déjà eu lieu. Date de la compétition: {foundcompetition['date']}.")
        return render_template('welcome.html', club=foundclub, competitions=competitions)
    return render_template('booking.html', club=foundclub, competition=foundcompetition)


"""Fonctions auxiliaire"""


def get_competition_by_name(name):
    return next((c for c in competitions if c['name'] == name), None)


def get_club_by_name(name):
    return next((c for c in clubs if c['name'] == name), None)


def get_total_reserved_places(club_name, competition_name):
    total_reserved = 0
    if club_name in club_reservations and competition_name in club_reservations[club_name]:
        total_reserved = club_reservations[club_name][competition_name]
    print(club_reservations)
    return total_reserved


@app.route('/purchasePlaces', methods=['POST'])
def purchase_places():
    competition_name = request.form['competition']
    club_name = request.form['club']
    places_required = int(request.form['places'])

    if places_required <= 0:
        flash("Quantité de places invalide.")
        return render_template('welcome.html', competitions=competitions)

    competition = get_competition_by_name(competition_name)
    club = get_club_by_name(club_name)

    competition_places = int(competition['numberOfPlaces'])
    club_points = int(club['points'])
    total_reserved_places = get_total_reserved_places(club_name, competition_name)  # Modification ici

    if places_required > competition_places:
        flash(f"Pas assez de places disponibles. Places restantes : {competition_places}")
        return render_template('welcome.html', club=club, competitions=competitions)

    if places_required > club_points:
        flash(
            f"Pas assez de points disponibles pour réserver cette quantité de places."
            f" Points restants du club : {club_points}")
        return render_template('welcome.html', club=club, competitions=competitions)

    if total_reserved_places + places_required > 12:
        flash(
            f"Le maximum de reservation est de 12."
            f" Places déjà réservées : {total_reserved_places}")
        return render_template('welcome.html', club=club, competitions=competitions)

    club_points -= places_required
    club['points'] = str(club_points)

    competition_places -= places_required
    competition['numberOfPlaces'] = str(competition_places)

    if club_name not in club_reservations:
        club_reservations[club_name] = {}

    club_reservations[club_name][competition_name] = club_reservations[club_name].get(competition_name,
                                                                                      0) + places_required
    print(club_reservations)
    flash(f'Super ! Réservation effectuée.Points restants du club : {club_points}')

    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
