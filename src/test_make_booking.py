class TestMakeBooking(object):

    def setup_method(self):
        from src. AuthenticationManager import DummyAuthenticationManager
        self.system = system(DummyAuthenticationManager())
    
    def test_empty_start_location(self):
        start_location = ''
        end_location = 'Melbourne'
        start_date = '2018-5-20'
        end_date = '2018-5-23'
        num_days = 3
        location = Location(start_location, end_location)
        
        car = self.system.cars[0]
        user = self.system.login_customer('Matt', 'pass')
        
        self.system.make_booking(user, num_days, start_date, end_date, car, location)
        
        assert len(self.system._bookings) == 0
        
    
    def test_empty_end_location(self):
        start_location = 'Sydney'
        end_location = ''
        start_date = '2018-5-20'
        end_date = '2018-5-23'
        num_days = 3
        location = Location(start_location, end_location)
        
        car = self.system.cars[0]
        user = self.system.login_customer('Matt', 'pass')
        
        self.system.make_booking(user, num_days, start_date, end_date, car, location)
        
        assert len(self.system._bookings) == 0
        
    def test_empty_start_date(self):
        start_location = 'Sydney'
        end_location = 'Melbourne'
        start_date = ''
        end_date = '2018-5-23'
        num_days = 3
        location = Location(start_location, end_location)
        
        car = self.system.cars[0]
        user = self.system.login_customer('Matt', 'pass')
        
        self.system.make_booking(user, num_days, start_date, end_date, car, location)
        
        assert len(self.system._bookings) == 0
        
    def test_empty_start_date(self):
        start_location = 'Sydney'
        end_location = 'Melbourne'
        start_date = '2018-5-23'
        end_date = ''
        num_days = 3
        location = Location(start_location, end_location)
        
        car = self.system.cars[0]
        user = self.system.login_customer('Matt', 'pass')
        
        self.system.make_booking(user, num_days, start_date, end_date, car, location)
        
        assert len(self.system._bookings) == 0
     
    
    def test_invalid_period(self):
        start_location = 'Sydney'
        end_location = 'Melbourne'
        start_date = '2018-5-20'
        end_date = '2018-5-17'
        num_days = 3
        location = Location(start_location, end_location)
        
        car = self.system.cars[0]
        user = self.system.login_customer('Matt', 'pass')
        
        self.system.make_booking(user, num_days, start_date, end_date, car, location)
        
        assert len(self.system._bookings) == 0
        
        

tests = TestMakeBooking()
tests.setup_method()
tests.test_empty_start_location()
tests.test_empty_end_location()
tests.test_empty_start_date()
tests.test_empty_end_date()
test_invalid_period()
