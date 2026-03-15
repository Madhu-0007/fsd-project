import sqlite3
from flask import Flask, render_template, request, redirect, url_for, g, flash

app = Flask(__name__)
app.secret_key = 'ridepool_secret_2024'

DATABASE = 'ridepool.db'


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/post-ride', methods=['GET', 'POST'])
def post_ride():
    if request.method == 'POST':
        driver_name = request.form.get('driver_name', '').strip()
        driver_email = request.form.get('driver_email', '').strip()
        from_location = request.form.get('from_location', '').strip()
        to_location = request.form.get('to_location', '').strip()
        ride_date = request.form.get('ride_date', '').strip()
        ride_time = request.form.get('ride_time', '').strip()
        seats_available = request.form.get('seats_available', '').strip()
        price_per_seat = request.form.get('price_per_seat', '').strip()
        notes = request.form.get('notes', '').strip()

        # Basic server-side validation
        errors = []
        if not driver_name:
            errors.append('Driver name is required.')
        if not driver_email:
            errors.append('Driver email is required.')
        if not from_location:
            errors.append('From location is required.')
        if not to_location:
            errors.append('To location is required.')
        if from_location and to_location and from_location.lower() == to_location.lower():
            errors.append('From and To locations cannot be the same.')
        if not ride_date:
            errors.append('Ride date is required.')
        if not ride_time:
            errors.append('Ride time is required.')
        if not seats_available or not seats_available.isdigit() or int(seats_available) < 1:
            errors.append('Seats available must be at least 1.')
        try:
            price = float(price_per_seat)
            if price < 0:
                errors.append('Price per seat cannot be negative.')
        except (ValueError, TypeError):
            errors.append('Price per seat must be a valid number.')

        if errors:
            for err in errors:
                flash(err, 'danger')
            return render_template('post_ride.html',
                                   form_data=request.form)

        db = get_db()
        db.execute(
            '''INSERT INTO rides (driver_name, driver_email, from_location, to_location,
               ride_date, ride_time, seats_available, price_per_seat, notes)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (driver_name, driver_email, from_location, to_location,
             ride_date, ride_time, int(seats_available), float(price_per_seat), notes)
        )
        db.commit()
        flash('Your ride has been posted successfully! 🎉', 'success')
        return redirect(url_for('success', type='post'))

    return render_template('post_ride.html', form_data={})


@app.route('/search')
def search():
    from_q = request.args.get('from_location', '').strip()
    to_q = request.args.get('to_location', '').strip()
    date_q = request.args.get('ride_date', '').strip()

    db = get_db()
    query = 'SELECT * FROM rides WHERE 1=1'
    params = []

    if from_q:
        query += ' AND LOWER(from_location) LIKE ?'
        params.append(f'%{from_q.lower()}%')
    if to_q:
        query += ' AND LOWER(to_location) LIKE ?'
        params.append(f'%{to_q.lower()}%')
    if date_q:
        query += ' AND ride_date = ?'
        params.append(date_q)

    query += ' ORDER BY ride_date ASC, ride_time ASC'
    rides = db.execute(query, params).fetchall()

    return render_template('search_rides.html',
                           rides=rides,
                           from_q=from_q,
                           to_q=to_q,
                           date_q=date_q)


@app.route('/ride/<int:id>')
def ride_detail(id):
    db = get_db()
    ride = db.execute('SELECT * FROM rides WHERE id = ?', (id,)).fetchone()
    if ride is None:
        flash('Ride not found.', 'danger')
        return redirect(url_for('search'))
    return render_template('ride_detail.html', ride=ride)


@app.route('/request-ride/<int:ride_id>', methods=['POST'])
def request_ride(ride_id):
    db = get_db()
    ride = db.execute('SELECT * FROM rides WHERE id = ?', (ride_id,)).fetchone()
    if ride is None:
        flash('Ride not found.', 'danger')
        return redirect(url_for('search'))

    passenger_name = request.form.get('passenger_name', '').strip()
    passenger_email = request.form.get('passenger_email', '').strip()
    seats_requested = request.form.get('seats_requested', '').strip()
    message = request.form.get('message', '').strip()

    errors = []
    if not passenger_name:
        errors.append('Passenger name is required.')
    if not passenger_email:
        errors.append('Passenger email is required.')
    if not seats_requested or not seats_requested.isdigit():
        errors.append('Seats requested must be a valid number.')
    else:
        seats_int = int(seats_requested)
        if seats_int < 1:
            errors.append('Must request at least 1 seat.')
        elif seats_int > ride['seats_available']:
            errors.append(f'Only {ride["seats_available"]} seat(s) available.')

    if errors:
        for err in errors:
            flash(err, 'danger')
        return redirect(url_for('ride_detail', id=ride_id))

    db.execute(
        '''INSERT INTO requests (ride_id, passenger_name, passenger_email, seats_requested, message)
           VALUES (?, ?, ?, ?, ?)''',
        (ride_id, passenger_name, passenger_email, int(seats_requested), message)
    )
    # Decrement available seats
    db.execute(
        'UPDATE rides SET seats_available = seats_available - ? WHERE id = ?',
        (int(seats_requested), ride_id)
    )
    db.commit()

    return redirect(url_for('success', type='request'))


@app.route('/success')
def success():
    success_type = request.args.get('type', 'request')
    return render_template('request_success.html', success_type=success_type)


@app.route('/my-rides')
def my_rides():
    db = get_db()
    rides = db.execute('SELECT * FROM rides ORDER BY created_at DESC').fetchall()
    return render_template('my_rides.html', rides=rides)


# Initialise DB on startup (works with both gunicorn and flask dev server)
init_db()

if __name__ == '__main__':
    app.run(debug=True)
