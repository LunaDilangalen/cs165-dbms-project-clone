from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://cs165project:cs165project@localhost/dilangalen'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

# CREATE TABLE CardOption (
# 	card_option			  int NOT NULL AUTO_INCREMENT,
# 	card_association	varchar(30),
# 	card_type			    varchar(30),
#
# 	PRIMARY KEY (card_option)
# );

class CardOption(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    card_association = db.Column(db.String(20))
    card_type = db.Column(db.String(20))
    application = db.relationship('Application', backref='card_option', lazy=True)

    def __repr__(self):
        return "<CardOption %r>" %self.id


# CREATE TABLE PersonalInformation (
# 	person_ID				int NOT NULL,
# 	full_name		    varchar(50),
# 	education		    varchar(50),
# 	birthdate		    date,
# 	birthplace		  varchar(50),
# 	sex				      varchar(10),
# 	phone_number	  varchar(15),
# 	email_address	  varchar(50),
# 	present_address	varchar(200),
#
# 	PRIMARY KEY (person_ID),
# 	UNIQUE (full_name, phone_number, email_address)
# );

class Person(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('application.person_id'), primary_key=True)
    full_name = db.Column(db.String(50), nullable=False)
    education = db.Column(db.String(50))
    birthdate = db.Column(db.DateTime)
    birthplace = db.Column(db.String(50))
    sex = db.Column(db.String(10))
    phone_number = db.Column(db.String(11), nullable=False)
    email_address = db.Column(db.String(100), nullable=False)
    present_address = db.Column(db.String(200))
    employment_type = db.Column(db.String(50))
    job_title = db.Column(db.String(50))
    tenure = db.Column(db.Integer)
    gross_annual_income = db.Column(db.Float)

    def __repr__(self):
        return "<PersonalInformation %r>" %self.id

# CREATE TABLE OwnedCard (
# 	card_number		varchar(25) NOT NUll,
# 	member_since	date,
# 	credit_limit	numeric(15,2),
#
# 	PRIMARY KEY (card_number)
# );

class OwnedCard(db.Model):
    card_number = db.Column(db.String(25), db.ForeignKey('application.card_number'), primary_key=True)
    member_since = db.Column(db.DateTime)
    credit_limit = db.Column(db.Float)

    def __repr__(self):
        return "<OwnedCard %r>" %self.number

# CREATE TABLE CreditCardApplicationInfo (
#   application_ID    int NOT NULL AUTO_INCREMENT,
# 	card_option		    int NOT NULL,
# 	person_ID				  int NOT NUll,
# 	card_number		    varchar(25) NOT NULL,
#
#   PRIMARY KEY (application_ID),
#   UNIQUE (card_option, person_ID, card_number),
# 	FOREIGN KEY (card_option) REFERENCES CardOption(card_option) ON DELETE CASCADE,
# 	FOREIGN KEY (person_ID) REFERENCES PersonalInformation(person_ID) ON DELETE CASCADE,
# 	FOREIGN KEY (card_number) REFERENCES OwnedCard(card_number) ON DELETE CASCADE
# );

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    card_option_id = db.Column(db.Integer, db.ForeignKey('card_option.id'), nullable=False)
    person_id = db.Column(db.Integer, unique=True, nullable=False)
    card_number = db.Column(db.String(25), unique=True, nullable=False)
    person = db.relationship('Person', cascade='all, delete', backref='application', lazy=True)
    owned_card = db.relationship('OwnedCard', cascade='all, delete', backref='application', lazy=True)

@app.route('/')
def index():
    # return render_template('index.html')
    return redirect(url_for('show_pending', _external=True))

@app.route('/apply', methods=['GET', 'POST'])
def show_apply():
    if request.method == 'POST':
        req = request.form

        card_association = req['card_association']
        card_type = req['card_type']

        full_name = req['full_name']
        education = req['education']
        birthdate = req['birthdate']
        birthplace = req['birthplace']
        sex = req['sex']
        phone_number = req['phone_number']
        email_address = req['email_address']
        present_address = req['present_address']

        employment_type = req['employment_type']
        job_title = req['job_title']
        tenure = req['tenure']
        gross_annual_income = req['gross_annual_income']

        card_number = req['card_number']
        member_since = req['member_since']
        credit_limit = req['credit_limit']


        # INSERT INTO application ...
        card_option = CardOption.query.filter_by(card_association=card_association, card_type=card_type).first()

        person_id = abs(hash(card_number) %(10 ** 8))

        application = Application(
            person_id=person_id,
            card_option_id=card_option.id,
            card_number=card_number
        )
        db.session.add(application)
        db.session.commit()

        # INSERT INTO person ...
        application = Application.query.filter_by(card_number=card_number).first()
        print(application)

        person = Person(
            id=application.person_id,
            full_name=full_name,
            education=education,
            birthdate=birthdate,
            birthplace=birthplace,
            sex=sex,
            phone_number=phone_number,
            email_address=email_address,
            present_address=present_address,
            employment_type=employment_type,
            job_title=job_title,
            tenure=tenure,
            gross_annual_income=gross_annual_income
        )
        db.session.add(person)

        # INSERT INTO owned_card ...
        owned_card = OwnedCard(
            card_number=card_number,
            member_since=member_since,
            credit_limit=credit_limit
        )
        db.session.add(owned_card)
        db.session.commit()

        return redirect(url_for('show_pending'))

    return render_template('apply.html')
    # return redirect(url_for('show_pending'), _external=True)

@app.route('/pending/', methods=['GET', 'POST'])
@app.route('/pending/<apply_id>', methods=['GET', 'POST'])
def show_pending(apply_id=None):
    if apply_id:
        print('apply_id: ',apply_id)
        data = db.session.query( Application.id, CardOption.card_association, CardOption.card_type, Person.full_name, Person.education, Person.birthdate, Person.birthplace, Person.sex, Person.phone_number, Person.email_address, Person.present_address, Person.employment_type, Person.job_title, Person.tenure, Person.gross_annual_income, OwnedCard.card_number, OwnedCard.member_since, OwnedCard.credit_limit)\
            .outerjoin(CardOption, Application.card_option_id == CardOption.id)\
            .outerjoin(Person, Application.person_id == Person.id)\
            .outerjoin(OwnedCard, Application.card_number == OwnedCard.card_number).filter(Application.id==apply_id).first()
        birthdate = datetime.strftime(data[5], '%Y-%m-%d')
        print(birthdate)
        return render_template('pending.html', apply_id=apply_id, data=data, birthdate=birthdate)
    else:
        data = db.session.query(Application.id, CardOption.card_association, CardOption.card_type, Person.full_name, Person.email_address, Person.employment_type, Person.gross_annual_income, OwnedCard.card_number, OwnedCard.member_since)\
            .outerjoin(CardOption, Application.card_option_id == CardOption.id)\
            .outerjoin(Person, Application.person_id == Person.id)\
            .outerjoin(OwnedCard, Application.card_number == OwnedCard.card_number).all()

        return render_template('pending.html', apply_id=apply_id, data=data)


@app.route("/delete", methods=["GET", "POST"])
def delete():
    id = request.form.get("id")
    application = Application.query.filter_by(id=id).first()
    db.session.delete(application)
    db.session.commit()
    return redirect(url_for('show_pending', _external=True))

@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        card_association = request.form['card_association']
        card_type = request.form['card_type']
        card_option = CardOption.query.filter_by(card_association=card_association, card_type=card_type).first()

        print('new_card_option_id: ', card_option.id)

        application_id = request.form['application_id']
        application = Application.query.filter_by(id=application_id).first()
        application.card_option_id = card_option.id

        person_id = application.person_id
        full_name = request.form['full_name']
        education = request.form['education']
        print('birthday: ', request.form['birthdate'])
        birthdate = datetime.strptime(str(request.form['birthdate']), '%Y-%m-%d')
        birthplace = request.form['birthplace']
        sex = request.form['sex']
        phone_number = request.form['phone_number']
        email_address = request.form['email_address']
        present_address = request.form['present_address']
        employment_type = request.form['employment_type']
        job_title = request.form['job_title']
        tenure = request.form['tenure']
        gross_annual_income = request.form['gross_annual_income']


        print('person_id: ', person_id)
        person = Person.query.filter_by(id=person_id).first()
        person.full_name = full_name
        person.education = education
        person.birthdate = birthdate
        person.birthplace = birthplace
        person.sex = sex
        person.phone_number = phone_number
        person.email_address = email_address
        person.present_address = present_address
        person.employment_type = employment_type
        person.employment_type = employment_type
        person.job_title = job_title
        person.tenure = tenure
        person.gross_annual_income = gross_annual_income

        db.session.commit()


    return redirect(url_for('show_pending', _external=True))

# @app.rouute()
if __name__ == '__main__':
    app.run()
