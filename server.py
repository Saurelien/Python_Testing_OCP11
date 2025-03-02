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
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['JSON_AS_ASCII'] = False

competitions = loadcompetitions()
clubs = loadclubs()


@app.route('/')
def index():
    return render_template('index.html', club_data=clubs)


@app.route('/showSummary', methods=['POST'])
def show_summary():
    email = request.form['email']

    matching_clubs = [club for club in clubs if club.get('email') == email]
    club_data = [{'name': club['name'], 'points': club['points']} for club in clubs if club.get('email')]

    if not email or not any(matching_clubs):
        message = "Email non valide ou non existant, veuillez réessayer"
        flash(message)
        return render_template('index.html', club_data=clubs)
    club = matching_clubs[0]
    return render_template('welcome.html', club=club, club_data=club_data, competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition, club):
    found_club = ([c for c in clubs if c['name'] == club] or [None])[0]
    found_competition = ([c for c in competitions if c['name'] == competition] or [None])[0]
    competition_date = datetime.strptime(found_competition['date'], '%Y-%m-%d %H:%M:%S')
    current_date = datetime.now()
    if competition_date < current_date:
        message = "La compétition a déjà eu lieu. Date de la compétition"
        flash(f"{message}: {found_competition}.")
        return render_template('welcome.html', club=found_club, competitions=competitions, club_data=clubs)
    return render_template('booking.html', club=found_club, competition=found_competition)


"""Fonctions auxiliaire"""


def get_competition_by_name(name):
    return next((c for c in competitions if c['name'] == name), None)


def get_club_by_name(name):
    return next((c for c in clubs if c['name'] == name), None)


@app.route('/purchasePlaces', methods=['POST'])
def purchase_places():
    competition_name = request.form['competition']
    club_name = request.form['club']
    places_required = int(request.form['places'])
    messages = list()

    if places_required <= 0:
        messages.append("Quantité de places invalide.")

    if places_required > 12:
        messages.append("Le maximum de reservation est de 12.")

    competition = get_competition_by_name(competition_name)

    if not competition:
        messages.append("Compétition invalide")

    club = get_club_by_name(club_name)
    if not club:
        messages.append("Club invalide")

    if messages:
        for message in messages:
            flash(message)
        return render_template('welcome.html', club=club, competitions=competitions, club_data=clubs)

    competition_places = int(competition['numberOfPlaces'])
    club_points = int(club['points'])

    if places_required > competition_places:
        messages.append(f"Pas assez de places disponibles.")

    if places_required > club_points:
        messages.append(f"Pas assez de points disponibles pour réserver cette quantité de places.")

    if messages:
        for message in messages:
            flash(message)
        return render_template('welcome.html', club=club, competitions=competitions, club_data=clubs)

    club_points -= places_required
    club['points'] = str(club_points)
    competition_places -= places_required
    competition['numberOfPlaces'] = str(competition_places)
    flash(f"Super ! Réservation effectuée. Nombre de places reservées: {places_required}")
    return render_template('welcome.html', club=club, competitions=competitions, club_data=clubs)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
