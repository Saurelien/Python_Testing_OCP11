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
    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundclub = [c for c in clubs if c['name'] == club][0]
    foundcompetition = [c for c in competitions if c['name'] == competition][0]

    # Contrôle de la date de la compétition
    if foundclub and foundcompetition:
        competition_date = datetime.strptime(foundcompetition['date'], '%Y-%m-%d %H:%M:%S')
        current_date = datetime.now()

        if competition_date < current_date:
            flash("La compétition a déjà eu lieu. Vous ne pouvez pas réserver pour cette compétition.")
            return render_template('welcome.html', club=foundclub, competitions=competitions)

        # Si la compétition est valide, afficher la page de réservation
        return render_template('booking.html', club=foundclub, competition=foundcompetition)
    else:
        flash("Quelque chose s'est mal passé. Veuillez réessayer.")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces', methods=['POST'])
def purchaseplaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesrequired = int(request.form['places'])
    competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesrequired
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
