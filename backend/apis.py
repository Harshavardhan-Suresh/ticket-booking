from time import perf_counter_ns
import ast
import redis
from flask import request
from sqlalchemy import and_, func, exists
from flask_restful import Resource, abort
from datetime import datetime
from flask_bcrypt import Bcrypt
from functools import wraps
from tasks import *
bcrypt = Bcrypt(app)
r = redis.StrictRedis(host='localhost', port=6379, db=0)


def evict_cache(key):
    r.delete(key)


def verify_user_credentials(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        verify_jwt_in_request()
        current_user = get_jwt_identity()
        email = current_user.get('email')
        password = current_user.get('password')
        if isinstance(password, bytes):
            password = password.decode('utf-8')
        user_valid = User.query.filter_by(email=email).first()
        if isinstance(user_valid.password, bytes):
            user_valid.password = user_valid.password.decode('utf-8')
        if user_valid and user_valid.password == password:
            return func(*args, **kwargs)
        else:
            return {'message': 'Unauthorized access'}, 401
    return decorated_function


def verify_admin_credentials(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        verify_jwt_in_request()
        current_user = get_jwt_identity()
        email = current_user.get('email')
        password = current_user.get('password')
        u_type = current_user.get('u_type')
        user_valid = User.query.filter_by(
            email=email, password=password, u_type='admin').first() is not None
        if user_valid and u_type == 'admin':
            return func(*args, **kwargs)
        else:
            return {'message': 'Unauthorized access'}, 401
    return decorated_function


class AddRating(Resource):
    @verify_user_credentials
    def post(self):
        evict_cache('allShow')
        data = request.get_json()
        show = Show.query.filter_by(id=data['show_id']).first()
        if show:
            user = User.query.filter_by(id=data['user_id']).first()
            if user:
                ratingPresent = Rating.query.filter_by(
                    show_id=data['show_id'], user_id=data['user_id']).first()
                if ratingPresent:
                    return {"error": "Rating already present"}, 402
                if int(data['rating']) <= 0:
                    return {"error": "Rating can't be negative"}, 404
                if isinstance(data['rating'], int) or data['rating'].isdigit():
                    new_rating = Rating(show_id=data['show_id'], user_id=data['user_id'], rating=int(
                        data['rating']), added_at=datetime.now())
                    db.session.add(new_rating)
                    db.session.commit()
                    return {"message": "Rating created successfully."}, 200
                else:
                    return {"error": "Rating must be integer."}, 403
            else:
                return {"error": "User does not exist"}, 405
        else:
            return {"error": "Show does not exist"}, 404


class AddTicket(Resource):
    @verify_user_credentials
    def post(self):
        evict_cache('allShow')
        data = request.get_json()
        screen = Screen.query.filter_by(id=data['screen_id']).first()
        if screen:
            user = User.query.filter_by(id=data['user_id']).first()
            if user:
                if isinstance(data['no_of_seats'], int) or data['no_of_seats'].isdigit():
                    if int(data['no_of_seats']) <= 0:
                        return {"error": "No of seats can't be negative"}, 402
                    booked_tickets = db.session.query(func.count(Ticket.no_of_seats)).filter_by(
                        screen_id=data['screen_id']).scalar()
                    booked_seats = 0
                    if booked_tickets:
                        booked_seats = db.session.query(func.sum(Ticket.no_of_seats)).filter_by(
                            screen_id=data['screen_id']).scalar()
                    capacity = db.session.query(Venue.capacity).join(
                        Screen, Screen.venue_id == Venue.id).filter(Screen.id == data['screen_id']).scalar()
                    available_seats = capacity - booked_seats
                    if available_seats < int(data['no_of_seats']):
                        return {"error": "No of seats is more than the available tickets"}, 403
                    price_inc = 0
                    # 25 % percent
                    if booked_seats * 4 <= capacity and (booked_seats + int(data['no_of_seats'])) * 4 > capacity:
                        price_inc = 0.1
                    # 50% percent
                    if booked_seats * 2 <= capacity and (booked_seats + int(data['no_of_seats'])) * 2 > capacity:
                        price_inc += 0.2
                    # 75% percent
                    if booked_seats * 4 <= 3 * capacity and (booked_seats + int(data['no_of_seats'])) * 4 > 3 * capacity:
                        price_inc += 0.2
                    # TODO - update price in database
                    price = screen.price
                    new_ticket = Ticket(screen_id=data['screen_id'], total_price=int(
                        data['no_of_seats']) * price,  user_id=data['user_id'], no_of_seats=int(data['no_of_seats']))
                    db.session.add(new_ticket)
                    if price_inc > 0:
                        new_price = screen.price * (1 + price_inc)
                        screen.price = new_price
                    db.session.commit()
                    return {"message": "ticket created successfully."}, 200
                else:
                    return {"error": "No_of_seats must be integer"}, 401
            else:
                return {"error": "User does not exist"}, 405
        else:
            return {"error": "Screen does not exist"}, 404


class AvailableSeats(Resource):
    @verify_user_credentials
    def get(self):
        screen_id = request.args.get('screen_id')
        screen = Screen.query.filter_by(id=screen_id).first()
        if screen:
            booked_tickets = db.session.query(func.count(
                Ticket.no_of_seats)).filter_by(screen_id=screen_id).scalar()
            booked_seats = 0
            if booked_tickets:
                booked_seats = db.session.query(func.sum(Ticket.no_of_seats)).filter_by(
                    screen_id=screen_id).scalar()
            capacity = db.session.query(Venue.capacity).join(
                Screen, Screen.venue_id == Venue.id).filter(Screen.id == screen_id).scalar()
            available_seats = capacity - booked_seats
            return {"available_seats": available_seats}, 200
        else:
            return {"error": "Screen does not exist", "available_seats": 0}, 404


class AddCelebrity(Resource):
    @verify_admin_credentials
    def post(self):
        evict_cache('allCelebs')
        data = request.get_json()
        photo1 = '/images/no_image.png'
        if "photo" in data.keys():
            photo1 = data["photo"]
        new_celebrity = Celebrity(name=data['name'], photo=photo1)
        db.session.add(new_celebrity)
        db.session.commit()
        return {"message": "celebrity created successfully."}, 200


class AddPhoto(Resource):
    @verify_admin_credentials
    def post(self):
        if ('photo' in request.files):
            photo = request.files['photo']
            filename = secure_filename(photo.filename)
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            photo_path = '/images/' + filename
        else:
            photo_path = ""
        return {"photo_path": photo_path}, 200


class DeleteCast(Resource):
    @verify_admin_credentials
    def delete(self, show_id, celebrity_id):
        evict_cache('allShow')
        if db.session.query(cast).filter_by(celebrity_id=celebrity_id, show_id=show_id).first():
            cast_entry = cast.delete().where(cast.c.celebrity_id ==
                                             celebrity_id).where(cast.c.show_id == show_id)
            db.session.execute(cast_entry)
            db.session.commit()
            return {"message": "celebrity deleted successfully."}, 200
        else:
            return {"message": "celebrity is not part of the show"}, 404


class AddShow(Resource):
    @verify_admin_credentials
    def post(self):
        evict_cache('allShow')
        data = request.get_json()
        poster1 = '/images/no_image.png'
        if "poster" in data.keys():
            poster1 = data['poster']
        new_show = Show(name=data['name'], poster=poster1)
        tags_data = data.get('tags', [])
        for tag_data in tags_data:
            tag_id = tag_data.get('id')
            tag_name = tag_data.get('name')
            if tag_id and tag_name:
                tag = Tag.query.get(tag_id)
                if tag and tag.name == tag_name:
                    new_show.tags.append(tag)
        db.session.add(new_show)
        db.session.commit()
        return {"message": "Show created successfully."}, 200


class Booking(Resource):
    @verify_user_credentials
    def get(self):
        user_id = request.args.get('user_id')
        tickets = Ticket.query.filter_by(user_id=user_id).all()
        ticket_list = []
        for ticket in tickets:
            screen = Screen.query.filter_by(id=ticket.screen_id).first()
            venue = Venue.query.filter_by(id=screen.venue_id).first()
            show = Show.query.filter_by(id=screen.show_id).first()
            ticket_data = {
                "ticket_id": ticket.id,
                "screen_id": ticket.screen_id,
                "show_name": show.name,
                "show_poster": show.poster,
                "venue_name": venue.name,
                "time_and_date": str(screen.timing.strftime("%d %B, %Y %I:%M %p")),
                "no_of_seats": ticket.no_of_seats,
                "total_price": ticket.total_price
            }
            ticket_list.append(ticket_data)
        return {'tickets': ticket_list}, 200


class AddVenue(Resource):
    @verify_admin_credentials
    def post(self):
        evict_cache('displayVenue')
        evict_cache('allVenue')
        data = request.get_json()
        if isinstance(data['capacity'], int) or data['capacity'].isdigit():
            if int(data['capacity']) <= 0:
                return {"error": "Capacity can't be negative"}, 402
            new_venue = Venue(name=data['name'], city=data['city'],
                              address=data['address'], capacity=int(data['capacity']))
            db.session.add(new_venue)
            db.session.commit()
            return {"message": "Venue created successfully."}, 200
        else:
            return {"error": "Capacity must be integer"}, 404


class AddScreen(Resource):
    @verify_admin_credentials
    def post(self):
        evict_cache('displayVenue')
        data = request.get_json()
        show = Show.query.filter_by(id=data['show_id']).first()
        if show:
            venue = Venue.query.filter_by(id=data['venue_id']).first()
            if venue:
                new_screen = Screen(timing=datetime.strptime(
                    data['timing'], "%Y/%m/%d %H:%M:%S"), price=data['price'], venue_id=data['venue_id'], show_id=data['show_id'])
                db.session.add(new_screen)
                db.session.commit()
                return {"message": "Screen created successfully."}, 200
            else:
                return {"error": "Venue does not exist"}, 404
        else:
            return {"error": "Show does not exist"}, 405


class AddCast(Resource):
    @verify_admin_credentials
    def post(self):
        evict_cache('allShow')
        data = request.get_json()
        show = Show.query.filter_by(id=data['show_id']).first()
        if (show):
            celebrity = Celebrity.query.filter_by(
                id=data['celebrity_id']).first()
            if (celebrity):
                if db.session.query(cast).filter_by(celebrity_id=data['celebrity_id'], show_id=data['show_id']).first():
                    return {"error": "Celebrity is already part of the show cast"}, 403
                insert = cast.insert().values(
                    show_id=data['show_id'], celebrity_id=data['celebrity_id'])
                db.session.execute(insert)
                db.session.commit()
                return {"message": "Cast created successfully."}, 200
            else:
                return {"error": "Celebrity does not exist"}, 404
        else:
            return {"error": "Show does not exist"}, 405


class AllCelebrity(Resource):
    @verify_user_credentials
    def get(self):
        start = perf_counter_ns()
        cached_data = r.get('allCelebs')
        if cached_data is not None:
            if isinstance(cached_data, bytes):
                cached_data = cached_data.decode('utf-8')
            stop = perf_counter_ns()
            print("Time taken cache", stop - start)
            return ast.literal_eval(cached_data), 200
        celebrity = Celebrity.query.all()
        celebrity_field = {}
        celebrity_field['celebrities'] = []
        if celebrity:
            for x in celebrity:
                celebrity_field["celebrities"].append(
                    {"id": x.id, "name": x.name, "photo": x.photo})
        stop = perf_counter_ns()
        print("Time taken w/o cache", stop - start)
        r.set('allCelebs', str(celebrity_field), ex=60)
        return celebrity_field, 200


class AllUser(Resource):
    @verify_user_credentials
    def get(self):
        user = User.query.all()
        user_field = {}
        user_field['users'] = []
        if user:
            for x in user:
                user_field["users"].append(
                    {"id": x.id, "username": x.username, "email": x.email, "phone_number": x.phone_number})
        return user_field, 200


class AllScreen(Resource):
    @verify_user_credentials
    def get(self):
        screen = Screen.query.all()
        screen_field = {}
        screen_field['screens'] = []
        # print(screen)
        if screen:
            for x in screen:
                show = Show.query.filter_by(id=x.show_id).first()
                venue = Venue.query.filter_by(id=x.venue_id).first()
                # print(venue.name)
                # print(show.name)
                screen_field["screens"].append({"id": x.id, "venue_id": x.venue_id, "show_id": x.show_id, "venue_name": venue.name, "venue_address": venue.address, "show": show.name, "timing": x.timing.strftime("%Y-%m-%d %H:%M:%S"),
                                                "price": x.price})
        return screen_field, 200


class AllShow(Resource):
    @verify_user_credentials
    def get(self):
        start = perf_counter_ns()
        cached_data = r.get('allShow')
        if cached_data is not None:
            if isinstance(cached_data, bytes):
                cached_data = cached_data.decode('utf-8')
            stop = perf_counter_ns()
            print("Time taken cache", stop - start)
            return ast.literal_eval(cached_data), 200
        show = Show.query.all()
        show_field = {}
        show_field['shows'] = []
        if show:
            for x in show:
                cast = []
                for y in x.cast:
                    cast.append({"id": y.id, "name": y.name, "photo": y.photo})
                tag = []
                for y in x.tags:
                    tag.append({"id": y.id, "name": y.name})
                rating = Rating.query.filter_by(show_id=x.id).all()
                sum_of_ratings = db.session.query(
                    func.sum(Rating.rating)).filter_by(show_id=x.id).scalar()
                if sum_of_ratings:
                    sum_of_ratings /= len(rating)
                if sum_of_ratings and sum_of_ratings == int(sum_of_ratings):
                    sum_of_ratings = int(sum_of_ratings)
                total_revenue = db.session.query(func.sum(Ticket.total_price)).join(
                    Screen).filter(Screen.show_id == x.id).scalar()
                current_user = get_jwt_identity()
                user_id = current_user.get('user_id')
                rating_exists = Rating.query.filter_by(
                    show_id=x.id, user_id=user_id).first() is not None
                show_field["shows"].append({"id": x.id, "name": x.name, "poster": x.poster, "cast": cast,
                                            "tags": tag, "rating": sum_of_ratings, "rating_exists": rating_exists, "total_revenue": total_revenue})
        stop = perf_counter_ns()
        print("Time taken w/o cache", stop - start)
        r.set('allShow', str(show_field), ex=60)
        return show_field, 200


class AllVenue(Resource):
    @verify_user_credentials
    def get(self):
        start = perf_counter_ns()
        cached_data = r.get('allVenue')
        if cached_data is not None:
            if isinstance(cached_data, bytes):
                cached_data = cached_data.decode('utf-8')
            stop = perf_counter_ns()
            print("Time taken cache", stop - start)
            return ast.literal_eval(cached_data), 200
        venue = Venue.query.all()
        venue_field = {}
        venue_field['venues'] = []
        if venue:
            for x in venue:
                venue_field["venues"].append(
                    {"id": x.id, "name": x.name, "city": x.city, "address": x.address, "capacity": x.capacity})
        stop = perf_counter_ns()
        print("Time taken w/o cache", stop - start)
        r.set('allVenue', str(venue_field), ex=60)
        return venue_field, 200


class ShowRelated(Resource):
    @verify_user_credentials
    def get(self, id1):
        show = Show.query.filter_by(id=id1).first()
        if show:
            show_field = {}
            cast = []
            for y in show.cast:
                cast.append({"name": y.name, "photo": y.photo})
            tag = []
            for y in show.tags:
                tag.append({"id": y.id, "name": y.name})
            rating = Rating.query.filter_by(show_id=show.id).all()
            sum_of_ratings = db.session.query(
                func.sum(Rating.rating)).filter_by(show_id=show.id).scalar()
            if sum_of_ratings:
                sum_of_ratings /= len(rating)
            show_field['id'] = show.id
            show_field['name'] = show.name
            show_field['poster'] = show.poster
            show_field['cast'] = cast
            show_field['rating'] = sum_of_ratings
            show_field['tags'] = tag
            return show_field, 200
        else:
            return {"error": "Show does not exist"}, 404

    @verify_admin_credentials
    def put(self, id1):
        evict_cache('displayVenue')
        evict_cache('allShow')
        data = request.get_json()
        show = Show.query.get(id1)
        if show:
            print(data)
            show.name = data.get('name', show.name)
            if ('poster' in data and data.get('poster') != ""):
                show.poster = data.get('poster', show.poster)
            tags = []
            if ('name' not in data.keys() or data.get('name') == ""):
                tags = data.get('tags', show.tags)
                show.tags.clear()
            for tag_data in tags:
                tag_id = tag_data.get('id')
                tag_name = tag_data.get('name')
                if tag_id and tag_name:
                    tag = Tag.query.get(tag_id)
                    if tag and tag.name == tag_name:
                        show.tags.append(tag)
            db.session.commit()
            return {"message": "Show updated successfully."}, 200
        else:
            return {"error": "show does not exist"}, 404

    @verify_admin_credentials
    def delete(self, id1):
        evict_cache('displayVenue')
        evict_cache('allShow')
        show = Show.query.get(id1)
        if show:
            screens = Screen.query.filter_by(show_id=id1)
            for screen in screens:
                tickets = Ticket.query.filter_by(screen_id=screen.id)
                for ticket in tickets:
                    db.session.delete(ticket)
                db.session.delete(screen)
            ratings = Rating.query.filter_by(show_id=id1)
            for x in ratings:
                db.session.delete(x)
            cast_entries = db.session.query(
                cast).filter_by(show_id=show.id).all()
            # for cast_entry in cast_entries:
            #     db.session.delete(cast_entry)
            tags = db.session.query(show_tags).filter_by(show_id=show.id).all()
            for tag_id, show_id in tags:
                tag_entry = show_tags.delete().where(
                    tags.t.tag_id == tag_id).where(tags.t.show_id == show_id)
                db.session.execute(tag_entry)
            for celebrity_id, show_id in cast_entries:
                cast_entry = cast.delete().where(cast.c.celebrity_id ==
                                                 celebrity_id).where(cast.c.show_id == show_id)
                db.session.execute(cast_entry)
            db.session.delete(show)
            db.session.commit()
            return {"message": "Show deleted successfully."}, 200
        else:
            return {"error": "show does not exist"}, 404


class ScreenRelated(Resource):
    @verify_user_credentials
    def get(self, id1):
        screen = Screen.query.filter_by(id=id1).first()
        if screen:
            show = Show.query.filter_by(id=screen.show_id).first()
            venue = Venue.query.filter_by(id=screen.venue_id).first()
            screen_field = {}
            screen_field['id'] = screen.id
            screen_field['timing'] = screen.timing.strftime(
                "%Y-%m-%d %H:%M:%S")
            screen_field['venue_name'] = venue.name
            screen_field['venue_address'] = venue.address
            screen_field['venue_id'] = screen.venue_id
            screen_field['show_id'] = screen.show_id
            screen_field['show'] = show.name
            screen_field['price'] = screen.price
            return screen_field, 200
        else:
            return {"error": "screen does not exist"}, 404

    @verify_admin_credentials
    def put(self, id1):
        evict_cache('displayVenue')
        data = request.get_json()
        screen = Screen.query.get(id1)
        if screen:
            timing_str = data.get('timing', screen.timing)
            if isinstance(timing_str, str):
                timing = datetime.strptime(timing_str, '%Y-%m-%d %H:%M:%S')
            else:
                timing = screen.timing
            screen.timing = timing
            screen.venue_id = data.get('venue_id', screen.venue_id)
            screen.show_id = data.get('show_id', screen.show_id)
            if (isinstance(data['price'], int) or isinstance(data['price'], float)):
                screen.price = data.get('price', screen.price)
            try:
                p = float(data['price'])
                screen.price = p
            except:
                pass
            db.session.commit()
            return {"message": "screen updated successfully."}, 200
        else:
            return {"error": "screen does not exist"}, 404

    @verify_admin_credentials
    def delete(self, id1):
        evict_cache('displayVenue')
        screen = Screen.query.get(id1)
        if screen:
            tickets = Ticket.query.filter_by(screen_id=screen.id).all()
            for x in tickets:
                db.session.delete(x)
            db.session.delete(screen)
            db.session.commit()
            return {"message": "screen deleted successfully."}, 200
        else:
            return {"error": "screen does not exist"}, 404


class VenueRelated(Resource):
    @verify_user_credentials
    def get(self, id1):
        venue = Venue.query.filter_by(id=id1).first()
        if venue:
            venue_field = {}
            venue_field['id'] = venue.id
            venue_field['name'] = venue.name
            venue_field['city'] = venue.city
            venue_field['address'] = venue.address
            venue_field['capacity'] = venue.capacity
            return venue_field, 200
        else:
            return {"error": "venue does not exist"}, 404

    @verify_admin_credentials
    def put(self, id1):
        evict_cache('displayVenue')
        evict_cache('allVenue')
        data = request.get_json()
        venue = Venue.query.get(id1)
        if venue:
            venue.name = data.get('name', venue.name)
            venue.city = data.get('city', venue.city)
            venue.address = data.get('address', venue.address)
            capacity = data.get('capacity', venue.capacity)
            if isinstance(capacity, int) or capacity.isdigit():
                venue.capacity = capacity
            else:
                return {"error": "capacity must be integer"}, 403
            db.session.commit()
            return {"message": "venue updated successfully."}, 200
        else:
            return {"error": "venue does not exist"}, 404

    @verify_admin_credentials
    def delete(self, id1):
        evict_cache('displayVenue')
        evict_cache('allVenue')
        venue = Venue.query.get(id1)
        if venue:
            screens = Screen.query.filter_by(venue_id=id1)
            for screen in screens:
                tickets = Ticket.query.filter_by(screen_id=screen.id)
                for ticket in tickets:
                    db.session.delete(ticket)
                db.session.delete(screen)
            db.session.delete(venue)
            db.session.commit()
            return {"message": "venue deleted successfully."}, 200
        else:
            return {"error": "venue does not exist"}, 404


class DisplayVenue(Resource):
    @verify_admin_credentials
    def get(self):
        start = perf_counter_ns()
        cached_data = r.get('displayVenue')
        if cached_data is not None:
            if isinstance(cached_data, bytes):
                cached_data = cached_data.decode('utf-8')
            stop = perf_counter_ns()
            print("Time taken cache", stop - start)
            return ast.literal_eval(cached_data), 200
        venues = Venue.query.all()
        venue_field = {}
        venue_field['venues'] = []
        for venue in venues:
            screens = Screen.query.filter_by(venue_id=venue.id).all()
            screendetails = []
            for screen in screens:
                show = Show.query.filter_by(id=screen.show_id).first()
                screendetails.append({"id": screen.id, "show": show.name, "timing": screen.timing.strftime(
                    "%Y-%m-%d %H:%M:%S"), "price": screen.price})
            venue_field["venues"].append({"id": venue.id, "name": venue.name, "city": venue.city,
                                         "address": venue.address, "capacity": venue.capacity, "screens": screendetails})
        stop = perf_counter_ns()
        print("Time taken w/o cache", stop - start)
        r.set('displayVenue', str(venue_field), ex=60)
        return venue_field, 200


class AddTag(Resource):
    @verify_admin_credentials
    def post(self):
        evict_cache('allShow')
        data = request.get_json()
        name = data.get("name")
        tag = Tag(name=name)
        db.session.add(tag)
        db.session.commit()
        return {"message": "Tag created successfully"}, 200


class TagRelated(Resource):
    @verify_user_credentials
    def get(self, tag_id):
        tag = Tag.query.get(tag_id)
        if tag:
            return {"id": tag.id, "name": tag.name}, 200
        else:
            return {"error": "Tag not found"}, 404

    @verify_admin_credentials
    def put(self, tag_id):
        evict_cache('allShow')
        data = request.get_json()
        tag = Tag.query.get(tag_id)
        if tag:
            tag.name = data.get("name", tag.name)
            db.session.commit()
            return {"message": "Tag updated successfully"}, 200
        else:
            return {"error": "Tag not found"}, 404

    @verify_admin_credentials
    def delete(self, tag_id):
        evict_cache('allShow')
        tag = Tag.query.get(tag_id)
        if tag:
            db.session.delete(tag)
            db.session.commit()
            return {"message": "Tag deleted successfully"}, 200
        else:
            return {"error": "Tag not found"}, 404


class AllTag(Resource):
    @verify_user_credentials
    def get(self):
        tags = Tag.query.all()
        tag_list = []
        for x in tags:
            tag_list.append({"id": x.id, "name": x.name})
        return tag_list, 200


class AdminLogin(Resource):
    def post(self):
        email = request.json.get('email')
        password = request.json.get('password')

        admin = User.query.filter_by(email=email, u_type='admin').first()

        if admin and bcrypt.check_password_hash(admin.password, password):
            access_token = create_access_token(
                identity={'email': admin.email, 'password': admin.password,  'u_type': admin.u_type})
            return {'access_token': access_token}, 200

        return {'message': 'Invalid credentials'}, 401


class UserLogin(Resource):
    def post(self):
        email = request.json.get('email')
        password = request.json.get('password')
        user = User.query.filter_by(email=email, u_type='user').first()
        try:
            if user and bcrypt.check_password_hash(user.password, password):
                hashed_password_bytes = user.password
                hashed_password_str = hashed_password_bytes
                if isinstance(hashed_password_bytes, bytes):
                    hashed_password_str = hashed_password_bytes.decode('utf-8')
                user.update_recent_login()
                access_token = create_access_token(identity={'email': user.email, 'password': hashed_password_str,
                                                             'user_id': user.id, 'u_type': 'user'})
                return {'access_token': access_token}, 200
            return {'message': 'Invalid credentials'}, 401
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return {'message': 'An error occurred'}, 500


class UserRegistration(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        phone_number = data.get('phone_number')
        email = data.get('email')
        u_type = 'user'

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            return {'message': 'User already exists'}, 400

        hashed_password = bcrypt.generate_password_hash(password)
        new_user = User(username=username, password=hashed_password,
                        phone_number=phone_number, email=email, u_type=u_type)
        db.session.add(new_user)
        db.session.commit()
        return {'message': "User registered successfully"}, 200
