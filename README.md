# CS165 Simple Database App
###  Credit Card Application Manager

[Link to web app (deployed in AWS EC2 instance)](http://ec2-34-229-179-255.compute-1.amazonaws.com:8080/pending/)

This is a simple web application that is able to process credit card applications. This serves as a simple counterpart to the usual paper application form.

  - Create: Apply for a new credit card
  - Read: Provides a dashboard for pending applications
  - Update: Able to update personal information and card option
  - Delete: Able to delete pending applications

### Tech
* Flask
* HTML
* MySQL

### Installation

Requires the following to run (list):

- Python 3.x    
- MySQL 5.7
- Flask 1.1.1
- wheel 0.33.6
- SQLAlchemy 1.3.11
- Flask-SQLAlchemy 2.4.1
- gunicorn 20.0.4
- psycopg2 2.8.4
- mysqlclient 1.4.6

### Running Web Application in Development
Activate virtual environment
```
$ source venv/bin/activate
```
Install the dependencies

```sh
$ pip install -r requirements.txt
```
Install MySQL (Based on DigitalOcean Community Guide: https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-18-04)

```
$ sudo apt-get update
$ sudo apt-get install mysql-server
$ sudo mysql_secure_installation
```
Log-in to MYSQL server using root, create user, and grant privileges
```
mysql> CREATE USER 'cs165project'@'localhost' IDENTIFIED BY 'cs165project';
mysql> GRANT ALL PRIVILEGES ON *.* TO 'cs165project'@'localhost' WITH GRANT OPTION;
```
Using 'cs165project' user, initialize database
```
mysql> create database dilangalen;
```
Use Python CLI to initialize the database and create tables (make sure to be in the project directory):
```
>>> from app import db
>>> db.create_all()
>>> db.session.commit()
>>> exit()
```
Log back in to MySQL server using 'cs165project' user and populate the tables
```
mysql> use dilangalen
mysql> source ~/<project-directory>/phase4_dump.sql
```

Run Flask-managed server locally:
```sh
$ export FLASK_APP=app.py FLASK_DEBUG=True FLASK_ENV=development
$ flask run
```

### SQL ORM Mapping

##### Create
SQL Statement:
```
INSERT INTO person VALUES (id, full_name, education, birthdate,
birthplace, sex, phone_number, email_address, present_address,
employment_type, job_title, tenure, gross_annual_income)
```
ORM Equivalent:
```
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
db.session.commit()
```
##### Read
SQL Statement:
```
SELECT application.id AS application_id, card_option.card_association AS card_option_card_association, card_option.card_type AS card_option_card_type, person.full_name AS person_full_name, person.email_address AS person_email_address, person.employment_type AS person_employment_type, person.gross_annual_income AS person_gross_annual_income, owned_card.card_number AS owned_card_card_number, owned_card.member_since AS owned_card_member_since
FROM application
    LEFT OUTER JOIN card_option ON application.card_option_id = card_option.id
    LEFT OUTER JOIN person ON application.person_id = person.id
    LEFT OUTER JOIN owned_card ON application.card_number = owned_card.card_number;
```
ORM Equivalent:
```
data = db.session.query(Application.id, CardOption.card_association, CardOption.card_type, Person.full_name, Person.email_address, Person.employment_type, Person.gross_annual_income, OwnedCard.card_number, OwnedCard.member_since)\
            .outerjoin(CardOption, Application.card_option_id == CardOption.id)\
            .outerjoin(Person, Application.person_id == Person.id)\
            .outerjoin(OwnedCard, Application.card_number == OwnedCard.card_number).all()
```
##### Update
SQL Statement:
```
UPDATE person SET full_name=<full_name>, education=<education>, birthdate=<birthdate>, ... , gross_annual_income=<gross_annual_income>
WHERE id=<person_id>
```
ORM Equivalent:
```
person = Person.query.filter_by(id=person_id).first()
person.full_name = full_name
person.education = education
person.birthdate = birthdate
db.session.commit()
...
person.gross_annual_income = gross_annual_income
```
##### Delete
SQL Statement:
```
DELETE FROM application WHERE id=<application_id>;
```
ORM Equivalent:
```
application = Application.query.filter_by(id=id).first()
db.session.delete(application)
db.session.commit()
```
