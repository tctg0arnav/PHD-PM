from flask import Flask, render_template, request, redirect, url_for, session, send_file
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
import os
import psycopg2
from datetime import datetime
import dateutil.parser as dparser
from zipfile import ZipFile as zipfile
import csv

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
ALLOWED_EXTENSIONS = {'pdf'}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SCALINGO_POSTGRESQL_ALCHEMY_URL')
app.secret_key = 'secret key'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'tempmail.xlcsgo@gmail.com'
app.config['MAIL_PASSWORD'] = 'jjjthrbdtohkiomc'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEFAULT_SENDER'] = 'tempmail.xlcsgo@gmail.com'
app.config['MAIL_SUBJECT_PREFIX'] = 'PHDmon:'
Port = os.environ.get('PORT')
mail = Mail(app)
db = SQLAlchemy(app)

Au_list = ['L. M. Thapar School of Management','School of Chemistry & Biochemistry (DST-FIST Sponsored)','School of Energy and Environment (DST-FIST Sponsered)','School of Humanities & Social Sciences','School of Mathematics','School of Physics & Materials Science','Thapar School of Liberal Arts & Sciences (TSLAS)','Basic & Engineering Sciences (Dera Bassi Campus)','Chemical Engineering','Civil Engineering','Computer Science & Engineering','Department of Biotechnology','Distance Education (DDE)','Electrical & Instrumentation Engineering','Electronics & Communication Engineering','Mechanical Engineering Department']
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
    password = db.Column(db.String(300), nullable=False) 
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
                    return redirect(url_for('auhead'))
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
        
        unapproved_users = [dict(email=unapproved_user.email, password=unapproved_user.password, role=unapproved_user.role, name=unapproved_user.name, Au=unapproved_user.Au) for unapproved_user in unapproved_users]
        return render_template('unapproved_users.html', unapproved_users=unapproved_users)
    return redirect(url_for('login'))

@app.route('/manage_users', methods=['GET', 'POST'])
def manage_users():
    if session.get('role') == 'admin':
        
        users = User.query.filter(User.role != 'admin').all()
        print(users)
        
        users = [dict(email=user.email, password=user.password, role=user.role, name=user.name, Au=user.Au) for user in users]
        
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
        
        print(request.files)
        file = request.files.get('file_path', None)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], Roll_No + '.pdf')
        file.save(file_path)
        Publications = request.form['Publications']
        Conferences = request.form['Conferences']
        
        lastdate = LastDate.query.first().LastDate
        
        lastdate = lastdate.strftime('%Y-%m-%d')
        
        lastdate = dparser.parse(lastdate, fuzzy=True)
        Au_Approval = False
        Adordc_Approval = False
        
        new_ticket = Ticket(Student_Name=student_name, Student_Email=student_email, Roll_No=Roll_No, Au=Au, Date_Of_Registration=Date_Of_Registration, Gate=Gate, Project_Title=Project_Title, Date_Of_Progress_Presentation=Date_Of_Progress_Presentation, Date_Of_IRB=Date_Of_IRB, Supervisor1_Name=Supervisor1_Name, Supervisor1_Email=Supervisor1_Email, Supervisor1_Approval=Supervisor1_Approval, Supervisor1_Remarks=Supervisor1_Remarks, Committee1_Name=Committee1_Name, Committee1_Email=Committee1_Email, Committee1_Approval=Committee1_Approval, Committee1_Remarks=Committee1_Remarks, Committee2_Name=Committee2_Name, Committee2_Email=Committee2_Email, Committee2_Approval=Committee2_Approval, Committee2_Remarks=Committee2_Remarks, Committee3_Name=Committee3_Name, Committee3_Email=Committee3_Email, Committee3_Approval=Committee3_Approval, Committee3_Remarks=Committee3_Remarks, Publications=Publications, Conferences=Conferences, Au_Approval=Au_Approval, Adordc_Approval=Adordc_Approval, File_Path=file_path, Supervisor1_Marks=Supervisor1_Marks, LastDate=lastdate)        
        
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
            
            send_email(ticket['Supervisor1_Email'], f'Ticket {Project_ID} Rejected By Committee', 'email/ticket_rejected', Ticket=ticket, Comm=5)
            if ticket['Supervisor2_Email'] != '':
                send_email(ticket['Supervisor2_Email'], f'Ticket {Project_ID} Rejected By Committee', 'email/ticket_rejected', Ticket=ticket, Comm=5)
            if ticket['Supervisor3_Email'] != '':
                send_email(ticket['Supervisor3_Email'], f'Ticket {Project_ID} Rejected By Committee', 'email/ticket_rejected', Ticket=ticket, Comm=5)
            return render_template('committee5.html', comm=5, Ticket=ticket, success='Project Rejected. Remarks added.')
    return render_template('committee5.html', comm=5, Ticket=ticket, success='')


@app.route('/auhead')
def auhead():
    if 'email' not in session:
        return redirect(url_for('login'))
    if session['role'] != 'AU_Head':
        return redirect(url_for('login'))
    Au = session['Au']
    tickets = Ticket.query.filter_by(Au=Au).all()
    add_approvals(tickets)
    tickets = [ticket.__dict__ for ticket in tickets]
    return render_template('auhead.html', Au=Au, success='', Tickets=tickets)

@app.route('/auhead/approved', methods=['GET', 'POST'])
def auhead_filter():
    if 'email' not in session:
        return redirect(url_for('login'))
    if session['role'] != 'AU_Head':
        return redirect(url_for('login'))
    Au = session['Au']
    tickets = Ticket.query.filter_by(Au=Au).all()
    add_approvals(tickets)
    tickets = [ticket.__dict__ for ticket in tickets]
    for ticket in tickets:
        flag = True
        if ticket['Supervisor1_Approval'] == False or ticket['Committee1_Approval'] == False or ticket['Committee2_Approval'] == False or ticket['Committee3_Approval'] == False:
            flag = False
        if ticket['Supervisor2_Email'] != '':
            if ticket['Supervisor2_Approval'] == False:
                flag = False
        if ticket['Supervisor3_Email'] != '':
            if ticket['Supervisor3_Approval'] == False:
                flag = False
        if ticket['Committee4_Email'] != '':
            if ticket['Committee4_Approval'] == False:
                flag = False
        if ticket['Committee5_Email'] != '':
            if ticket['Committee5_Approval'] == False:
                flag = False
        if flag == False:
            tickets.remove(ticket)
        return render_template('auhead.html', Au=Au, success='', Tickets=tickets)
    return render_template('auhead.html', Au=Au, success='', Tickets=tickets)

@app.route('/auhead/pending', methods=['GET', 'POST'])
def auhead_filter2():
    if 'email' not in session:
        return redirect(url_for('login'))
    if session['role'] != 'AU_Head':
        return redirect(url_for('login'))
    Au = session['Au']
    tickets = Ticket.query.filter_by(Au=Au).all()
    add_approvals(tickets)
    tickets = [ticket.__dict__ for ticket in tickets]
    for ticket in tickets:
        flag = False
        if ticket['Supervisor1_Approval'] == False or ticket['Committee1_Approval'] == False or ticket['Committee2_Approval'] == False or ticket['Committee3_Approval'] == False:
            flag = True
        if ticket['Supervisor2_Email'] != '':
            if ticket['Supervisor2_Approval'] == False:
                flag = True
        if ticket['Supervisor3_Email'] != '':
            if ticket['Supervisor3_Approval'] == False:
                flag = True
        if ticket['Committee4_Email'] != '':
            if ticket['Committee4_Approval'] == False:
                flag = True
        if ticket['Committee5_Email'] != '':
            if ticket['Committee5_Approval'] == False:
                flag = True
        if flag == False:
            tickets.remove(ticket)
    return render_template('auhead.html', Au=Au, success='', Tickets=tickets)

@app.route('/auhead/<int:Project_ID>/approve', methods=['GET', 'POST'])
def auhead_approve(Project_ID):
    
    if 'email' not in session:
        return redirect(url_for('login'))
    
    if session['role'] != 'AU_Head':
        return redirect(url_for('login'))
    ticket = Ticket.query.filter_by(Project_ID=Project_ID).first()
    if request.method == 'POST':
        ticket.Au_Approval = True
        db.session.commit()
        ticket = ticket.__dict__
        return render_template('auhead.html', success='Project Approved.', last_date=last_date)
    return render_template('auhead.html', Ticket=ticket, success='Project Successfully Approved')


@app.route('/auhead/approve_all', methods=['GET', 'POST'])
def auhead_approve_all():
    
    if 'email' not in session:
        return redirect(url_for('login'))
    
    if session['role'] != 'AU_Head':
        return redirect(url_for('login'))
    tickets = Ticket.query.filter_by(Au=session['Au']).all()
    for ticket in tickets:
        flag = False
        if ticket.Supervisor1_Approval == True and ticket.Committee1_Approval == True and ticket.Committee2_Approval == True and ticket.Committee3_Approval == True:
            if ticket.Supervisor2_Email != '':
                if ticket.Supervisor2_Approval == True:
                    flag = True
            if ticket.Supervisor3_Email != '':
                if ticket.Supervisor3_Approval == True:
                    flag = True
            if ticket.Committee4_Email != '':
                if ticket.Committee4_Approval == True:
                    flag = True
            if ticket.Committee5_Email != '':
                if ticket.Committee5_Approval == True:
                    flag = True
            flag = True
        if flag == True:
            ticket.Au_Approval = True
            db.session.commit()
    tickets = [ticket.__dict__ for ticket in tickets]
    return render_template('auhead.html', success='All Supervisor and Committee projects approved.', last_date=last_date, Tickets=tickets)



@app.route('/adordc', methods=['GET', 'POST'])
def adordc():
    
    if 'email' not in session:
        return redirect(url_for('login'))
    
    if session['role'] != 'admin':
        return redirect(url_for('login'))
    
    tickets = Ticket.query.filter_by(Au_Approval=True).all()
    tickets = [ticket.__dict__ for ticket in tickets]
    Au = session['Au']
    return render_template('adordc.html', Tickets=tickets, success='', last_date=last_date)


@app.route('/adordc/<int:au>')
def adordc_filter(au):
    
    if 'email' not in session:
        return redirect(url_for('login'))
    
    if session['role'] != 'admin':
        return redirect(url_for('login'))
    
    tickets = Ticket.query.filter_by(Au_Approval=True, Au=au).all()
    tickets = [ticket.__dict__ for ticket in tickets]
    Au = session['Au']
    return render_template('adordc.html', Tickets=tickets, success='', last_date=last_date)


@app.route('/adordc/<int:Project_ID>/approve', methods=['GET', 'POST'])
def adordc_approve(Project_ID):
    
    if 'email' not in session:
        return redirect(url_for('login'))
    
    if session['role'] != 'Adordc':
        return redirect(url_for('login'))
    ticket = Ticket.query.filter_by(Project_ID=Project_ID).first()
    if request.method == 'POST':
        ticket.Adordc_Approval = True
        db.session.commit()
        ticket = ticket.__dict__
        return render_template('adordc.html', success='Project Approved.', last_date=last_date)
    return render_template('adordc.html', Ticket=ticket, success='', last_date=last_date)


@app.route('/adordc/approve_all', methods=['GET', 'POST'])
def adordc_approve_all():
    tickets = Ticket.query.filter_by(Au_Approval=True).all()
    for ticket in tickets:
        ticket.Adordc_Approval = True
        db.session.commit()
    tickets = Ticket.query.filter_by(Au_Approval=True).all()
    tickets = [ticket.__dict__ for ticket in tickets]
    return render_template('adordc.html', success='All projects approved.', last_date=last_date, Tickets=tickets)


@app.route('/last_date', methods=['GET', 'POST'])
def last_date():
    if session['role'] != 'admin':
        return redirect(url_for('login'))
    
    if LastDate.query.first() != None:
        last_date = LastDate.query.first().LastDate
        return render_template('last_date.html', success='Last Date already set: {}'.format(last_date))
    
    if request.method == 'POST':
        last_date = request.form['last_date']
        
        last_date = datetime.strptime(last_date, '%Y-%m-%d')
        last_date = LastDate(LastDate=last_date)
        db.session.add(last_date)
        db.session.commit()
        last_date = LastDate.query.first().LastDate
        return render_template('last_date.html', success='Last Date set: {}'.format(last_date))
    return render_template('last_date.html', success='')

@app.route('/xl')
def xl():
    for Au in Au_list:
        headers = ['RollNo', 'Name', 'Email', 'DateOfRegistration', 'Title', 'DateofIRB', 'DateofProgressPresentation', 'Supervisor1', 'Supervisor1_Approval', 'Supervisor1_Marks', 'Supervisor2', 'Supervisor2_Approval', 'Supervisor2_Marks', 'Supervisor3', 'Supervisor3_Approval', 'Supervisor3_Marks']
        Au_index = Au_list.index(Au)
        Au_index = Au_index + 1
        tickets = Ticket.query.filter_by(Au=Au_index).all()
        tickets = [ticket.__dict__ for ticket in tickets]
        with open(f'Project Submissions for {Au}.csv', 'w') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            for ticket in tickets:
                data = [ticket['Roll_No'], ticket['Student_Name'], ticket['Student_Email'], ticket['Date_Of_Registration'], ticket['Project_Title'], ticket['Date_Of_IRB'], ticket['Date_Of_Progress_Presentation'],ticket['Supervisor1_Name'], ticket['Supervisor1_Approval'], ticket['Supervisor1_Marks'],ticket['Supervisor2_Name'], ticket['Supervisor2_Approval'], ticket['Supervisor2_Marks'],ticket['Supervisor3_Name'], ticket['Supervisor3_Approval'], ticket['Supervisor3_Marks']]
                data = dict(zip(headers, data))
                writer.writerow(data)
    with zipfile('all_au.zip', 'w') as zipObj:
        for Au in Au_list:
            zipObj.write(f'Project Submissions for {Au}.csv')
    return send_file('all_au.zip', as_attachment=True)

@app.route('/xl/au')
def xl_au():
    Au = session['Au']
    headers = ['RollNo', 'Name', 'Email', 'DateOfRegistration', 'Title', 'DateofIRB', 'DateofProgressPresentation', 'Supervisor1', 'Supervisor1_Approval', 'Supervisor1_Marks', 'Supervisor2', 'Supervisor2_Approval', 'Supervisor2_Marks', 'Supervisor3', 'Supervisor3_Approval', 'Supervisor3_Marks']
    tickets = Ticket.query.filter_by(Au=Au).all()
    tickets = [ticket.__dict__ for ticket in tickets]
    with open(f'au{Au}.csv', 'w') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for ticket in tickets:
            data = [ticket['Roll_No'], ticket['Student_Name'], ticket['Student_Email'], ticket['Date_Of_Registration'], ticket['Project_Title'], ticket['Date_Of_IRB'], ticket['Date_Of_Progress_Presentation'],ticket['Supervisor1_Name'], ticket['Supervisor1_Approval'], ticket['Supervisor1_Marks'],ticket['Supervisor2_Name'], ticket['Supervisor2_Approval'], ticket['Supervisor2_Marks'],ticket['Supervisor3_Name'], ticket['Supervisor3_Approval'], ticket['Supervisor3_Marks']]
            data = dict(zip(headers, data))
            writer.writerow(data)
    return send_file(f'au{Au}.csv', as_attachment=True)

@app.route('/xl/archived')
def xl_archived():
    for Au in Au_list:
        headers = ['RollNo', 'Name', 'Email', 'DateOfRegistration', 'Title', 'DateofIRB', 'DateofProgressPresentation', 'Supervisor1', 'Supervisor1_Approval', 'Supervisor1_Marks', 'Supervisor2', 'Supervisor2_Approval', 'Supervisor2_Marks', 'Supervisor3', 'Supervisor3_Approval', 'Supervisor3_Marks']
        Au_index = Au_list.index(Au)
        Au_index = Au_index + 1
        tickets = Ticket.query.filter_by(Au=Au_index).all()
        tickets = [ticket.__dict__ for ticket in tickets]
        with open(f'Project Submissions for {Au}.csv', 'w') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            for ticket in tickets:
                data = [ticket['Roll_No'], ticket['Student_Name'], ticket['Student_Email'], ticket['Date_Of_Registration'], ticket['Project_Title'], ticket['Date_Of_IRB'], ticket['Date_Of_Progress_Presentation'],ticket['Supervisor1_Name'], ticket['Supervisor1_Approval'], ticket['Supervisor1_Marks'],ticket['Supervisor2_Name'], ticket['Supervisor2_Approval'], ticket['Supervisor2_Marks'],ticket['Supervisor3_Name'], ticket['Supervisor3_Approval'], ticket['Supervisor3_Marks']]
                writer.writerow(data)
    with zipfile('all_au.zip', 'w') as zipObj:
        for Au in Au_list:
            zipObj.write(f'Project Submissions for {Au}.csv')
    return send_file('all_au.zip', as_attachment=True)

@app.route('/first_time')
def first_time():
    print(db_maker())
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

@app.route('/db')
def db_maker():
    db.create_all()
    return 'Database Created'

def send_email(to, subject, template, **kwargs):
    msg = Message(app.config['MAIL_SUBJECT_PREFIX'] + ' ' + subject, recipients=[to])
    msg.html = render_template(template + '.html', **kwargs)
    
    mail.send(msg)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def add_approvals(tickets):
    for ticket in tickets:
        ticket = ticket.__dict__
        if ticket['Supervisor1_Approval'] == True:
            ticket['Supervisor_Approval'] = True
        else:
            ticket['Supervisor_Approval'] = False
        if ticket['Supervisor2_Email'] != '':
            if ticket['Supervisor2_Approval'] == True:
                ticket['Supervisor_Approval'] = ticket['Supervisor_Approval'] and True
            else:
                ticket['Supervisor_Approval'] = False
        if ticket['Supervisor3_Email'] != '':
            if ticket['Supervisor3_Approval'] == True:
                ticket['Supervisor_Approval'] = ticket['Supervisor_Approval'] and True
            else:
                ticket['Supervisor_Approval'] = False
        if ticket['Committee1_Approval'] == True:
            if ticket['Committee2_Approval'] == True:
                if ticket['Committee3_Approval'] == True:
                    ticket['Committee_Approval'] = True
                else:
                    ticket['Committee_Approval'] = False
            else:
                ticket['Committee_Approval'] = False
        else:
            ticket['Committee_Approval'] = False
        if ticket['Committee4_Email'] != '':
            if ticket['Committee4_Approval'] == True:
                ticket['Committee_Approval'] = ticket['Committee_Approval'] and True
        if ticket['Committee5_Email'] != '':
            if ticket['Committee5_Approval'] == True:
                ticket['Committee_Approval'] = ticket['Committee_Approval'] and True
    return tickets

if __name__ == '__main__':
    app.run(host='0.0.0.0', port= Port)