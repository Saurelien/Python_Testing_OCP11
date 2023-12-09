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

    matching_clubs = [club for club in clubs if club.get('email') == email]

    if not email or not any(matching_clubs):
        flash("Email non valide ou non existant, veuillez réessayer")
        return render_template('index.html')
    club = matching_clubs[0]
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
def purchase_places():
    competition_name = request.form['competition']
    club_name = request.form['club']
    places_required = request.form['places']

    if not places_required or not places_required.isdigit() or int(places_required) <= 0:
        flash("Quantité de places invalide.")
        return redirect(url_for('index'))

    places_required = int(places_required)

    competition = next((c for c in competitions if c['name'] == competition_name), None)
    club = next((c for c in clubs if c['name'] == club_name), None)
    competition_places = int(competition['numberOfPlaces'])
    club_points = int(club['points'])

    if places_required > competition_places:
        flash("Pas assez de places disponibles.")
        return redirect(url_for('index'))

    if places_required > club_points:
        flash("Pas assez de points disponibles pour réserver cette quantité de places.")
        return render_template('index.html', club=club, competitions=competitions)

    # Test deduction des points lors du booking par le secretaire
    club_points -= places_required
    club['points'] = str(club_points)

    competition['numberOfPlaces'] = str(int(competition['numberOfPlaces']) - places_required)

    flash('Super ! Réservation effectuée.')
    return render_template('welcome.html', club=club, competitions=competitions)

# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
