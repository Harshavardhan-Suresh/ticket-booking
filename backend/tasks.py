from models import *
app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379/1',   
    result_backend='redis://localhost:6379/2',
    timezone='Asia/Kolkata'
)

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['result_backend'],
        broker=app.config['CELERY_BROKER_URL'],
        timezone=app.config['timezone']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

Celery = make_celery(app)

@Celery.task
def generate_excel_task(theatre_id):
    excel_filename = f'theatre_{theatre_id}_info.xlsx'
    workbook = xlsxwriter.Workbook(excel_filename)
    screens_sheet = workbook.add_worksheet('Screens')
    tickets_sheet = workbook.add_worksheet('Tickets')

    # Add data to sheets (replace with your data)
    screens = Screen.query.filter_by(venue_id = theatre_id).all();
    screens_data = [
        ['screen_id', 'show_id', 'show_name', 'price', 'timing'],
    ]
    tickets_data = [
        ['user_id','username', 'email','screen_id', 'show_id', 'show_name', 'no_of_seats', 'total_price'],
    ]
    for screen in screens:
        show = Show.query.filter_by(id = screen.show_id).first()
        timestamp = datetime.strptime(str(screen.timing), '%Y-%m-%d %H:%M:%S')
        # Format the datetime object as "day month, year hour:minute AM/PM"
        formatted_time = timestamp.strftime('%d %b, %Y %I:%M %p')
        screens_data.append([screen.id, screen.show_id, show.name, screen.price, formatted_time])
        tickets = Ticket.query.filter_by(screen_id = screen.id)
        for ticket in tickets:
            user = User.query.filter_by(id = ticket.user_id).first()
            tickets_data.append([user.id, user.username, user.email, screen.id, show.id, show.name, ticket.no_of_seats, ticket.total_price])

    for row_num, row_data in enumerate(screens_data):
        screens_sheet.write_row(row_num, 0, row_data)

    cell_format = workbook.add_format()
    cell_format.set_text_wrap()
    screens_sheet.set_column('A:E', 20, cell_format)
    for row_num, row_data in enumerate(tickets_data):
        tickets_sheet.write_row(row_num, 0, row_data)
        
    tickets_sheet.set_column('A:H', 20, cell_format)
    # Close the workbook
    workbook.close()

    # Send the Excel file as a response
    return excel_filename
# remember to run this line
# $env:PATH += ';C:\SQLite3'

def check_user_activity(user):
    current_time = datetime.now()
    return user.recent_login and ((current_time - user.recent_login) < timedelta(days = 1))

@app.route('/generate_excel/<int:theatre_id>')
def generate_excel(theatre_id):
    # Create an Excel workbook and add sheets for screens and shows
    result = generate_excel_task.delay(theatre_id)
    result = generate_excel_task(theatre_id)
    return send_file(result, as_attachment=True)

@Celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(minute=0, hour=18),
        notify.s(), 
        name ='notify_users'
    )
    sender.add_periodic_task(
        crontab(0, 0, day_of_month='1'),
        entertainment_report.s(),
        name='entertainment_report'
    )


def send_email(to_address, subject, message, content="text", attachment_file=None):
    msg=MIMEMultipart()
    msg['From'] = app.config['SENDER_ADDRESS']
    msg['To'] = to_address
    msg['Subject'] = subject
    if content=="html":
        msg.attach(MIMEText(message, "html"))
    else:
        msg.attach(MIMEText(message, "plain"))
    if attachment_file:
        with open(attachment_file, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition", f"attachemnt; filename= {attachment_file}"
        )
        msg.attach(part)
    s = smtplib.SMTP(host=app.config['SMTP_SERVER_HOST'], port=app.config['SMTP_SERVER_PORT'])
    s.login(app.config['SENDER_ADDRESS'], app.config['SENDER_PASSWORD'])
    s.send_message(msg)
    s.quit()
    return True

@Celery.task
def notify():
    users = User.query.all()
    for user in users:
        if user.u_type == 'user':
            with open("notify_user.html") as file_:
                template = Template(file_.read())
                message = template.render(data = {"name": user.username})
            if not check_user_activity(user):
                send_email(user.email, subject="Book Tickets", message=message, content="html")
    return "Mails were send successfully"

@Celery.task
def entertainment_report():
    users = User.query.all()
    shows = Show.query.all()
    current_time = datetime.now()
    for user in users:
        user_obj = {"username" : user.username, "email": user.email}
        if user.u_type == 'user':
            ratings = []
            for show in shows:
                rating = Rating.query.filter_by(show_id = show.id, user_id = user.id).first()
                if rating and ((current_time - rating.added_at ) < timedelta(days = 30)): 
                    ratings.append({"rating": rating.rating, "show_name": show.name})
            tickets = Ticket.query.filter_by(user_id = user.id)
            ticket_obj = []
            for ticket in tickets:
                screen =  Screen.query.filter_by(id = ticket.screen_id).first()
                show =  Show.query.filter_by(id = screen.show_id).first()
                venue =  Venue.query.filter_by(id = screen.venue_id).first()
                input_datetime = screen.timing
                output_date_string = input_datetime.strftime("%d %B, %Y %I:%M %p")
                poster = show.poster
                if not poster:
                    poster = '/images/no_image.png'
                poster = 'http://localhost:8082' + poster
                if screen.timing and ((current_time - screen.timing) < timedelta(days = 30)): 
                    ticket_obj.append({"no_of_seats" : ticket.no_of_seats, "total_price": ticket.total_price,
                                    "time_and_date" : output_date_string, "show_name" : show.name, "venue_name":venue.name, "show_poster" : poster})
            with open("entertainment_report.html") as file_:
                template = Template(file_.read())
                message = template.render(user = user_obj, ratings = ratings, tickets = ticket_obj)
                html = HTML(string=message)
                file_name = str(user.username +" " + str(datetime.now())) + ".pdf"
                print(file_name)
                html.write_pdf(target=file_name)
                send_email(user.email, subject="Monthly report", message='Here is your monthly report', attachment_file=file_name)
    return "Reports were send successfully"

