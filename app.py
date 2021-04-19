from flask import Flask, redirect, render_template, request, abort
from service import db_connector
from service.sql_requests_creator import *
from datetime import datetime, time, timedelta

app = Flask(__name__)
connection = db_connector.create_connection('localhost', '3307', 'root', 'lololowka00', 'Railway')

@app.route('/')
def index():
    return redirect('/countries')


@app.route('/countries', methods=['GET', 'POST'])
def countries():
    if request.method == 'POST':
        departure_country_id = request.form['country1']
        arrival_country_id = request.form['country2']
        return redirect(f'/cities/{departure_country_id}/{arrival_country_id}')
    countries = db_connector.execute_read_query(connection, Country.get_all())
    return render_template('countries.html', countries=countries)


@app.route('/cities/<departure_country_id>/<arrival_country_id>', methods=['GET', 'POST'])
def cities(departure_country_id, arrival_country_id):
    if request.method == 'POST':
        departure_city_id = request.form['city1']
        arrival_city_id = request.form['city2']
        return redirect(f'/station/{departure_city_id}/{arrival_city_id}')
    arrival_cities = db_connector.execute_read_query(connection, City.get_all_by_country(arrival_country_id))
    departure_cities = db_connector.execute_read_query(connection, City.get_all_by_country(departure_country_id))
    return render_template('cities.html', arrival_cities=arrival_cities, departure_cities=departure_cities)


@app.route('/station/<departure_city_id>/<arrival_city_id>', methods=['GET', 'POST'])
def station(departure_city_id, arrival_city_id):
    if request.method == 'POST':
        departure_station_id = request.form['station1']
        arrival_station_id = request.form['station2']
        date = request.form['date']
        return redirect(f'/trains/{departure_station_id}/{arrival_station_id}/{date}')
    cities = [db_connector.execute_read_query(connection, City.get_by_id(arrival_city_id))[0][0],
              db_connector.execute_read_query(connection, City.get_by_id(departure_city_id))[0][0]]
    arrival_stations = db_connector.execute_read_query(connection, Station.get_all_by_city(arrival_city_id))
    departure_stations = db_connector.execute_read_query(connection, Station.get_all_by_city(departure_city_id))
    return render_template('station.html', cities=cities, arrival_stations=arrival_stations, departure_stations=departure_stations)


@app.route('/trains/<departure_station_id>/<arrival_station_id>/<date>', methods=['GET', 'POST'])
def get_trains(departure_station_id, arrival_station_id, date):
    if request.method == 'POST':
        data = request.form['buy'].split(';')
        train_id = data[0]
        carriage_type_id = data[1]
        return redirect(f'/train/{train_id}/{carriage_type_id}/{date}')
    trains = db_connector.execute_read_query(connection, Way.get_all_info(departure_station_id, arrival_station_id))
    trains_carriages = []
    times = []
    for x in range(0, len(trains)):
        carriages = db_connector.execute_read_query(connection, TrainType.get_by_id(trains[x][10]))
        trains_carriages.append([])
        date_data = date.split('-')
        departure_time_data = str(trains[x][6]).split(':')
        departure_time = datetime(int(date_data[0]), int(date_data[1]), int(date_data[2]), int(departure_time_data[0]),
                                  int(departure_time_data[1]))
        transit_time = trains[x][7]
        arrival_time = departure_time + transit_time
        times.append([departure_time, arrival_time, transit_time.seconds//3600])
        for i in range(0, len(carriages)): # add all info
            trains_carriages[x].append([])
            reserved_places = db_connector.execute_read_query(connection, Ticket.get_count(date, trains[x][0], carriages[i][5]))[0][0]
            free_places = int(carriages[i][0]) * int(carriages[i][1]) - int(reserved_places)
            price = float(trains[x][9]) * carriages[i][4]
            trains_carriages[x][i].append(carriages[i][2])
            trains_carriages[x][i].append(carriages[i][3])
            trains_carriages[x][i].append(free_places)
            trains_carriages[x][i].append(price)
            trains_carriages[x][i].append(carriages[i][5])
    return render_template('trains.html', trains=trains, trains_carriages=trains_carriages, times=times)


@app.route('/train/<train_id>/<carriage_type_id>/<date>', methods=['GET', 'POST'])
def train(train_id, carriage_type_id, date):
    passenger_info = ['', '', '', '', '', '', '']
    places = []
    finally_price = None
    carriage_info = db_connector.execute_read_query(connection, CarriageType.get_by_id(carriage_type_id))[0]
    if request.method == 'POST':
        passenger_info = [request.form.get('email'), request.form.get('surname'), request.form.get('name'),
                          request.form.get('patronymic'), request.form['passenger_type'], request.form['carriage'], '']
        price = db_connector.execute_read_query(connection, Way.get_price(train_id))[0][0]
        rate = carriage_info[2]
        discount = db_connector.execute_read_query(connection, PassengerType.get_discount(passenger_info[4]))[0][0]
        if request.form['submit_button'] == 'Підтвердити номер вагону':
            reserved_places = db_connector.execute_read_query(connection, Ticket.get_reserved_places(date, train_id, carriage_type_id, passenger_info[5]))
            places = [x for x in range(1, carriage_info[1]+1)]
            for place in reserved_places:
                places.remove(place[0])
        if request.form['submit_button'] == 'Підтвердити номер місця':
            reserved_places = db_connector.execute_read_query(connection, Ticket.get_reserved_places(date, train_id, carriage_type_id, passenger_info[5]))
            places = [x for x in range(1, carriage_info[1]+1)]
            for place in reserved_places:
                places.remove(place[0])
            passenger_info[6] = request.form['place']
            finally_price = float(price) * float(rate) * float(discount)
        if request.form['submit_button'] == 'Купити квиток':
            passenger_info[6] = request.form['place']
            finally_price = float(price) * float(rate) * float(discount)
            passenger = db_connector.execute_read_query(connection, Passenger.get_by_email(passenger_info[0]))
            if len(passenger) == 0:  # if passenger is not exist in db
                db_connector.execute_query(connection, Passenger.add(
                    passenger_info[4], passenger_info[2], passenger_info[1], passenger_info[3], passenger_info[0]))
            passenger = db_connector.execute_read_query(connection, Passenger.get_by_email(passenger_info[0]))
            passenger_id = passenger[0][0]
            times = db_connector.execute_read_query(connection, Way.get_time(train_id))[0]
            date_data = date.split('-')
            departure_time_data = str(times[0]).split(':')
            departure_time = datetime(int(date_data[0]), int(date_data[1]), int(date_data[2]), int(departure_time_data[0]), int(departure_time_data[1]))
            transit_time = times[1]
            arrival_time = departure_time + transit_time
            db_connector.execute_query(connection, Ticket.add(passenger_id, train_id, carriage_type_id, passenger_info[5], passenger_info[6], departure_time, arrival_time, finally_price))
            ticket_id = db_connector.execute_read_query(connection, Ticket.get(passenger_id, train_id))[0][0]
            return redirect(f'/ticket/{ticket_id}')
    passenger_types = db_connector.execute_read_query(connection, PassengerType.get_all())
    carriages = [x for x in range(1, carriage_info[0]+1)]
    return render_template('train.html', passenger_types=passenger_types, carriages=carriages, places=places,
                           passenger_info=passenger_info, finally_price=finally_price)


@app.route('/ticket/<ticket_id>')
def ticket(ticket_id):
    try:
        ticket_info = db_connector.execute_read_query(connection, Ticket.get_all_info(ticket_id))[0]
    except:
        abort(404, description="Ticket not found")
    return render_template('ticket.html', ticket_info=ticket_info)


if __name__ == '__main__':
    app.run()
