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
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.secret_key = 'secret key'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'tempmail.xlcsgo@gmail.com'
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEFAULT_SENDER'] = 'tempmail.xlcsgo@gmail.com'
app.config['MAIL_SUBJECT_PREFIX'] = 'PhD Monitoring System:'
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
    Supervisor_Name = db.Column(db.String(500), nullable=False)
    Supervisor_Email = db.Column(db.String(500), nullable=False)
    Supervisor_Remarks = db.Column(db.String(500))
    Supervisor_Approval = db.Column(db.String(500))
    Committee_Name = db.Column(db.Integer, nullable=False)
    Committee_Email = db.Column(db.String(50), nullable=False)
    Committee_Remarks = db.Column(db.String(50))
    Committee_Approval = db.Column(db.Integer)
    Au_Approval = db.Column(db.Boolean)
    Adordc_Approval = db.Column(db.Boolean)
    LastDate = db.Column(db.DateTime, nullable=False)

class Archive_Ticket(db.Model):
    Project_ID = db.Column(db.Integer, primary_key=True)
    Roll_No = db.Column(db.String(50), nullable=False)
    Student_Name = db.Column(db.String(50), nullable=False)
    Student_Email = db.Column(db.String(50), nullable=False)
    Au = db.Column(db.String(50), nullable=False)
    Date_Of_Registration = db.Column(db.DateTime, nullable=False)
    Gate = db.Column(db.Boolean, nullable=False)
    Project_Title = db.Column(db.String(50), nullable=False)
    Date_Of_IRB = db.Column(db.DateTime, nullable=False)
    Date_Of_Progress_Presentation = db.Column(db.DateTime, nullable=False)
    File_Path = db.Column(db.String(50), nullable=False)
    Publications = db.Column(db.String(50))
    Conferences = db.Column(db.String(50))
    Supervisor_Name = db.Column(db.String(50), nullable=False)
    Supervisor_Email = db.Column(db.String(50), nullable=False)
    Supervisor_Remarks = db.Column(db.String(50))
    Supervisor_Approval = db.Column(db.Integer)
    Committee_Name = db.Column(db.Integer, nullable=False)
    Committee_Email = db.Column(db.String(50), nullable=False)
    Committee_Remarks = db.Column(db.String(50))
    Committee_Approval = db.Column(db.Integer)
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
        new_ticket = Ticket(Student_Name=student_name, Student_Email=student_email, Roll_No=Roll_No, Au=Au, Date_Of_Registration=Date_Of_Registration, Gate=Gate, Project_Title=Project_Title, Date_Of_Progress_Presentation=Date_Of_Progress_Presentation, Date_Of_IRB=Date_Of_IRB, Publications=Publications, Conferences=Conferences, Au_Approval=Au_Approval, Adordc_Approval=Adordc_Approval, File_Path=file_path, LastDate=lastdate)        
        form_data = request.form
        supN = ""
        supE = ""
        comN = ""
        comE = ""
        for key in form_data:
            #if key starts with supervisor_name
            if key.startswith('supervisor_name'):
                #get the index of the supervisor
                index = key.split('_')[-1]
                #get the name of the supervisor
                name = form_data[key]
                supN += name + ";"
            if key.startswith('supervisor_email'):
                #get the index of the supervisor
                index = key.split('_')[-1]
                #get the name of the supervisor
                email = form_data[key]
                supE += email + ";"
            if key.startswith('committee_name'):
                #get the index of the supervisor
                index = key.split('_')[-1]
                #get the name of the supervisor
                name = form_data[key]
                comN += name + ";"
            if key.startswith('committee_email'):
                #get the index of the supervisor
                index = key.split('_')[-1]
                #get the name of the supervisor
                email = form_data[key]
                comE += email + ";"
        new_ticket.Supervisor_Name = supN
        new_ticket.Supervisor_Email = supE
        new_ticket.Committee_Name = comN
        new_ticket.Committee_Email = comE
        print(supN, supE, comN, comE)
        supA = ""
        for i in range(len(supN)):
            supA += "0;"
        new_ticket.Supervisor_Approval = supA
        comA = ""
        for i in range(len(comN)):
            comA += "0;"
        new_ticket.Committee_Approval = comA
        db.session.add(new_ticket)
        db.session.commit()
        ticket = Ticket.query.filter_by(Student_Email=student_email).first()
        Project_ID = ticket.Project_ID
        send_email(student_email, 'Thesis Submitted', 'email/ticket_created', Ticket=ticket)
        print(request.form)
        for i in supE.split(';'):
            send_email(i, 'Thesis Submitted', 'email/ticket_created', Ticket=ticket)
        return render_template('create_ticket.html', success='Ticket created successfully', Project_ID=Project_ID)
    return render_template('create_ticket.html', success='')

@app.route('/ticket_created/<Project_ID>')
def ticket_created(Project_ID):
    ticket = Ticket.query.filter_by(Project_ID=Project_ID).first()
    ticket = ticket.__dict__
    return render_template('ticket_created.html', Ticket=ticket, success='')

@app.route('/file/<Project_ID>')
def file(Project_ID):
    ticket = Ticket.query.filter_by(Project_ID=Project_ID).first()
    file_path = ticket.File_Path
    return send_file(file_path, as_attachment=True)

@app.route('/supervisor/<Project_ID>', methods=['GET', 'POST'])
def supervisor(Project_ID):
    if request.method == 'POST':
        Supervisor_Email = request.form['supervisor-email']
        ticket = Ticket.query.filter_by(Project_ID=Project_ID).first()
        #check index of supervisor email in ticket.Supervisor_Email which is a string of all emails separated by ';'
        #then insert total-percentage into ticket.Supervisor_Marks at that index in the string of all marks separated by ';'
        supE = ticket.Supervisor_Email.split(';')
        #find index of email in supE
        index = supE.index(Supervisor_Email)
        #insert total-percentage into ticket.Supervisor_Marks at that index in the string of all marks separated by ';'
        supM = ticket.Supervisor_Marks.split(';')
        supM[index] = request.form['total-percentage']
        ticket.Supervisor_Marks = ''.join(supM, ';')
        #insert supervisor-remarks into ticket.Supervisor_Remarks at that index in the string of all remarks separated by ';'
        supR = ticket.Supervisor_Remarks.split(';')
        supR[index] = request.form['supervisor-remarks']
        ticket.Supervisor_Remarks = ''.join(supR, ';')
        #if submit value = Satisfactory, set Supervisor_Approval at that index in the string of all approvals separated by ';' to 1
        if request.form['submit'] == 'Satisfactory':
            supA = ticket.Supervisor_Approval.split(';')
            supA[index] = '1'
            ticket.Supervisor_Approval = ''.join(supA, ';')
        elif request.form['submit'] == 'Unsatisfactory':
            supA = ticket.Supervisor_Approval.split(';')
            supA[index] = '-1'
            ticket.Supervisor_Approval = ''.join(supA, ';')
        db.session.commit()
        #if for each supervisor email in ticket.Supervisor_Email, the corresponding approval in ticket.Supervisor_Approval is 1, then send an email to all the committee members
        for i in range(len(supE)):
            if supA[i] == '1':
                continue
            else:
                break
        else:
            for i in ticket.Committee_Email.split(';'):
                    ticket = Ticket.query.filter_by(Project_ID=Project_ID).first()
                    ticket = ticket.__dict__
                    send_email(i, 'Thesis Approved by Supervisors', 'email/ticket_created', Ticket=ticket)
        return redirect(url_for('supervisor', Project_ID=Project_ID))
    ticket = Ticket.query.filter_by(Project_ID=Project_ID).first()
    ticket = ticket.__dict__
    return render_template('supervisor.html', Ticket=ticket)

@app.route('/committee/<Project_ID>', methods=['GET', 'POST'])
def committee(Project_ID):
    if request.method == "POST":
        Committee_Email = request.form['committee-email']
        ticket = Ticket.query.filter_by(Project_ID=Project_ID).first()
        #check index of committee email in ticket.Committee_Email which is a string of all emails separated by ';'
        #then insert total-percentage into ticket.Committee_Marks at that index in the string of all marks separated by ';'
        comE = ticket.Committee_Email.split(';')
        #find index of email in comE
        index = comE.index(Committee_Email)
        #if submit value = Satisfactory, set Committee_Approval at that index in the string of all approvals separated by ';' to 1
        if request.form['submit'] == 'Satisfactory':
            comA = ticket.Committee_Approval.split(';')
            comA[index] = '1'
            ticket.Committee_Approval = ''.join(comA, ';')
        elif request.form['submit'] == 'Unsatisfactory':
            comA = ticket.Committee_Approval.split(';')
            comA[index] = '-1'
            ticket.Committee_Approval = ''.join(comA, ';')
        db.session.commit()
        return redirect(url_for('committee', Project_ID=Project_ID))
    else:
        ticket = Ticket.query.filter_by(Project_ID=Project_ID).first()
        ticket = ticket.__dict__
        return render_template('committee.html', Ticket=ticket)

@app.route('/auhead')
def auhead():
    if 'email' not in session:
        return redirect(url_for('login'))
    if session['role'] != 'AU_Head':
        return redirect(url_for('login'))
    Au = session['Au']
    tickets = Ticket.query.filter_by(Au=Au).all()
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
    tickets = [ticket.__dict__ for ticket in tickets]
    for ticket in tickets:
        for i in ticket['Supervisor_Approval'].split(';'):
            if i == '-1':
                tickets.remove(ticket)
                break
        for i in ticket['Committee_Approval'].split(';'):
            if i == '-1':
                tickets.remove(ticket)
                break
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
    tickets = [ticket.__dict__ for ticket in tickets]
    for ticket in tickets:
        for i in ticket['Supervisor_Approval'].split(';'):
            if i == '1':
                tickets.remove(ticket)
                break
        for i in ticket['Committee_Approval'].split(';'):
            if i == '-1':
                tickets.remove(ticket)
                break
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
        for i in ticket.Supervisor_Approval.split(';'):
            if i == '-1':
                flag = False
                break
            else:
                flag = True
        for i in ticket.Committee_Approval.split(';'):
            if i == '-1':
                flag = False
                break
            else:
                flag = True
        if flag == True:
            ticket.Au_Approval = True
            db.session.commit()
    tickets = [ticket.__dict__ for ticket in tickets]
    return render_template('auhead.html', success='All projects approved.', last_date=last_date, Tickets=tickets)



@app.route('/adordc', methods=['GET', 'POST'])
def adordc():
    
    if 'email' not in session:
        return redirect(url_for('login'))
    
    if session['role'] != 'admin':
        return redirect(url_for('login'))
    
    tickets = Ticket.query.all()
    Tts = []
    for au in range(16):
        Tts.append(len(Ticket.query.filter_by(Au=au).all()))
    Tas = []
    for au in range(16):
        Tas.append(len(Ticket.query.filter_by(Au=au, Au_Approval=True).all()))
    Tps = []
    for au in range(16):
        Tps.append(len(Ticket.query.filter_by(Au=au, Au_Approval=False).all()))
    return render_template('adordc.html', Tickets=tickets, success='', last_date=last_date, Au=Au_list, Tts=Tts, Tas=Tas, Tps=Tps)





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

@app.route('/last_date/delete', methods=['GET', 'POST'])
def last_date_delete():
    if session['role'] != 'admin':
        return redirect(url_for('login'))
    if LastDate.query.first() != None:
        last_date = LastDate.query.first()
        db.session.delete(last_date)
        db.session.commit()
        #move all projects to archive
        tickets = Ticket.query.all()
        for ticket in tickets:
            archive_ticket = Archive_Ticket()
            for column in Ticket.__table__.columns:
                setattr(archive_ticket, column.name, getattr(ticket, column.name))
            db.session.add(archive_ticket)
            db.session.delete(ticket)
        db.session.commit()
        print('archive done')
        return render_template('last_date.html', success='Last Date deleted')
    return render_template('last_date.html', success='Last Date not set')

@app.route('/xl')
def xl():
    for Au in Au_list:
        headers = ['RollNo', 'Name', 'Email', 'DateOfRegistration', 'Title', 'DateofIRB', 'DateofProgressPresentation', 'Supervisors', 'Supervisors_Approval', 'Supervisors_Marks']
        Au_index = Au_list.index(Au)
        Au_index = Au_index + 1
        tickets = Ticket.query.filter_by(Au=Au_index).all()
        tickets = [ticket.__dict__ for ticket in tickets]
        with open(f'Project Submissions for {Au}.csv', 'w') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            for ticket in tickets:
                data = [ticket['Roll_No'], ticket['Student_Name'], ticket['Student_Email'], ticket['Date_Of_Registration'], ticket['Project_Title'], ticket['Date_Of_IRB'], ticket['Date_Of_Progress_Presentation'],ticket['Supervisor_Name'], ticket['Supervisor_Approval'], ticket['Supervisor_Marks']]
                data = dict(zip(headers, data))
                writer.writerow(data)
    with zipfile('all_au.zip', 'w') as zipObj:
        for Au in Au_list:
            zipObj.write(f'Project Submissions for {Au}.csv')
    return send_file('all_au.zip', as_attachment=True)

@app.route('/xl/au')
def xl_au():
    Au = session['Au']
    headers = ['RollNo', 'Name', 'Email', 'DateOfRegistration', 'Title', 'DateofIRB', 'DateofProgressPresentation', 'Supervisors', 'Supervisors_Approval', 'Supervisors_Marks']
    tickets = Ticket.query.filter_by(Au=Au).all()
    tickets = [ticket.__dict__ for ticket in tickets]
    with open(f'au{Au}.csv', 'w') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for ticket in tickets:
            data = [ticket['Roll_No'], ticket['Student_Name'], ticket['Student_Email'], ticket['Date_Of_Registration'], ticket['Project_Title'], ticket['Date_Of_IRB'], ticket['Date_Of_Progress_Presentation'],ticket['Supervisor_Name'], ticket['Supervisor_Approval'], ticket['Supervisor_Marks']]
            data = dict(zip(headers, data))
            writer.writerow(data)
    return send_file(f'au{Au}.csv', as_attachment=True)

@app.route('/xl/archived')
def xl_archived():
    for Au in Au_list:
        headers = ['RollNo', 'Name', 'Email', 'DateOfRegistration', 'Title', 'DateofIRB', 'DateofProgressPresentation', 'Supervisor1', 'Supervisor1_Approval', 'Supervisor1_Marks', 'Supervisor2', 'Supervisor2_Approval', 'Supervisor2_Marks', 'Supervisor3', 'Supervisor3_Approval', 'Supervisor3_Marks', 'Last Date']
        Au_index = Au_list.index(Au)
        Au_index = Au_index + 1
        tickets = Archive_Ticket.query.filter_by(Au=Au_index).all()
        tickets = [ticket.__dict__ for ticket in tickets]
        with open(f'Project Submissions for {Au}.csv', 'w') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            for ticket in tickets:
                data = [ticket['Roll_No'], ticket['Student_Name'], ticket['Student_Email'], ticket['Date_Of_Registration'], ticket['Project_Title'], ticket['Date_Of_IRB'], ticket['Date_Of_Progress_Presentation'],ticket['Supervisor1_Name'], ticket['Supervisor1_Approval'], ticket['Supervisor1_Marks'],ticket['Supervisor2_Name'], ticket['Supervisor2_Approval'], ticket['Supervisor2_Marks'],ticket['Supervisor3_Name'], ticket['Supervisor3_Approval'], ticket['Supervisor3_Marks'], ticket['LastDate']]
                data = dict(zip(headers, data))
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

@app.route("/dr_a")
def dr_a():
    #send email to dr_a with link to /xl 
    send_email('dr_a@thapar.edu', 'Thesis Submissions', 'email/dr_a', link= url_for('xl', _external=True))
    return redirect(url_for('adordc'))

def send_email(to, subject, template, **kwargs):
    # msg = Message(app.config['MAIL_SUBJECT_PREFIX'] + ' ' + subject, recipients=[to])
    # msg.html = render_template(template + '.html', **kwargs)
    
    # mail.send(msg)
    return print('Email Sent, but not really', to, subject, template, kwargs)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    app.run(host='0.0.0.0', port= Port)