from src.Booking import Booking
import copy

class BookingError(Exception):

    def __init__(self, field, msg):
        self._field = field
        self._msg = msg


class CarRentalSystem:
    def __init__(self, admin_system, auth_manager):
        self._cars = []
        self._customers = []
        self._bookings = []
        self._admin_system = admin_system
        self._auth_manager = auth_manager


    '''
    Query Processing Services
    '''
    def car_search(self, name=None, model=None):
        new_cars = []
        for car in self._cars:
            if name == None:
                if model in car._model:
                   new_cars.append(car)
            elif model == None:
                if name in car._name:
                    new_cars.append(car)
            elif model != None and name != None:
                if name in car._name:
                    if model in car._model:
                       new_cars.append(car)
            else:
                new_cars.append(car)

        return new_cars


    def get_user_by_id(self, user_id):
        for c in self._customers:
            if c.get_id() == user_id:
                return c

        return self._admin_system.get_user_by_id(user_id)


    def get_car(self, rego):
        for c in self.cars:
            if c.rego == rego:
                return c
        return None



    '''
    Booking Services
    '''
    def make_booking(self, customer, period, start_date, end_date, car, location):
        # Prevent the customer from referencing 'current_user';
        # otherwise the customer recorded in each booking will be modified to
        # a different user whenever the current_user changes (i.e. when new user logs-in)
        try:
            if start_date == None:
                raise(BookingError(start_date,"Specify a valid start date"))
            elif end_date == None:
                raise(BookingError(end_date,"Specify a valid end date"))
            elif location.pickup == None:
                raise(BookingError(location.pickup,"Specify a valid start location"))
            elif location.dropoff == None:
                raise(BookingError(location.dropoff,"Specify a valid end location"))
            elif period <= 0:
                raise(BookingError(period,"Specify a valid period"))
        except BookingError:
            msg = self._msg
            return -1

        customer = copy.copy(customer)

        new_booking = Booking(customer, period, car, location)
        self._bookings.append(new_booking)
        car.add_booking(new_booking)
        return new_booking


    def check_fee(self, fee):
        if fee <= 0:
            fee = 1
        return fee
    '''
    Registration Services
    '''
    def add_car(self, car):
        self._cars.append(car)


    def add_customer(self, customer):
        self._customers.append(customer)



    '''
    Login Services
    '''

    def login_customer(self, username, password):
        for customer in self._customers:
            if self._auth_manager.login(customer, username, password):
                return True
        return False

    def login_admin(self, username, password):
        return self._admin_system.login(username, password)



    '''
    Properties
    '''
    @property
    def cars(self):
        return self._cars


    @property
    def bookings(self):
        return self._bookings
