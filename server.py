import json
from flask import Flask, render_template, request, redirect, flash, url_for


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

    club = [club for club in clubs if club.get('email') == email]

    if not email or not any(club):
        return "Email non valide ou non existant, veuillez réessayer"

    club = clubs[0]
    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundclub = [c for c in clubs if c['name'] == club][0]
    foundcompetition = [c for c in competitions if c['name'] == competition][0]
    if foundclub and foundcompetition:
        return render_template('booking.html', club=foundclub, competition=foundcompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces', methods=['POST'])
def purchaseplaces():
    competition_name = request.form['competition']
    club_name = request.form['club']
    places_required = int(request.form['places'])

    found_competition = next((c for c in competitions if c['name'] == competition_name), None)
    found_club = next((c for c in clubs if c['name'] == club_name), None)

    if not (found_competition and found_club):
        flash("Compétition ou club non trouvés.")
        return render_template('welcome.html', club=club_name, competitions=competitions)

    available_places = int(found_competition.get('numberOfPlaces', 0))
    club_points = int(found_club.get('points', 0))

    if places_required > available_places:
        flash("Désolé, pas assez de places disponibles.")
    elif places_required > club_points:
        flash("Le club ne dispose pas assez de points pour effectuer la réservation.")
    else:
        flash('Super ! Réservation effectuée avec succès !')
        found_competition['numberOfPlaces'] = str(available_places - places_required)
        found_club['points'] = str(club_points - places_required)

    return render_template('welcome.html', club=found_club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
