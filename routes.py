from flask import render_template, request, redirect, url_for, abort
from flask_login import login_required, current_user

from server import app, system, auth_manager
from datetime import datetime
from src.Location import Location



@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Task 1: complete this function
    """
    if request.method == 'POST':
        
        username = request.form["username"]
        password = request.form["password"]
        
        check_user = system.login_customer(username, password)
        if (check_user):
             return redirect(url_for('cars'))
        else:
            # Next helps with redirecting the user to their previous page
            redir = request.args.get('next')
            return redirect(redir or url_for('home'))
    
    return render_template('login.html')



@app.route('/login_admin', methods=['POST'])
def login_admin():

    '''
    TASK 4.1 complete this function
    '''
    username = request.form["username"]
    password = request.form["password"]
        
    check_user = system.login_admin(username, password)
    if (check_user):
         return redirect(url_for('cars'))
    else:
        # Next helps with redirecting the user to their previous page
        redir = request.args.get('next')
        return redirect(redir or url_for('home'))



@app.route('/logout')
@login_required
def logout():
    auth_manager.logout()
    return redirect(url_for('home'))



'''
    Dedicated page for "page not found"
'''
@app.route('/404')
@app.errorhandler(404)
def page_not_found(e=None):
    return render_template('404.html'), 404



'''
    Search for Cars
'''
@app.route('/cars', methods=['POST', 'GET'])
@login_required
def cars():
    """
    Task 2: At the moment this endpoint does not do anything if a search
    is sent. It should filter the cars depending on the search criteria
    """
    cars = system.cars
    
    if request.method == 'POST':
    
        make = request.form["make"]
        model = request.form["model"]
        new_cars = system.car_search(make, model)
        return render_template('cars.html', cars = new_cars)
    
    return render_template('cars.html', cars = cars)



'''
    Display car details for the car with given rego
'''
@app.route('/cars/<rego>')
@login_required
def car(rego):
    car = system.get_car(rego)

    if not car:
        abort(404)

    return render_template('car_details.html', car=car)



'''
    Make a booking for a car with given rego
'''
@app.route('/cars/book/<rego>', methods=["GET", "POST"])
@auth_manager.customer_required
def book(rego):
    car = system.get_car(rego)

    if not car:
        abort(404)
    
    if request.method == 'POST':
        date_format = "%Y-%m-%d"
        start_date  = datetime.strptime(request.form['start_date'], date_format)
        end_date    = datetime.strptime(request.form['end_date'],   date_format)

        num_days = (end_date - start_date).days + 1

        if 'check' in request.form:
            fee = car.get_fee(num_days)
            
            return render_template(
                'booking_form.html',
                confirmation=True,
                form=request.form,
                car=car,
                fee=fee
            )

        elif 'confirm' in request.form:
            location = Location(request.form['start'], request.form['end'])
            booking  = system.make_booking(current_user, num_days, car, location)
    
            return render_template('booking_confirm.html', booking=booking)

    return render_template('booking_form.html', car=car)


'''
    Display list of all bookings for the car with given 'rego'
'''
@app.route('/cars/bookings/<rego>')
@login_required
def car_bookings(rego):
    """
    Task 3: This should render a new template that shows a list of all
    the bookings associated with the car represented by 'rego'
    """
    
    cars = system.cars
    for car in cars:
        if rego == car._rego:
            curr_car = car
    
    
    return render_template('bookings.html', car = curr_car, admin = False)


'''
    View all current bookings
'''
@app.route('/cars/bookings')
@auth_manager.admin_required
def all_bookings():

    '''
    Task 4.2: This should render a list of all current bookings
    on the system
    '''
    list_bookings = []
    cars = system.cars
    for car in cars:
        for booking in car._bookings:
            list_bookings.append(booking)
            
    return render_template('bookings.html', admin = True, all_bookings = list_bookings) 


'''
    Add a new car to the system
'''
from src.CarFactory import CarFactory
@app.route('/add_car', methods=['GET', 'POST'])
@auth_manager.admin_required
def add_car():

    '''
    Task 4.3: This should allow the admin to register
    new cars to the system, using the method provided
    in the CarFactory class.
    
    Provide meaningful message upon success
    '''
    factory = CarFactory()
    if request.method == 'POST':
        name = request.form['name']
        model = request.form['model']
        rego = request.form['rego']
        car_type = request.form['car-type']
        
        new_car = factory.make_car(name, model, rego, car_type)
        system.add_car(new_car)
        
        return render_template('car_register_form.html', success = True)
    

    return render_template('car_register_form.html')
