from google.appengine.ext import db

class User(db.Model):
    username = db.StringProperty(required = True)
    password = db.TextProperty(required = True)
    position = db.TextProperty(required = True)
	#position should be only manager, driver, kitchen_hands
    email = db.TextProperty()
    time = db.DateTimeProperty(auto_now_add = True)

class Timetable(db.Model):
    store = db.StringProperty(required = True)
    weekday = db.StringProperty(required = True)
    name = db.StringProperty(required = True)
    work_info = db.StringProperty()
    create_date = db.DateProperty(auto_now_add = True)