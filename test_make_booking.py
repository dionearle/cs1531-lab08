class TestMakeBooking(object):

    def setup_method(self):
        from src. AuthenticationManager import DummyAuthenticationManager
        self.system = bootstrap_system(DummyAuthenticationManager())
    
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
        
        

tests = TestMakeBooking()
tests.setup_method()
tests.test_empty_start_location()
