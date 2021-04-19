class Country:
    @staticmethod
    def get_all():
        return "SELECT * FROM Country"


class City:
    @staticmethod
    def get_all_by_country(country_id):
        return f"SELECT city_id, name FROM City WHERE country_id={country_id}"

    @staticmethod
    def get_by_id(city_id):
        return f"SELECT name FROM City WHERE city_id={city_id}"


class Station:
    @staticmethod
    def get_all_by_city(city_id):
        return f"SELECT station_id, name FROM Station WHERE city_id={city_id}"


class CarriageType:
    @staticmethod
    def get_by_id(carriage_type_id):
        return f"SELECT CarriageCounter.number_of_carriage, number_of_seats, price_rate FROM CarriageType " \
               f"INNER JOIN CarriageCounter ON CarriageType.carriage_type_id = CarriageCounter.carriage_type_id " \
               f"WHERE CarriageType.carriage_type_id = {carriage_type_id}"


class TrainType:
    @staticmethod
    def get_by_id(train_type_id):
        return f"SELECT CarriageCounter.number_of_carriage, CarriageType.number_of_seats, CarriageType.name, " \
               f"CarriageType.description, CarriageType.price_rate, CarriageType.carriage_type_id FROM TrainType " \
               f"INNER JOIN CarriageCounter ON TrainType.train_type_id=CarriageCounter.train_type_id " \
               f"INNER JOIN CarriageType ON CarriageCounter.carriage_type_id = CarriageType.carriage_type_id " \
               f"WHERE TrainType.train_type_id={train_type_id}"


class CarriageCounter:
    @staticmethod
    def add(train_type_id, carriage_type_id, number_of_seats):
        return f"INSERT INTO CarriageCounter(train_type_id, carriage_type_id, number_of_seats) VALUES(" \
                f"{train_type_id}, {carriage_type_id}, {number_of_seats})"


class PassengerType:
    @staticmethod
    def add(type_group, discount_cof):
        return f"INSERT INTO PassengerType(type_group, discount_cof) VALUES('{type_group}, {discount_cof}')"

    @staticmethod
    def get_discount(passenger_type_id):
        return f"SELECT discount_cof FROM PassengerType WHERE passenger_type_id={passenger_type_id}"

    @staticmethod
    def get_all():
        return "SELECT * FROM PassengerType"


class Passenger:
    @staticmethod
    def add(passenger_type_id, name, surname, patronymic, email):
        return f"INSERT INTO Passenger(passenger_type_id, name, surname, patronymic, email) " \
               f"VALUES({passenger_type_id}, '{name}', '{surname}', '{patronymic}', '{email}')"

    @staticmethod
    def get_by_email(email):
        return f"SELECT * FROM Passenger WHERE email='{email}'"


class Way:
    @staticmethod
    def add(train_type_id, departure_station_id, arrival_station_id, departure_time, arrival_time, transit_time, price):
        return f"INSERT INTO Way(train_type_id, departure_station_id, arrival_station_id, departure_time, arrival_time, transit_time, price) " \
               f"VALUES({train_type_id}, {departure_station_id}, {arrival_station_id}, '{departure_time}', '{arrival_time}', {transit_time} {price};"

    @staticmethod
    def get_all_info(departure_station_id, arrival_station_id):
        return f"SELECT Way.train_id, TrainType.name, d_city.name, d_station.name, a_city.name, a_station.name, departure_time, transit_time, transit_time, price, Way.train_type_id FROM Way " \
               f"INNER JOIN TrainType ON Way.train_type_id = TrainType.train_type_id " \
               f"INNER JOIN Station d_station ON Way.departure_station_id = d_station.station_id " \
               f"INNER JOIN Station a_station ON Way.arrival_station_id = a_station.station_id " \
               f"INNER JOIN City d_city ON d_station.city_id = d_city.city_id " \
               f"INNER JOIN City a_city ON a_station.city_id = a_city.city_id " \
               f"WHERE Way.departure_station_id = {departure_station_id} AND Way.arrival_station_id = {arrival_station_id}"

    @staticmethod
    def get_price(train_id):
        return f"SELECT price FROM Way WHERE train_id={train_id}"

    @staticmethod
    def get_time(train_id):
        return f"SELECT departure_time, transit_time FROM Way WHERE train_id={train_id}"


class Ticket:
    @staticmethod
    def add(passenger_id, train_id, carriage_type_id, carriage_number, place_number, departure_time, arrival_time, finally_price):
        return f"INSERT INTO Ticket(passenger_id, train_id, carriage_type_id, carriage_number, place_number, departure_time, arrival_time, finally_price) " \
               f"VALUES({passenger_id}, {train_id}, {carriage_type_id}, {carriage_number}, {place_number}, '{departure_time}', '{arrival_time}', {finally_price})"

    @staticmethod
    def get_count(date, train_id, carriage_type_id):
        return f"SELECT COUNT(ticket_id) FROM Ticket WHERE DATE(departure_time) = '{date}' AND train_id = {train_id} AND carriage_type_id = {carriage_type_id}"

    @staticmethod
    def get_reserved_places(date, train_id, carriage_type_id, carriage_number):
        return f"SELECT place_number FROM Ticket WHERE DATE(departure_time) = '{date}' AND train_id = {train_id} AND carriage_type_id = {carriage_type_id} AND carriage_number = {carriage_number}"

    @staticmethod
    def get(passenger_id, train_id):
        return f"SELECT ticket_id FROM Ticket WHERE passenger_id={passenger_id} AND train_id={train_id}"

    @staticmethod
    def get_all_info(ticket_id):
        return f"SELECT Passenger.name, Passenger.surname, Passenger.patronymic, PassengerType.type_group, Ticket.train_id, TrainType.name, d_country.name, d_city.name, d_station.name, a_country.name, a_city.name, a_station.name, Ticket.departure_time, Ticket.arrival_time, CarriageType.name, Ticket.carriage_number, Ticket.place_number, Ticket.finally_price FROM Ticket " \
               f"INNER JOIN Passenger on Ticket.passenger_id = Passenger.passenger_id INNER JOIN PassengerType ON Passenger.passenger_type_id = PassengerType.passenger_type_id " \
               f"INNER JOIN Way on Ticket.train_id = Way.train_id INNER JOIN TrainType ON Way.train_type_id = TrainType.train_type_id " \
               f"INNER JOIN Station d_station ON Way.departure_station_id = d_station.station_id INNER JOIN Station a_station ON Way.arrival_station_id = a_station.station_id " \
               f"INNER JOIN City d_city ON d_station.city_id = d_city.city_id INNER JOIN City a_city ON a_station.city_id = a_city.city_id " \
               f"INNER JOIN Country d_country ON d_city.country_id = d_country.country_id INNER JOIN Country a_country ON a_city.country_id = a_country.country_id " \
               f"INNER JOIN CarriageType on Ticket.carriage_type_id = CarriageType.carriage_type_id WHERE Ticket.ticket_id = {ticket_id}"