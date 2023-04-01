from flask import Flask, render_template, request, redirect, url_for, session, send_file
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
import os
from datetime import datetime
import dateutil.parser as dparser
import zipfile
import csv

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
ALLOWED_EXTENSIONS = {'pdf'}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.secret_key = 'secret key'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'tempmail.xlcsgo@gmail.com'
app.config['MAIL_PASSWORD'] = 'jjjthrbdtohkiomc'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEFAULT_SENDER'] = 'tempmail.xlcsgo@gmail.com'
app.config['MAIL_SUBJECT_PREFIX'] = 'PHDmon:'
mail = Mail(app)
db = SQLAlchemy(app)

class Ticket(db.Model):
    Project_ID = db.Column(db.Integer, primary_key=True)
    Roll_No = db.Column(db.String(50), unique=True, nullable=False)
    Student_Name = db.Column(db.String(50), unique=True, nullable=False)
    Student_Email = db.Column(db.String(50), unique=True, nullable=False)
    Au = db.Column(db.String(50), nullable=False)
    Date_Of_Registration = db.Column(db.DateTime, nullable=False)
    Gate = db.Column(db.Boolean, nullable=False)
    Project_Title = db.Column(db.String(50), nullable=False)
    Date_Of_IRB = db.Column(db.DateTime, nullable=False)
    Date_Of_Progress_Presentation = db.Column(db.DateTime, nullable=False)
    File_Path = db.Column(db.String(50), unique=True, nullable=False)
    Publications = db.Column(db.String(50))
    Conferences = db.Column(db.String(50))
    Supervisor1_Name = db.Column(db.String(50))
    Supervisor1_Email = db.Column(db.String(50))
    Supervisor1_Approval = db.Column(db.Boolean)
    Supervisor1_Remarks = db.Column(db.String(100))
    Supervisor1_Marks = db.Column(db.Integer)
    Supervisor2_Name = db.Column(db.String(50))
    Supervisor2_Email = db.Column(db.String(50))
    Supervisor2_Approval = db.Column(db.Boolean)
    Supervisor2_Remarks = db.Column(db.String(100))
    Supervisor2_Marks = db.Column(db.Integer)
    Supervisor3_Name = db.Column(db.String(50))
    Supervisor3_Email = db.Column(db.String(50))
    Supervisor3_Approval = db.Column(db.Boolean)
    Supervisor3_Remarks = db.Column(db.String(100))
    Supervisor3_Marks = db.Column(db.Integer)
    Committee1_Name = db.Column(db.String(50))
    Committee1_Email = db.Column(db.String(50))
    Committee1_Approval = db.Column(db.Boolean)
    Committee1_Remarks = db.Column(db.String(100))
    Committee2_Name = db.Column(db.String(50))
    Committee2_Email = db.Column(db.String(50))
    Committee2_Approval = db.Column(db.Boolean)
    Committee2_Remarks = db.Column(db.String(100))
    Committee3_Name = db.Column(db.String(50))
    Committee3_Email = db.Column(db.String(50))
    Committee3_Approval = db.Column(db.Boolean)
    Committee3_Remarks = db.Column(db.String(100))
    Committee4_Name = db.Column(db.String(50))
    Committee4_Email = db.Column(db.String(50))
    Committee4_Approval = db.Column(db.Boolean)
    Committee4_Remarks = db.Column(db.String(100))
    Committee5_Name = db.Column(db.String(50))
    Committee5_Email = db.Column(db.String(50))
    Committee5_Approval = db.Column(db.Boolean)
    Committee5_Remarks = db.Column(db.String(100))
    Au_Approval = db.Column(db.Boolean)
    Adordc_Approval = db.Column(db.Boolean)
    LastDate = db.Column(db.DateTime, nullable=False)

class Archive_Ticket(db.Model):
    Project_ID = db.Column(db.Integer, primary_key=True)
    Roll_No = db.Column(db.String(50), unique=True, nullable=False)
    Student_Name = db.Column(db.String(50), unique=True, nullable=False)
    Student_Email = db.Column(db.String(50), unique=True, nullable=False)
    Au = db.Column(db.String(50), nullable=False)
    Date_Of_Registration = db.Column(db.DateTime, nullable=False)
    Gate = db.Column(db.Boolean, nullable=False)
    Project_Title = db.Column(db.String(50), nullable=False)
    Date_Of_IRB = db.Column(db.DateTime, nullable=False)
    Date_Of_Progress_Presentation = db.Column(db.DateTime, nullable=False)
    File_Path = db.Column(db.String(50), unique=True, nullable=False)
    Publications = db.Column(db.String(50))
    Conferences = db.Column(db.String(50))
    Supervisor1_Name = db.Column(db.String(50))
    Supervisor1_Email = db.Column(db.String(50))
    Supervisor1_Approval = db.Column(db.Boolean)
    Supervisor1_Remarks = db.Column(db.String(100))
    Supervisor1_Marks = db.Column(db.Integer)
    Supervisor2_Name = db.Column(db.String(50))
    Supervisor2_Email = db.Column(db.String(50))
    Supervisor2_Approval = db.Column(db.Boolean)
    Supervisor2_Remarks = db.Column(db.String(100))
    Supervisor2_Marks = db.Column(db.Integer)
    Supervisor3_Name = db.Column(db.String(50))
    Supervisor3_Email = db.Column(db.String(50))
    Supervisor3_Approval = db.Column(db.Boolean)
    Supervisor3_Remarks = db.Column(db.String(100))
    Supervisor3_Marks = db.Column(db.Integer)
    Committee1_Name = db.Column(db.String(50))
    Committee1_Email = db.Column(db.String(50))
    Committee1_Approval = db.Column(db.Boolean)
    Committee1_Remarks = db.Column(db.String(100))
    Committee2_Name = db.Column(db.String(50))
    Committee2_Email = db.Column(db.String(50))
    Committee2_Approval = db.Column(db.Boolean)
    Committee2_Remarks = db.Column(db.String(100))
    Committee3_Name = db.Column(db.String(50))
    Committee3_Email = db.Column(db.String(50))
    Committee3_Approval = db.Column(db.Boolean)
    Committee3_Remarks = db.Column(db.String(100))
    Committee4_Name = db.Column(db.String(50))
    Committee4_Email = db.Column(db.String(50))
    Committee4_Approval = db.Column(db.Boolean)
    Committee4_Remarks = db.Column(db.String(100))
    Committee5_Name = db.Column(db.String(50))
    Committee5_Email = db.Column(db.String(50))
    Committee5_Approval = db.Column(db.Boolean)
    Committee5_Remarks = db.Column(db.String(100))
    Au_Approval = db.Column(db.Boolean)
    Adordc_Approval = db.Column(db.Boolean)
    LastDate = db.Column(db.DateTime, nullable=False)

class User(db.Model):
    email = db.Column(db.String(50), unique=True, nullable=False, primary_key=True)
    password = db.Column(db.String(50), nullable=False) 
    role = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    Au = db.Column(db.String(50), nullable=False)

class Unapproved_Users(db.Model):
    email = db.Column(db.String(50), unique=True, nullable=False, primary_key=True)
    password = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    Au = db.Column(db.String(50), nullable=False)

class LastDate(db.Model):
    LastDate = db.Column(db.DateTime, nullable=False, primary_key=True)

@app.route('/')
def home():
    return redirect(url_for('first_time'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                session['email'] = email
                session['role'] = user.role
                session['Au'] = user.Au
                if user.role == 'AU_Head':
                    return redirect(url_for('au_head'))
                elif user.role == 'admin':
                    return redirect(url_for('adordc'))
            else:
                print('Wrong password')
                return render_template('login.html', error='Wrong password')
        else:
            print('Email does not exist')
            return render_template('login.html', error='Email does not exist')
    return render_template('login.html', error='')

@app.route('/logout')
def logout():
    session.pop('email', None)
    session.pop('role', None)
    session.pop('Au', None)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        role = "AU_Head"
        name = request.form['name']
        Au = request.form['Au']
        user = User.query.filter_by(email=email).first()
        if user:
            return render_template('register.html', error='Email already exists', success='')
        new_user = Unapproved_Users(email=email, password=generate_password_hash(password, method='sha256'), role=role, name=name, Au=Au)
        db.session.add(new_user)
        db.session.commit()
        return render_template('register.html', success='User created successfully', error='')
    return render_template('register.html', error='', success='')

@app.route('/unapproved_users', methods=['GET', 'POST'])
def unapproved_users():
    if session.get('role') == 'admin':
        unapproved_users = Unapproved_Users.query.all()
        print(unapproved_users)
        #convert to list of dictionaries
        unapproved_users = [dict(email=unapproved_user.email, password=unapproved_user.password, role=unapproved_user.role, name=unapproved_user.name, Au=unapproved_user.Au) for unapproved_user in unapproved_users]
        return render_template('unapproved_users.html', unapproved_users=unapproved_users)
    return redirect(url_for('login'))

@app.route('/manage_users', methods=['GET', 'POST'])
def manage_users():
    if session.get('role') == 'admin':
        #get all users where role is not admin
        users = User.query.filter(User.role != 'admin').all()
        print(users)
        #convert to list of dictionaries
        users = [dict(email=user.email, password=user.password, role=user.role, name=user.name, Au=user.Au) for user in users]
        #delete passwords from dictionary
        for user in users:
            del user['password']
        return render_template('manage_users.html', users=users)
    return redirect(url_for('login'))

@app.route('/approve_user/<email>', methods=['GET', 'POST'])
def approve_user(email):
    if session.get('role') == 'admin':
        unapproved_user = Unapproved_Users.query.filter_by(email=email).first()
        new_user = User(email=unapproved_user.email, password=unapproved_user.password, role=unapproved_user.role, name=unapproved_user.name, Au=unapproved_user.Au)
        db.session.add(new_user)
        db.session.commit()
        db.session.delete(unapproved_user)
        db.session.commit()
        return redirect(url_for('unapproved_users'))
    return redirect(url_for('login'))

@app.route('/delete_user/<email>', methods=['GET', 'POST'])
def delete_user(email):
    if session.get('role') == 'admin':
        unapproved_user = Unapproved_Users.query.filter_by(email=email).first()
        db.session.delete(unapproved_user)
        db.session.commit()
        return redirect(url_for('unapproved_users'))
    return redirect(url_for('login'))

@app.route('/create_ticket', methods=['GET', 'POST'])
def create_ticket():
    if request.method == 'POST':
        student_name = request.form['student_name']
        student_email = request.form['student_email']
        Roll_No = request.form['Roll_No']
        Au = request.form['Au']
        Date_Of_Registration = datetime.now()
        Gate = request.form['Gate']
        if Gate == 'Yes':
            Gate = True
        else:
            Gate = False
        Project_Title = request.form['Project_Title']
        Date_Of_Progress_Presentation = request.form['Date_Of_Progress_Presentation']
        Date_Of_Progress_Presentation = dparser.parse(Date_Of_Progress_Presentation, fuzzy=True)
        Date_Of_IRB = request.form['Date_Of_IRB']
        Date_Of_IRB = dparser.parse(Date_Of_IRB, fuzzy=True)
        Supervisor1_Name = request.form['Supervisor1_Name']
        Supervisor1_Email = request.form['Supervisor1_Email']
        Supervisor1_Approval = False
        Supervisor1_Remarks = ''
        Supervisor1_Marks = 0
        if request.form['Supervisor2_Name'] != '':
            Supervisor2_Name = request.form['Supervisor2_Name']
            Supervisor2_Email = request.form['Supervisor2_Email']
            Supervisor2_Approval = False
            Supervisor2_Remarks = ''
            Supervisor2_Marks = 0
        else:
            Supervisor2_Name = ''
            Supervisor2_Email = ''
            Supervisor2_Approval = False
            Supervisor2_Remarks = ''
            Supervisor2_Marks = 0
        if request.form['Supervisor3_Name'] != '':
            Supervisor3_Name = request.form['Supervisor3_Name']
            Supervisor3_Email = request.form['Supervisor3_Email']
            Supervisor3_Approval = False
            Supervisor3_Remarks = ''
            Supervisor3_Marks = 0
        else:
            Supervisor3_Name = ''
            Supervisor3_Email = ''
            Supervisor3_Approval = False
            Supervisor3_Remarks = ''
            Supervisor3_Marks = 0
        Committee1_Name = request.form['Committee1_Name']
        Committee1_Email = request.form['Committee1_Email']
        Committee1_Approval = False
        Committee1_Remarks = ''
        Committee2_Name = request.form['Committee2_Name']
        Committee2_Email = request.form['Committee2_Email']
        Committee2_Approval = False
        Committee2_Remarks = ''
        Committee3_Name = request.form['Committee3_Name']
        Committee3_Email = request.form['Committee3_Email']
        Committee3_Approval = False
        Committee3_Remarks = ''
        #committee4 is optional
        if request.form['Committee4_Name'] != '':
            Committee4_Name = request.form['Committee4_Name']
            Committee4_Email = request.form['Committee4_Email']
            Committee4_Approval = False
            Committee4_Remarks = ''
        else:
            Committee4_Name = ''
            Committee4_Email = ''
            Committee4_Approval = False
            Committee4_Remarks = ''
        #committee5 is optional
        if request.form['Committee5_Name'] != '':
            Committee5_Name = request.form['Committee5_Name']
            Committee5_Email = request.form['Committee5_Email']
            Committee5_Approval = False
            Committee5_Remarks = ''
        else:
            Committee5_Name = ''
            Committee5_Email = ''
            Committee5_Approval = False
            Committee5_Remarks = ''
        #uploading file to server store in UPLOAD_FOLDER with name as Roll_No and extension as .pdf and save the path in database
        print(request.files)
        file = request.files.get('file_path', None)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], Roll_No + '.pdf')
        file.save(file_path)
        Publications = request.form['Publications']
        Conferences = request.form['Conferences']
        #set last date to last_date
        lastdate = LastDate.query.first().LastDate
        #convert lastdate to string
        lastdate = lastdate.strftime('%Y-%m-%d')
        #convert lastdate to datetime
        lastdate = dparser.parse(lastdate, fuzzy=True)
        Au_Approval = False
        Adordc_Approval = False
        #create new ticket without including supervisor2, supervisor3, committee4, committee5
        new_ticket = Ticket(Student_Name=student_name, Student_Email=student_email, Roll_No=Roll_No, Au=Au, Date_Of_Registration=Date_Of_Registration, Gate=Gate, Project_Title=Project_Title, Date_Of_Progress_Presentation=Date_Of_Progress_Presentation, Date_Of_IRB=Date_Of_IRB, Supervisor1_Name=Supervisor1_Name, Supervisor1_Email=Supervisor1_Email, Supervisor1_Approval=Supervisor1_Approval, Supervisor1_Remarks=Supervisor1_Remarks, Committee1_Name=Committee1_Name, Committee1_Email=Committee1_Email, Committee1_Approval=Committee1_Approval, Committee1_Remarks=Committee1_Remarks, Committee2_Name=Committee2_Name, Committee2_Email=Committee2_Email, Committee2_Approval=Committee2_Approval, Committee2_Remarks=Committee2_Remarks, Committee3_Name=Committee3_Name, Committee3_Email=Committee3_Email, Committee3_Approval=Committee3_Approval, Committee3_Remarks=Committee3_Remarks, Publications=Publications, Conferences=Conferences, Au_Approval=Au_Approval, Adordc_Approval=Adordc_Approval, File_Path=file_path, Supervisor1_Marks=Supervisor1_Marks, LastDate=lastdate)        
        #put data into database. check if supervisor2, supervisor3, committee4, committee5 are empty or not, if empty then don't add them to database
        if Supervisor2_Name != '':
            new_ticket.Supervisor2_Name = Supervisor2_Name
            new_ticket.Supervisor2_Email = Supervisor2_Email
            new_ticket.Supervisor2_Approval = Supervisor2_Approval
            new_ticket.Supervisor2_Remarks = Supervisor2_Remarks
            new_ticket.Supervisor2_Marks = Supervisor2_Marks
        if Supervisor3_Name != '':
            new_ticket.Supervisor3_Name = Supervisor3_Name
            new_ticket.Supervisor3_Email = Supervisor3_Email
            new_ticket.Supervisor3_Approval = Supervisor3_Approval
            new_ticket.Supervisor3_Remarks = Supervisor3_Remarks
            new_ticket.Supervisor3_Marks = Supervisor3_Marks
        if Committee4_Name != '':
            new_ticket.Committee4_Name = Committee4_Name
            new_ticket.Committee4_Email = Committee4_Email
            new_ticket.Committee4_Approval = Committee4_Approval
            new_ticket.Committee4_Remarks = Committee4_Remarks
        if Committee5_Name != '':
            new_ticket.Committee5_Name = Committee5_Name
            new_ticket.Committee5_Email = Committee5_Email
            new_ticket.Committee5_Approval = Committee5_Approval
            new_ticket.Committee5_Remarks = Committee5_Remarks
        db.session.add(new_ticket)
        db.session.commit()
        #get Project_ID
        ticket = Ticket.query.filter_by(Student_Email=student_email).first()
        Project_ID = ticket.Project_ID
        send_email(student_email, 'Ticket Created', 'email/ticket_created', Ticket=ticket)
        send_email(Supervisor1_Email, f'Ticket {Project_ID} Created', 'email/ticket_created_super', Ticket=ticket, Super=1)
        if Supervisor2_Email != '':
            send_email(Supervisor2_Email, f'Ticket {Project_ID} Created', 'email/ticket_created_super', Ticket=ticket, Super=2)
        if Supervisor3_Email != '':
            send_email(Supervisor3_Email, f'Ticket {Project_ID} Created', 'email/ticket_created_super', Ticket=ticket, Super=3)
        return render_template('create_ticket.html', success='Ticket created successfully', Project_ID=Project_ID)
    return render_template('create_ticket.html', success='')

@app.route('/ticket_created/<Project_ID>')
def ticket_created(Project_ID):
    ticket = Ticket.query.filter_by(Project_ID=Project_ID).first()
    ticket = ticket.__dict__
    return render_template('ticket_created.html', Ticket=ticket)

@app.route('/file/<Project_ID>')
def file(Project_ID):
    ticket = Ticket.query.filter_by(Project_ID=Project_ID).first()
    file_path = ticket.File_Path
    return send_file(file_path, as_attachment=True)

@app.route('/super/1/<Project_ID>', methods=['GET', 'POST'])
def super1(Project_ID):
    ticket = Ticket.query.filter_by(Project_ID=Project_ID).first()
    if request.method == 'POST':
        if request.form['submit'] == 'Approve':
            ticket.Supervisor1_Approval = True
        prev_marks = request.form['prevmarks']
        now_marks = request.form['nowmarks']
        ticket.Supervisor1_Marks = int(prev_marks) + int(now_marks)
        ticket.Supervisor1_Remarks = request.form['Supervisor1_Remarks']
        db.session.commit()
        ticket = Ticket.query.filter_by(Project_ID=Project_ID).first()
        ticket = ticket.__dict__
        if request.form['submit'] == 'Approve':
            if ticket['Supervisor1_Approval'] == True and ticket['Supervisor2_Approval'] == True and ticket['Supervisor3_Approval'] == True:
                send_email(ticket['Committee1_Email'], f'Ticket {Project_ID} Approved By Supervisors', 'email/ticket_approved', Ticket=ticket, Comm=1)
                send_email(ticket['Committee2_Email'], f'Ticket {Project_ID} Approved By Supervisors', 'email/ticket_approved', Ticket=ticket, Comm=2)
                send_email(ticket['Committee3_Email'], f'Ticket {Project_ID} Approved By Supervisors', 'email/ticket_approved', Ticket=ticket, Comm=3)
                if ticket['Committee4_Email'] != '':
                    send_email(ticket['Committee4_Email'], f'Ticket {Project_ID} Approved By Supervisors', 'email/ticket_approved', Ticket=ticket, Comm=4)
                if ticket['Committee5_Email'] != '':
                    send_email(ticket['Committee5_Email'], f'Ticket {Project_ID} Approved By Supervisors', 'email/ticket_approved', Ticket=ticket, Comm=5)
            return render_template('supervisor.html', super=1, Ticket=ticket, success='Project Approved. Remarks added successfully')
        else:
            return render_template('supervisor.html', super=1, Ticket=ticket, success='Project Rejected. Remarks added.')
    return render_template('supervisor.html', super=1, Ticket=ticket, success='')

@app.route('/super/2/<Project_ID>', methods=['GET', 'POST'])
def super2(Project_ID):
    ticket = Ticket.query.filter_by(Project_ID=Project_ID).first()
    if request.method == 'POST':
        if request.form['submit'] == 'Approve':
            ticket.Supervisor2_Approval = True
        prev_marks = request.form['prevmarks']
        now_marks = request.form['nowmarks']
        ticket.Supervisor2_Marks = int(prev_marks) + int(now_marks)
        ticket.Supervisor2_Remarks = request.form['Supervisor1_Remarks']
        db.session.commit()
        ticket = Ticket.query.filter_by(Project_ID=Project_ID).first()
        ticket = ticket.__dict__
        if request.form['submit'] == 'Approve':
            if ticket['Supervisor1_Approval'] == True and ticket['Supervisor2_Approval'] == True and ticket['Supervisor3_Approval'] == True:
                send_email(ticket['Committee1_Email'], f'Ticket {Project_ID} Approved By Supervisors', 'email/ticket_approved', Ticket=ticket, Comm=1)
                send_email(ticket['Committee2_Email'], f'Ticket {Project_ID} Approved By Supervisors', 'email/ticket_approved', Ticket=ticket, Comm=2)
                send_email(ticket['Committee3_Email'], f'Ticket {Project_ID} Approved By Supervisors', 'email/ticket_approved', Ticket=ticket, Comm=3)
                if ticket['Committee4_Email'] != '':
                    send_email(ticket['Committee4_Email'], f'Ticket {Project_ID} Approved By Supervisors', 'email/ticket_approved', Ticket=ticket, Comm=4)
                if ticket['Committee5_Email'] != '':
                    send_email(ticket['Committee5_Email'], f'Ticket {Project_ID} Approved By Supervisors', 'email/ticket_approved', Ticket=ticket, Comm=5)
            return render_template('supervisor.html', super=2, Ticket=ticket, success='Project Approved. Remarks added successfully')
        else:
            return render_template('supervisor.html', super=2, Ticket=ticket, success='Project Rejected. Remarks added.')
    return render_template('supervisor.html', super=2, Ticket=ticket, success='')

@app.route('/super/3/<Project_ID>', methods=['GET', 'POST'])
def super3(Project_ID):
    ticket = Ticket.query.filter_by(Project_ID=Project_ID).first()
    if request.method == 'POST':
        if request.form['submit'] == 'Approve':
            ticket.Supervisor1_Approval = True
        prev_marks = request.form['prevmarks']
        now_marks = request.form['nowmarks']
        ticket.Supervisor3_Marks = int(prev_marks) + int(now_marks)
        ticket.Supervisor3_Remarks = request.form['Supervisor3_Remarks']
        db.session.commit()
        ticket = Ticket.query.filter_by(Project_ID=Project_ID).first()
        ticket = ticket.__dict__
        if request.form['submit'] == 'Approve':
            if ticket['Supervisor1_Approval'] == True and ticket['Supervisor2_Approval'] == True and ticket['Supervisor3_Approval'] == True:
                send_email(ticket['Committee1_Email'], f'Ticket {Project_ID} Approved By Supervisors', 'email/ticket_approved', Ticket=ticket, Comm=1)
                send_email(ticket['Committee2_Email'], f'Ticket {Project_ID} Approved By Supervisors', 'email/ticket_approved', Ticket=ticket, Comm=2)
                send_email(ticket['Committee3_Email'], f'Ticket {Project_ID} Approved By Supervisors', 'email/ticket_approved', Ticket=ticket, Comm=3)
                if ticket['Committee4_Email'] != '':
                    send_email(ticket['Committee4_Email'], f'Ticket {Project_ID} Approved By Supervisors', 'email/ticket_approved', Ticket=ticket, Comm=4)
                if ticket['Committee5_Email'] != '':
                    send_email(ticket['Committee5_Email'], f'Ticket {Project_ID} Approved By Supervisors', 'email/ticket_approved', Ticket=ticket, Comm=5)
            return render_template('supervisor.html', super=3, Ticket=ticket, success='Project Approved. Remarks added successfully')
        else:
            return render_template('supervisor.html', super=3, Ticket=ticket, success='Project Rejected. Remarks added.')
    return render_template('supervisor.html', super=3, Ticket=ticket, success='')

@app.route('/comm/1/<Project_ID>', methods=['GET', 'POST'])
def comm1(Project_ID):
    ticket = Ticket.query.filter_by(Project_ID=Project_ID).first()
    if request.method == 'POST':
        if request.form['submit'] == 'Approve':
            ticket.Committee1_Approval = True
        db.session.commit()
        ticket = Ticket.query.filter_by(Project_ID=Project_ID).first()
        ticket = ticket.__dict__
        if request.form['submit'] == 'Approve':
            if ticket['Committee2_Approval'] == True and ticket['Committee3_Approval'] == True and ticket['Committee4_Approval'] == True and ticket['Committee5_Approval'] == True:
                send_email(ticket['Student_Email'], f'Ticket {Project_ID} Approved By Committee', 'email/ticket_approved', Ticket=ticket, Comm=0)
            return render_template('committee1.html', comm=1, Ticket=ticket, success='Project Approved. Remarks added successfully')
        else:
            #send email to existing supervisors informing them that project has been rejected
            send_email(ticket['Supervisor1_Email'], f'Ticket {Project_ID} Rejected By Committee', 'email/ticket_rejected', Ticket=ticket, Comm=1)
            if ticket['Supervisor2_Email'] != '':
                send_email(ticket['Supervisor2_Email'], f'Ticket {Project_ID} Rejected By Committee', 'email/ticket_rejected', Ticket=ticket, Comm=1)
            if ticket['Supervisor3_Email'] != '':
                send_email(ticket['Supervisor3_Email'], f'Ticket {Project_ID} Rejected By Committee', 'email/ticket_rejected', Ticket=ticket, Comm=1)
            return render_template('committee1.html', comm=1, Ticket=ticket, success='Project Rejected. Remarks added.')
    return render_template('committee1.html', comm=1, Ticket=ticket, success='')

@app.route('/comm/2/<Project_ID>', methods=['GET', 'POST'])
def comm2(Project_ID):
    ticket = Ticket.query.filter_by(Project_ID=Project_ID).first()
    if request.method == 'POST':
        if request.form['submit'] == 'Approve':
            ticket.Committee2_Approval = True
        db.session.commit()
        ticket = Ticket.query.filter_by(Project_ID=Project_ID).first()
        ticket = ticket.__dict__
        if request.form['submit'] == 'Approve':
            if ticket['Committee1_Approval'] == True and ticket['Committee3_Approval'] == True and ticket['Committee4_Approval'] == True and ticket['Committee5_Approval'] == True:
                send_email(ticket['Student_Email'], f'Ticket {Project_ID} Approved By Committee', 'email/ticket_approved', Ticket=ticket, Comm=0)
            return render_template('committee2.html', comm=2, Ticket=ticket, success='Project Approved. Remarks added successfully')
        else:
            #send email to existing supervisors informing them that project has been rejected
            send_email(ticket['Supervisor1_Email'], f'Ticket {Project_ID} Rejected By Committee', 'email/ticket_rejected', Ticket=ticket, Comm=2)
            if ticket['Supervisor2_Email'] != '':
                send_email(ticket['Supervisor2_Email'], f'Ticket {Project_ID} Rejected By Committee', 'email/ticket_rejected', Ticket=ticket, Comm=2)
            if ticket['Supervisor3_Email'] != '':
                send_email(ticket['Supervisor3_Email'], f'Ticket {Project_ID} Rejected By Committee', 'email/ticket_rejected', Ticket=ticket, Comm=2)
            return render_template('committee2.html', comm=2, Ticket=ticket, success='Project Rejected. Remarks added.')
    return render_template('committee2.html', comm=2, Ticket=ticket, success='')

@app.route('/comm/3/<Project_ID>', methods=['GET', 'POST'])
def comm3(Project_ID):
    ticket = Ticket.query.filter_by(Project_ID=Project_ID).first()
    if request.method == 'POST':
        if request.form['submit'] == 'Approve':
            ticket.Committee3_Approval = True
        db.session.commit()
        ticket = Ticket.query.filter_by(Project_ID=Project_ID).first()
        ticket = ticket.__dict__
        if request.form['submit'] == 'Approve':
            if ticket['Committee1_Approval'] == True and ticket['Committee2_Approval'] == True and ticket['Committee4_Approval'] == True and ticket['Committee5_Approval'] == True:
                send_email(ticket['Student_Email'], f'Ticket {Project_ID} Approved By Committee', 'email/ticket_approved', Ticket=ticket, Comm=0)
            return render_template('committee3.html', comm=3, Ticket=ticket, success='Project Approved. Remarks added successfully')
        else:
            #send email to existing supervisors informing them that project has been rejected
            send_email(ticket['Supervisor1_Email'], f'Ticket {Project_ID} Rejected By Committee', 'email/ticket_rejected', Ticket=ticket, Comm=3)
            if ticket['Supervisor2_Email'] != '':
                send_email(ticket['Supervisor2_Email'], f'Ticket {Project_ID} Rejected By Committee', 'email/ticket_rejected', Ticket=ticket, Comm=3)
            if ticket['Supervisor3_Email'] != '':
                send_email(ticket['Supervisor3_Email'], f'Ticket {Project_ID} Rejected By Committee', 'email/ticket_rejected', Ticket=ticket, Comm=3)
            return render_template('committee3.html', comm=3, Ticket=ticket, success='Project Rejected. Remarks added.')
    return render_template('committee3.html', comm=3, Ticket=ticket, success='')

@app.route('/comm/4/<Project_ID>', methods=['GET', 'POST'])
def comm4(Project_ID):
    ticket = Ticket.query.filter_by(Project_ID=Project_ID).first()
    if request.method == 'POST':
        if request.form['submit'] == 'Approve':
            ticket.Committee4_Approval = True
        db.session.commit()
        ticket = Ticket.query.filter_by(Project_ID=Project_ID).first()
        ticket = ticket.__dict__
        if request.form['submit'] == 'Approve':
            if ticket['Committee1_Approval'] == True and ticket['Committee2_Approval'] == True and ticket['Committee3_Approval'] == True and ticket['Committee5_Approval'] == True:
                send_email(ticket['Student_Email'], f'Ticket {Project_ID} Approved By Committee', 'email/ticket_approved', Ticket=ticket, Comm=0)
            return render_template('committee4.html', comm=4, Ticket=ticket, success='Project Approved. Remarks added successfully')
        else:
            #send email to existing supervisors informing them that project has been rejected
            send_email(ticket['Supervisor1_Email'], f'Ticket {Project_ID} Rejected By Committee', 'email/ticket_rejected', Ticket=ticket, Comm=4)
            if ticket['Supervisor2_Email'] != '':
                send_email(ticket['Supervisor2_Email'], f'Ticket {Project_ID} Rejected By Committee', 'email/ticket_rejected', Ticket=ticket, Comm=4)
            if ticket['Supervisor3_Email'] != '':
                send_email(ticket['Supervisor3_Email'], f'Ticket {Project_ID} Rejected By Committee', 'email/ticket_rejected', Ticket=ticket, Comm=4)
            return render_template('committee4.html', comm=4, Ticket=ticket, success='Project Rejected. Remarks added.')
    return render_template('committee4.html', comm=4, Ticket=ticket, success='')

@app.route('/comm/5/<Project_ID>', methods=['GET', 'POST'])
def comm5(Project_ID):
    ticket = Ticket.query.filter_by(Project_ID=Project_ID).first()
    if request.method == 'POST':
        if request.form['submit'] == 'Approve':
            ticket.Committee5_Approval = True
        db.session.commit()
        ticket = Ticket.query.filter_by(Project_ID=Project_ID).first()
        ticket = ticket.__dict__
        if request.form['submit'] == 'Approve':
            if ticket['Committee1_Approval'] == True and ticket['Committee2_Approval'] == True and ticket['Committee3_Approval'] == True and ticket['Committee4_Approval'] == True:
                send_email(ticket['Student_Email'], f'Ticket {Project_ID} Approved By Committee', 'email/ticket_approved', Ticket=ticket, Comm=0)
            return render_template('committee5.html', comm=5, Ticket=ticket, success='Project Approved. Remarks added successfully')
        else:
            #send email to existing supervisors informing them that project has been rejected
            send_email(ticket['Supervisor1_Email'], f'Ticket {Project_ID} Rejected By Committee', 'email/ticket_rejected', Ticket=ticket, Comm=5)
            if ticket['Supervisor2_Email'] != '':
                send_email(ticket['Supervisor2_Email'], f'Ticket {Project_ID} Rejected By Committee', 'email/ticket_rejected', Ticket=ticket, Comm=5)
            if ticket['Supervisor3_Email'] != '':
                send_email(ticket['Supervisor3_Email'], f'Ticket {Project_ID} Rejected By Committee', 'email/ticket_rejected', Ticket=ticket, Comm=5)
            return render_template('committee5.html', comm=5, Ticket=ticket, success='Project Rejected. Remarks added.')
    return render_template('committee5.html', comm=5, Ticket=ticket, success='')

#route for AU_Head 
@app.route('/auhead', methods=['GET', 'POST'])
def auhead():
    #check if user is logged in
    filter_approval = 'All'
    if 'email' not in session:
        return redirect(url_for('login'))
    #check if user is AU_Head
    if session['role'] != 'AU_Head':
        return redirect(url_for('login'))
    if request.method == 'GET':
        filter_approval = request.args.get('filter_approval')
    if filter_approval == 'All':
        tickets = Ticket.query.filter_by(Au=session['Au']).all()
    elif filter_approval == 'Approved':
        tickets = Ticket.query.filter_by(Au=session['Au']).filter(Ticket.Supervisor1_Approval == True, Ticket.Committee1_Approval == True, Ticket.Committee2_Approval == True, Ticket.Committee3_Approval == True).all()
        for ticket in tickets:
            if ticket.Supervisor2_Email != '':
                if ticket.Supervisor2_Approval == False:
                    tickets.remove(ticket)
            if ticket.Supervisor3_Email != '':
                if ticket.Supervisor3_Approval == False:
                    tickets.remove(ticket)
            if ticket.Committee4_Email != '':
                if ticket.Committee4_Approval == False:
                    tickets.remove(ticket)
            if ticket.Committee5_Email != '':
                if ticket.Committee5_Approval == False:
                    tickets.remove(ticket)
    elif filter_approval == 'Pending':
        #check if ticket is rejected by any of the supervisors (Supervisor1, Supervisor2[if exists], Supervisor3[if exists]) or any of the committee members (Committee1, Committee2, Committee3, Committee4[if exists], Committee5[if exists])
        tickets = Ticket.query.filter_by(Au=session['Au']).filter(Ticket.Supervisor1_Approval == False, Ticket.Committee1_Approval == False, Ticket.Committee2_Approval == False, Ticket.Committee3_Approval == False).all()
        for ticket in tickets:
            if ticket.Supervisor2_Email != '':
                if ticket.Supervisor2_Approval == True:
                    tickets.remove(ticket)
            if ticket.Supervisor3_Email != '':
                if ticket.Supervisor3_Approval == True:
                    tickets.remove(ticket)
            if ticket.Committee4_Email != '':
                if ticket.Committee4_Approval == True:
                    tickets.remove(ticket)
            if ticket.Committee5_Email != '':
                if ticket.Committee5_Approval == True:
                    tickets.remove(ticket)
    tickets = Ticket.query.filter_by(Au=session['Au']).all()
    print(tickets)
    for ticket in tickets:
            if ticket.Supervisor2_Email != '':
                if ticket.Supervisor2_Approval == False:
                    ticket.Supervisor_Approval = False
                else:
                    ticket.Supervisor_Approval = True
            if ticket.Supervisor3_Email != '':
                if ticket.Supervisor3_Approval == False:
                    ticket.Supervisor_Approval = False
                else:
                    ticket.Supervisor_Approval = True
        #check if ticket is approved by all committee members
            if ticket.Committee1_Approval == False:
                ticket.Committee_Approval = False
            elif ticket.Committee2_Approval == False:
                ticket.Committee_Approval = False
            elif ticket.Committee3_Approval == False:
                ticket.Committee_Approval = False
            if ticket.Committee4_Email != '':
                if ticket.Committee4_Approval == False:
                    ticket.Committee_Approval = False
                else:
                    ticket.Committee_Approval = True
            if ticket.Committee5_Email != '':
                if ticket.Committee5_Approval == False:
                    ticket.Committee_Approval = False
                else:
                    ticket.Committee_Approval = True
    #if ticket has been approved by AU_Head, then remove it from the list
    for ticket in tickets:
        if ticket.Au_Approval == True:
            tickets.remove(ticket)
    tickets = [ticket.__dict__ for ticket in tickets]
    return render_template('auhead.html', Tickets=tickets, success='', last_date=last_date)

#route for AU_Head approve
@app.route('/auhead/<int:Project_ID>/approve', methods=['GET', 'POST'])
def auhead_approve(Project_ID):
    #check if user is logged in
    if 'email' not in session:
        return redirect(url_for('login'))
    #check if user is AU_Head
    if session['role'] != 'AU_Head':
        return redirect(url_for('login'))
    ticket = Ticket.query.filter_by(Project_ID=Project_ID).first()
    if request.method == 'POST':
        ticket.Au_Approval = True
        db.session.commit()
        ticket = ticket.__dict__
        return render_template('auhead.html', success='Project Approved.', last_date=last_date)
    return render_template('auhead.html', Ticket=ticket, success='')

#route for AU_Head approve all where supervisor approval is true and committee approval is true
@app.route('/auhead/approve_all', methods=['GET', 'POST'])
def auhead_approve_all():
    #check if user is logged in
    if 'email' not in session:
        return redirect(url_for('login'))
    #check if user is AU_Head
    if session['role'] != 'AU_Head':
        return redirect(url_for('login'))
    tickets = Ticket.query.filter_by(Au=session['Au']).all()
    for ticket in tickets:
        if ticket.Supervisor_Approval == True and ticket.Committee_Approval == True:
            ticket.Au_Approval = True
            db.session.commit()
    return render_template('auhead.html', success='All projects approved.', last_date=last_date)


#route for Adordc
@app.route('/adordc', methods=['GET', 'POST'])
def adordc():
    #check if user is logged in
    if 'email' not in session:
        return redirect(url_for('login'))
    #check if user is Adordc
    if session['role'] != 'admin':
        return redirect(url_for('login'))
    #select all tickets where Au_Approval is True
    tickets = Ticket.query.filter_by(Au_Approval=True).all()
    #if get request, then filter tickets based on filter_au 
    print(tickets)
    if request.method == 'GET':
        filter_au = request.args.get('filter_au')
        if filter_au != '':
            tickets = Ticket.query.filter_by(Au=filter_au).filter_by(Au_Approval=True).all()
            tickets = [ticket.__dict__ for ticket in tickets]
            render_template('adordc.html', Tickets=tickets, success='')
        #convert tickets to dictionary
        tickets = [ticket.__dict__ for ticket in tickets]
        render_template('adordc.html', tickets=tickets, success='', last_date=last_date)
    return render_template('adordc.html', Tickets=tickets, success='', last_date=last_date)

#route for Adordc approve
@app.route('/adordc/<int:Project_ID>/approve', methods=['GET', 'POST'])
def adordc_approve(Project_ID):
    #check if user is logged in
    if 'email' not in session:
        return redirect(url_for('login'))
    #check if user is Adordc
    if session['role'] != 'Adordc':
        return redirect(url_for('login'))
    ticket = Ticket.query.filter_by(Project_ID=Project_ID).first()
    if request.method == 'POST':
        ticket.Adordc_Approval = True
        db.session.commit()
        ticket = ticket.__dict__
        return render_template('adordc.html', success='Project Approved.', last_date=last_date)
    return render_template('adordc.html', Ticket=ticket, success='', last_date=last_date)

#route for Adordc approve all where au approval is true
@app.route('/adordc/approve_all', methods=['GET', 'POST'])
def adordc_approve_all():
    #check if user is logged in
    if 'email' not in session:
        return redirect(url_for('login'))
    #check if user is Adordc
    if session['role'] != 'Adordc':
        return redirect(url_for('login'))
    tickets = Ticket.query.filter_by(Au_Approval=True).all()
    for ticket in tickets:
        ticket.Adordc_Approval = True
        db.session.commit()
    return render_template('adordc.html', success='All projects approved.', last_date=last_date)

#manage last date page
@app.route('/last_date', methods=['GET', 'POST'])
def last_date():
    if session['role'] != 'admin':
        return redirect(url_for('login'))
    #if last date in database is set then get it from database
    if LastDate.query.first() != None:
        last_date = LastDate.query.first().LastDate
        return render_template('last_date.html', success='Last Date already set: {}'.format(last_date))
    #if last date in database is not set then set it
    if request.method == 'POST':
        last_date = request.form['last_date']
        #convert last date to datetime object
        last_date = datetime.strptime(last_date, '%Y-%m-%d')
        last_date = LastDate(LastDate=last_date)
        db.session.add(last_date)
        db.session.commit()
        last_date = LastDate.query.first().LastDate
        return render_template('last_date.html', success='Last Date set: {}'.format(last_date))
    return render_template('last_date.html', success='')
@app.route('/xl')
def xl():
    for Au in range(1, 18):
        headers = ['RollNo', 'Name', 'Email', 'DateOfRegistration', 'Title', 'DateofIRB', 'DateofProgressPresentation', 'Name of Supervisors(list)', 'Approval of Supervisors (List)', 'Total Marks (List)']
        tickets = Ticket.query.filter_by(Au=Au).all()
        tickets = [ticket.__dict__ for ticket in tickets]
        with open(f'au{Au}.csv', 'w') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            for ticket in tickets:
                data = [ticket['RollNo'], ticket['Student_Name'], ticket['Student_Email'], ticket['Date_Of_Registration'], ticket['Project_Title'], ticket['Date_Of_IRB'], ticket['Date_of_ProgressPresentation']]
                Supervisors_Names = [ticket['Supervisor_1_Name'], ticket['Supervisor_2_Name'], ticket['Supervisor_3_Name']]
                Supervisors_Approval = [ticket['Supervisor_1_Approval'], ticket['Supervisor_2_Approval'], ticket['Supervisor_3_Approval']]
                Supervisors_Marks = [ticket['Supervisor_1_Marks'], ticket['Supervisor_2_Marks'], ticket['Supervisor_3_Marks']]
                data.append(Supervisors_Names)
                data.append(Supervisors_Approval)
                data.append(Supervisors_Marks)
                writer.writerow(data)
    with zipfile('all_au.zip', 'w') as zipObj:
        for Au in range(1, 18):
            zipObj.write(f'au{Au}.csv')
    return send_file('all_au.zip', as_attachment=True)

@app.route('/xl/<int:Au>')
def xl_au(Au):
    headers = ['RollNo', 'Name', 'Email', 'DateOfRegistration', 'Title', 'DateofIRB', 'DateofProgressPresentation', 'Name of Supervisors(list)', 'Approval of Supervisors (List)', 'Total Marks (List)']
    tickets = Ticket.query.filter_by(Au=Au).all()
    tickets = [ticket.__dict__ for ticket in tickets]
    with open(f'au{Au}.csv', 'w') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for ticket in tickets:
            data = [ticket['RollNo'], ticket['Student_Name'], ticket['Student_Email'], ticket['Date_Of_Registration'], ticket['Project_Title'], ticket['Date_Of_IRB'], ticket['Date_of_ProgressPresentation']]
            Supervisors_Names = [ticket['Supervisor_1_Name'], ticket['Supervisor_2_Name'], ticket['Supervisor_3_Name']]
            Supervisors_Approval = [ticket['Supervisor_1_Approval'], ticket['Supervisor_2_Approval'], ticket['Supervisor_3_Approval']]
            Supervisors_Marks = [ticket['Supervisor_1_Marks'], ticket['Supervisor_2_Marks'], ticket['Supervisor_3_Marks']]
            data.append(Supervisors_Names)
            data.append(Supervisors_Approval)
            data.append(Supervisors_Marks)
            writer.writerow(data)
    return send_file(f'au{Au}.csv', as_attachment=True)

@app.route('/xl/archived')
def xl_archived():
    for Au in range(1, 18):
        headers = ['RollNo', 'Name', 'Email', 'DateOfRegistration', 'Title', 'DateofIRB', 'DateofProgressPresentation', 'Name of Supervisors(list)', 'Approval of Supervisors (List)', 'Total Marks (List)', 'Last Date']
        tickets = Archive_Ticket.query.filter_by(Au=Au).all()
        tickets = [ticket.__dict__ for ticket in tickets]
        with open(f'au{Au}.csv', 'w') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            for ticket in tickets:
                data = [ticket['RollNo'], ticket['Student_Name'], ticket['Student_Email'], ticket['Date_Of_Registration'], ticket['Project_Title'], ticket['Date_Of_IRB'], ticket['Date_of_ProgressPresentation']]
                Supervisors_Names = [ticket['Supervisor_1_Name'], ticket['Supervisor_2_Name'], ticket['Supervisor_3_Name']]
                Supervisors_Approval = [ticket['Supervisor_1_Approval'], ticket['Supervisor_2_Approval'], ticket['Supervisor_3_Approval']]
                Supervisors_Marks = [ticket['Supervisor_1_Marks'], ticket['Supervisor_2_Marks'], ticket['Supervisor_3_Marks']]
                data.append(Supervisors_Names)
                data.append(Supervisors_Approval)
                data.append(Supervisors_Marks)
                data.append(ticket['LastDate'])
                writer.writerow(data)
    with zipfile('all_au.zip', 'w') as zipObj:
        for Au in range(1, 18):
            zipObj.write(f'au{Au}.csv')
    return send_file('all_au.zip', as_attachment=True)

@app.route('/first_time')
def first_time():
    #if no admin is present, allow to create one
    if User.query.filter_by(role='admin').first() is None:
        return render_template('first_time.html', success='', error='')
    else:
        return redirect(url_for('login'))

@app.route('/first_time', methods=['POST'])
def first_time_post():
    if User.query.filter_by(role='admin').first() is None:
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')
        Au = 0
        user = User(email=email, password=generate_password_hash(password, method='sha256'), name=name, role='admin', Au=Au)
        db.session.add(user)
        db.session.commit()
        return render_template('first_time.html', success='Account Created Successfully', error='')
    else:
        return redirect(url_for('login'))

#send email using flask-mail sending /ticket_created html in body of email
def send_email(to, subject, template, **kwargs):
    msg = Message(app.config['MAIL_SUBJECT_PREFIX'] + ' ' + subject, recipients=[to])
    msg.html = render_template(template + '.html', **kwargs)
    # msg.attach(attachment)
    mail.send(msg)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS