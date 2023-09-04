from apis import *
from tasks import *

# remember to run this line
# $env:PATH += ';C:\SQLite3'

api.add_resource(AddShow, '/api/show/add')
api.add_resource(AddScreen, '/api/screen/add')
api.add_resource(AddVenue, '/api/venue/add')
api.add_resource(AddCast, '/api/cast/add')
api.add_resource(DeleteCast, '/api/cast/<int:show_id>/<int:celebrity_id>')
api.add_resource(AddCelebrity, '/api/celebrity/add')
api.add_resource(AddTicket, '/api/ticket/add')
api.add_resource(AddRating, '/api/rating/add')
api.add_resource(AllUser, '/api/user/all')
api.add_resource(AllCelebrity, '/api/celebrity/all')
api.add_resource(AllScreen, '/api/screen/all')
api.add_resource(AllShow, '/api/show/all')
api.add_resource(AllVenue, '/api/venue/all')
api.add_resource(ShowRelated, '/api/show/<int:id1>')
api.add_resource(ScreenRelated, '/api/screen/<int:id1>')
api.add_resource(VenueRelated, '/api/venue/<int:id1>')
api.add_resource(DisplayVenue, '/api/venue/admin')
api.add_resource(AvailableSeats, '/api/seat/available')
api.add_resource(Booking, '/api/booking')
api.add_resource(AddTag, '/api/tag/add')
api.add_resource(TagRelated, '/api/tag/<int:tag_id>')
api.add_resource(AllTag, '/api/tag/all')
api.add_resource(UserRegistration, '/api/user/register')
api.add_resource(UserLogin, '/api/user/login')
api.add_resource(AdminLogin, '/api/admin/login')
api.add_resource(AddPhoto, '/api/photo/add')


#  celery -A app.Celery beat --max-interval 1 -l info
#  celery -A app.Celery worker --loglevel=INFO
#  ~/go/bin/MailHog

if __name__ == "__main__":
    # db.drop_all()
    # db.create_all()
    app.run(debug=True)
    