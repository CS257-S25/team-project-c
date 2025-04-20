'''Code for creating a UFO object along with creating a UFO class'''
class UFO:
    def __init__(self, year, city, description, state, country, latitude, longitude, shape, duration_seconds, duration_hours_or_mins, date_posted):
        self.year = year
        self.city = city
        self.description = description
        self.state = state
        self.country = country
        self.latitude = latitude
        self.longitude = longitude
        self.shape = shape
        self.duration_seconds = duration_seconds
        self.duration_hours_or_mins = duration_hours_or_mins
        self.date_posted = date_posted
