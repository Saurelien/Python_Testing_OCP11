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


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def showsummary():
    email = request.form['email']

    matching_clubs = [club for club in clubs if club.get('email') == email]

    if not email or not any(matching_clubs):
        return "Email non valide ou non existant, veuillez réessayer"

    club = matching_clubs[0]
    valid_competitions = [c for c in competitions if
                          datetime.strptime(c['date'], '%Y-%m-%d %H:%M:%S') > datetime.now()]
    flash(f"Calendrier des compétition disponible {valid_competitions}")
    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundclub = next((c for c in clubs if c['name'] == club), None)
    foundcompetition = next((c for c in competitions if c['name'] == competition), None)
    if not foundclub or not foundcompetition:
        return render_template('welcome.html', club=club, competitions=competitions)
    competition_date = datetime.strptime(foundcompetition['date'], '%Y-%m-%d %H:%M:%S')
    current_date = datetime.now()
    if competition_date < current_date:
        flash(f"La compétition a déjà eu lieu. Date de la compétition : {foundcompetition['date']}.")
        return render_template('welcome.html', club=foundclub, competitions=competitions)
    return render_template('booking.html', club=foundclub, competition=foundcompetition)


@app.route('/purchasePlaces', methods=['POST'])
def purchaseplaces():
    competition = next(c for c in competitions if c['name'] == request.form['competition'])
    club = next(c for c in clubs if c['name'] == request.form['club'])
    places_required = int(request.form['places'])
    competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - places_required
    club['points'] = str(int(club['points']) - places_required)
    flash(f'Super! Réservation réussie! [Points du club restants: {club["points"]}]')
    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
