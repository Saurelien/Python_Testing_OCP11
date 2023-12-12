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
club_reservations = {}


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
    if foundclub and foundcompetition:
        return render_template('booking.html', club=foundclub,competition=foundcompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


def get_competition_by_name(name):
    return next((c for c in competitions if c['name'] == name), None)


def get_club_by_name(name):
    return next((c for c in clubs if c['name'] == name), None)


def check_quantity(places_required):
    if places_required is None:
        flash("Quantité de places non saisie.")
        return False

    try:
        places_required = int(places_required)
        if places_required <= 0:
            raise ValueError
    except ValueError:
        flash("Quantité de places invalide. Veuillez réessayer.")
        return False

    return places_required


def purchase_places():
    competition_name = request.form.get('competition')
    club_name = request.form.get('club')
    places_required = request.form.get('places')

    places_required = check_quantity(places_required)
    if places_required is None:
        return redirect(url_for('purchase_places'))

    competition = get_competition_by_name(competition_name)
    club = get_club_by_name(club_name)

    # Assurez-vous que les valeurs de points et de nombre de places sont des entiers
    club['points'] = int(club['points'])
    competition['numberOfPlaces'] = int(competition['numberOfPlaces'])

    # Vérifiez si le club a assez de points pour réserver
    if places_required > club['points']:
        flash(f"Points insuffisants pour réserver cette quantité de places. Pts du club:{club['points']}")
        return render_template('welcome.html')

    # Vérifiez si le total des places réservées dans cette compétition dépasse 12
    total_reserved_places = club.get('places_reserved', 0) + places_required
    if total_reserved_places > 12:
        flash("Vous ne pouvez pas réserver plus de 12 places pour cette compétition.")
        return redirect(url_for('index'))

    # Vérifiez et effectuez la réservation
    if places_required > competition['numberOfPlaces']:
        flash("Nombre de places insuffisant pour cette réservation.")
        return render_template('welcome.html')

    # Réduisez les points du club et le nombre de places disponibles dans la compétition
    club['points'] -= places_required
    competition['numberOfPlaces'] -= places_required

    # Mettez à jour le nombre total de places réservées par le club dans cette compétition
    club['places_reserved'] = club.get('places_reserved', 0) + places_required

    if club_name not in club_reservations:
        club_reservations[club_name] = {}

    if competition_name not in club_reservations[club_name]:
        club_reservations[club_name][competition_name] = places_required
    else:
        club_reservations[club_name][competition_name] += places_required

    return render_template('welcome.html', club=club, competitions=competitions)

# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
