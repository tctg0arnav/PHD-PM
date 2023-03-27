from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from flask_redmail import RedMail
from redmail import gmail
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email
import os
import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.secret_key = 'secret key'
app.config["EMAIL_HOST"] = gmail.host
app.config["EMAIL_PORT"] = gmail.port
app.config['EMAIL_USERNAME'] = 'tempmail.xlcsgo@gmail.com'
app.config['EMAIL_PASSWORD'] = 'jjjthrbdtohkiomc'
app.config['EMAIL_SENDER'] = 'tempmail.xlcsgo@gmail.com'
email = RedMail(app)


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
    Supervisor2_Name = db.Column(db.String(50))
    Supervisor2_Email = db.Column(db.String(50))
    Supervisor2_Approval = db.Column(db.Boolean)
    Supervisor2_Remarks = db.Column(db.String(100))
    Supervisor3_Name = db.Column(db.String(50))
    Supervisor3_Email = db.Column(db.String(50))
    Supervisor3_Approval = db.Column(db.Boolean)
    Supervisor3_Remarks = db.Column(db.String(100))
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

#use WTF forms for this
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                session['email'] = user.email
                session['role'] = user.role
                session['Au'] = user.Au
                return redirect(url_for('home'))
        return render_template('login.html', form=form, error='Invalid email or password')
    return render_template('login.html', form=form)

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
        role = request.form['role']
        name = request.form['name']
        Au = request.form['Au']
        user = User.query.filter_by(email=email).first()
        if user:
            return render_template('register.html', error='Email already exists')
        new_user = User(email=email, password=generate_password_hash(password, method='sha256'), role=role, name=name, Au=Au)
        db.session.add(new_user)
        db.session.commit()
        return render_template('register.html', success='User created successfully')
    return render_template('register.html')

@app.route('/unapproved_users', methods=['GET', 'POST'])
def unapproved_users():
    if session.get('role') == 'admin':
        unapproved_users = Unapproved_Users.query.all()
        return render_template('unapproved_users.html', unapproved_users=unapproved_users)
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
        Date_Of_IRB = request.form['Date_Of_IRB']
        Supervisor1_Name = request.form['Supervisor1_Name']
        Supervisor1_Email = request.form['Supervisor1_Email']
        Supervisor1_Approval = False
        Supervisor1_Remarks = ''
        #Supervisor2 and Supervisor3 are optional
        if request.form['Supervisor2_Name'] != '':
            Supervisor2_Name = request.form['Supervisor2_Name']
            Supervisor2_Email = request.form['Supervisor2_Email']
            Supervisor2_Approval = False
            Supervisor2_Remarks = ''
        else:
            Supervisor2_Name = ''
            Supervisor2_Email = ''
            Supervisor2_Approval = False
            Supervisor2_Remarks = ''
        if request.form['Supervisor3_Name'] != '':
            Supervisor3_Name = request.form['Supervisor3_Name']
            Supervisor3_Email = request.form['Supervisor3_Email']
            Supervisor3_Approval = False
            Supervisor3_Remarks = ''
        else:
            Supervisor3_Name = ''
            Supervisor3_Email = ''
            Supervisor3_Approval = False
            Supervisor3_Remarks = ''
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
        Committee4_Name = request.form['Committee4_Name']
        Committee4_Email = request.form['Committee4_Email']
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
        file = request.files.get('file')
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if Publications != '':
            Publications = request.form['Publications']
        else:
            Publications = ''
        if Conferences != '':
            Conferences = request.form['Conferences']
        else:
            Conferences = ''
        new_ticket = Ticket(student_name=student_name, student_email=student_email, Roll_No=Roll_No, Au=Au, Date_Of_Registration=Date_Of_Registration, Gate=Gate, Project_Title=Project_Title, Date_Of_Progress_Presentation=Date_Of_Progress_Presentation, Date_Of_IRB=Date_Of_IRB, Supervisor1_Name=Supervisor1_Name, Supervisor1_Email=Supervisor1_Email, Supervisor1_Approval=Supervisor1_Approval, Supervisor1_Remarks=Supervisor1_Remarks, Supervisor2_Name=Supervisor2_Name, Supervisor2_Email=Supervisor2_Email, Supervisor2_Approval=Supervisor2_Approval, Supervisor2_Remarks=Supervisor2_Remarks, Supervisor3_Name=Supervisor3_Name, Supervisor3_Email=Supervisor3_Email, Supervisor3_Approval=Supervisor3_Approval, Supervisor3_Remarks=Supervisor3_Remarks, Committee1_Name=Committee1_Name, Committee1_Email=Committee1_Email, Committee1_Approval=Committee1_Approval, Committee1_Remarks=Committee1_Remarks, Committee2_Name=Committee2_Name, Committee2_Email=Committee2_Email, Committee2_Approval=Committee2_Approval, Committee2_Remarks=Committee2_Remarks, Committee3_Name=Committee3_Name, Committee3_Email=Committee3_Email, Committee3_Approval=Committee3_Approval, Committee3_Remarks=Committee3_Remarks, Committee4_Name=Committee4_Name, Committee4_Email=Committee4_Email, Committee4_Approval=Committee4_Approval, Committee4_Remarks=Committee4_Remarks, Committee5_Name=Committee5_Name, Committee5_Email=Committee5_Email, Committee5_Approval=Committee5_Approval, Committee5_Remarks=Committee5_Remarks, file_path=file_path, Publications=Publications, Conferences=Conferences)
        db.session.add(new_ticket)
        db.session.commit()
        #get Project_ID
        ticket = Ticket.query.filter_by(student_email=student_email).first()
        Project_ID = ticket.Project_ID
        send_email(student_email, 'Ticket Created', 'email/ticket_created', student_name=student_name, Project_ID=Project_ID)
        return render_template('create_ticket.html', success='Ticket created successfully')
    return render_template('create_ticket.html')

#use redmail to send template html in mail
def send_email(to, subject, template, **kwargs):
    subject = 'PHDmon' + ' ' + subject
    email.send(subject,receivers=to,html_template=template, **kwargs)