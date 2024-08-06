# -*- encoding: utf-8 -*-
from datetime import datetime,timezone
import json
import logging

from werkzeug.security import generate_password_hash, check_password_hash

from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import Column, Integer, String, Date, TIMESTAMP, func, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
logger = logging.getLogger(__name__)
db = SQLAlchemy()

"""
Users model representing a user in the system.

Attributes:
    user_id: Unique identifier for the user.
    username: Username of the user.
    password_hash: Hashed password for the user.
    email: Email address of the user.
    first_name: First name of the user.
    last_name: Last name of the user.
    phone_number: Phone number of the user.
    company: Company name associated with the user.
    number_of_employees: Enum representing the number of employees in the user's company.
    province: Enum representing the province the user resides in.
    profile_picture_url: URL to the user's profile picture.
    security_question: Enum representing the security question for the user.
    security_answer: Answer to the security question.
    status: Status of the user.
    created_at: Timestamp when the user was created.
    updated_at: Timestamp when the user was last updated.
    connections: One-to-many relationship with the Connection model.
"""
class Users(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(20))
    company = db.Column(db.String(255))
    number_of_employees = db.Column(db.Enum('1-10', '11-50', '51-200', '201-500', '501-1000', '1001-5000', '5001-10000', '10001+'))
    province = db.Column(db.Enum('Alberta', 'British Columbia', 'Manitoba', 'New Brunswick', 'Newfoundland and Labrador', 'Nova Scotia', 'Ontario', 'Prince Edward Island', 'Quebec', 'Saskatchewan'), nullable=False)
    profile_picture_url = db.Column(db.String(255))
    security_question = db.Column(db.Enum('What is your mother’s maiden name?', 'What was the name of your first pet?', 'What was the make of your first car?', 'What is your favorite color?', 'What city were you born in?'), nullable=False)
    security_answer = db.Column(db.String(255), nullable=False)
    status = db.Column(db.Integer, nullable=False)  # To indicate the status of the user
    created_at = db.Column(db.TIMESTAMP, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.TIMESTAMP, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    my_resume_content = db.Column(db.Text, nullable=True, default='')  # New field added
    # One-to-many relationship with Connection
    connections = db.relationship('Connection', backref='user', lazy=True, cascade='all, delete')
    subscription = db.Column(
        db.Enum('Free Tier', 'Business Tier', 'Enterprise Tier'),
        nullable=False,
    )

    def __repr__(self):
        return f"User {self.username}"  # Return the username of the user   

    def save(self):
        logger.debug('save method called')
        db.session.add(self)
        db.session.commit()
        logger.debug('save method completed')

    def set_password(self, password):
        logger.debug('set_password called with password: %s', password)
        self.password_hash = generate_password_hash(password)
        logger.debug('set_password completed')

    def check_password(self, password):
        logger.debug('check_password called with password: %s', password)
        result = check_password_hash(self.password_hash, password)
        logger.debug('check_password result: %s', result)
        return result

    def update_email(self, new_email):
        logger.debug('update_email called with new_email: %s', new_email)
        self.email = new_email
        logger.debug('update_email completed')

    def update_first_name(self, new_first_name):
        logger.debug('update_first_name called with new_first_name: %s', new_first_name)
        self.first_name = new_first_name
        logger.debug('update_first_name completed')

    def update_last_name(self, new_last_name):
        logger.debug('update_last_name called with new_last_name: %s', new_last_name)
        self.last_name = new_last_name
        logger.debug('update_last_name completed')

    def check_status(self):
        logger.debug('check_status called')
        result = self.status
        logger.debug('check_status result: %s', result)
        return result

    def set_status(self, set_status):
        logger.debug('set_status called with set_status: %s', set_status)
        self.status = set_status
        logger.debug('set_status completed')

    @classmethod
    def get_by_id(cls, id):
        logger.debug('get_by_id called with id: %s', id)
        result = db.session.query(cls).get_or_404(id)
        logger.debug('get_by_id result: %s', result)
        return result

    @classmethod
    def get_by_email(cls, email):
        logger.debug('get_by_email called with email: %s', email)
        result = db.session.query(cls).filter_by(email=email).first()
        logger.debug('get_by_email result: %s', result)
        return result
    
    @classmethod
    def get_by_username(cls, username):
        logger.debug('get_by_username called with username: %s', username)
        result = db.session.query(cls).filter_by(username=username).first()
        logger.debug('get_by_username result: %s', result)
        return result

    def toDICT(self):
        cls_dict = {}
        cls_dict['user_id'] = self.user_id
        cls_dict['username'] = self.username
        cls_dict['email'] = self.email
        cls_dict['first_name'] = self.first_name
        cls_dict['last_name'] = self.last_name
        cls_dict['phone_number'] = self.phone_number
        cls_dict['company'] = self.company
        cls_dict['number_of_employees'] = self.number_of_employees
        cls_dict['province'] = self.province
        cls_dict['profile_picture_url'] = self.profile_picture_url
        cls_dict['security_question'] = self.security_question
        cls_dict['security_answer'] = self.security_answer
        cls_dict['created_at'] = self.created_at.isoformat() if self.created_at else None,
        cls_dict['updated_at'] = self.updated_at.isoformat() if self.updated_at else None,
        cls_dict['status'] = self.status,
        cls_dict['my_resume_content'] = self.my_resume_content

        return cls_dict
        
    def toJSON(self):
        return self.toDICT()

"""
JWTTokenBlocklist model representing a blocklist of JWT tokens.

Attributes:
    id: Unique identifier for the blocklist entry.
    jwt_token: JWT token string.
    created_at: Timestamp when the token was created.
"""
class JWTTokenBlocklist(Base):
    __tablename__ = 'users_session'
    id = db.Column(db.Integer, primary_key=True)
    jwt_token = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.TIMESTAMP, nullable=False)


    def __repr__(self):
        logger.debug('__repr__ called')
        result = f"Expired Token: {self.jwt_token}"
        logger.debug('__repr__ result: %s', result)
        return result

    def save(self):
        logger.debug('save method called')
        db.session.add(self)
        db.session.commit()
        logger.debug('save method completed')

"""
Contact model representing a contact person in the system.

Attributes:
    contact_url: URL to the contact's profile.
    name: Name of the contact.
    current_location: Current location of the contact.
    headline: Headline or title of the contact.
    about: About information for the contact.
    profile_pic_url: URL to the contact's profile picture.
"""
class Contact(db.Model):
    __tablename__ = 'contacts'
    contact_url = db.Column(db.String(255), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    current_location = db.Column(db.String(255), nullable=False)
    headline = db.Column(db.String(255), nullable=False)
    about = db.Column(db.Text, nullable=False)
    profile_pic_url = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        logger.debug('__repr__ called')
        result = f"Contact {self.contact_url}"
        logger.debug('__repr__ result: %s', result)
        return result

    def save(self):
        logger.debug('save method called')
        db.session.add(self)
        db.session.commit()
        logger.debug('save method completed')

    def update_name(self, new_name):
        logger.debug('update_name called with new_name: %s', new_name)
        self.name = new_name
        self.save()
        logger.debug('update_name completed')

    def update_current_location(self, new_location):
        logger.debug('update_current_location called with new_location: %s', new_location)
        self.current_location = new_location
        self.save()
        logger.debug('update_current_location completed')

    def update_headline(self, new_headline):
        logger.debug('update_headline called with new_headline: %s', new_headline)
        self.headline = new_headline
        self.save()
        logger.debug('update_headline completed')

    def update_about(self, new_about):
        logger.debug('update_about called with new_about: %s', new_about)
        self.about = new_about
        self.save()
        logger.debug('update_about completed')

    def update_profile_pic_url(self, new_profile_pic_url):
        logger.debug('update_profile_pic_url called with new_profile_pic_url: %s', new_profile_pic_url)
        self.profile_pic_url = new_profile_pic_url
        self.save()
        logger.debug('update_profile_pic_url completed')

    @classmethod
    def get_by_contact_url(cls, contact_url):
        return db.session.query(cls).get(contact_url)

    @classmethod
    def get_all(cls):
        logger.debug('get_all called')
        result = cls.query.all()
        logger.debug('get_all result: %s', result)
        return result

    def delete(self):
        logger.debug('delete method called')
        db.session.delete(self)
        db.session.commit()
        logger.debug('delete method completed')

    def toDICT(self):
        cls_dict = {}
        cls_dict['contact_url'] = self.contact_url
        cls_dict['name'] = self.name
        cls_dict['current_location'] = self.current_location
        cls_dict['headline'] = self.headline
        cls_dict['about'] = self.about
        cls_dict['profile_pic_url'] = self.profile_pic_url
        return cls_dict

    def toJSON(self):
        logger.debug('toJSON called')
        result = self.toDICT()
        logger.debug('toJSON result: %s', result)
        return result
    
"""
Experience model representing a professional experience of a contact.

Attributes:
    id: Unique identifier for the experience.
    contact_url: URL to the associated contact's profile.
    company_name: Name of the company.
    company_logo: URL to the company's logo.
    company_role: Role of the contact at the company.
    company_location: Location of the company.
    bulletpoints: Bullet points describing the experience.
    company_duration: Duration of the contact's role at the company.
    company_total_duration: Total duration of the contact's experience.
"""
class Experience(db.Model):
    __tablename__ = 'experiences'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    contact_url = db.Column(db.String(255), db.ForeignKey('contacts.contact_url', ondelete='CASCADE'), nullable=False)
    company_name = db.Column(db.String(255), nullable=False)
    company_logo = db.Column(db.String(255), nullable=False)
    company_role = db.Column(db.String(255), nullable=False)
    company_location = db.Column(db.String(255), nullable=False)
    bulletpoints = db.Column(db.Text, nullable=False)
    company_duration = db.Column(db.String(255), nullable=False)
    company_total_duration = db.Column(db.String(255), nullable=False)
    
    # contact = db.relationship('Contact', backref=db.backref('contacts', lazy=True))

    def __repr__(self):
        logger.debug('__repr__ called')
        result = f"Experience {self.company_name} #at {self.contact_url}"
        logger.debug('__repr__ result: %s', result)
        return result

    def save(self):
        logger.debug('save method called')
        db.session.add(self)
        db.session.commit()
        logger.debug('save method completed')

    @classmethod
    def get_by_id(cls, id):
        logger.debug('get_by_id called with id: %s', id)
        result = db.session.query(cls).get_or_404(id)
        logger.debug('get_by_id result: %s', result)
        return result

    @classmethod
    def get_all(cls):
        logger.debug('get_all called')
        result = cls.query.all()
        logger.debug('get_all result: %s', result)
        return result

    def update_company_name(self, new_company_name):
        logger.debug('update_company_name called with new_company_name: %s', new_company_name)
        self.company_name = new_company_name
        self.save()
        logger.debug('update_company_name completed')

    def update_company_role(self, new_company_role):
        logger.debug('update_company_role called with new_company_role: %s', new_company_role)
        self.company_role = new_company_role
        self.save()
        logger.debug('update_company_role completed')

    def update_company_location(self, new_company_location):
        logger.debug('update_company_location called with new_company_location: %s', new_company_location)
        self.company_location = new_company_location
        self.save()
        logger.debug('update_company_location completed')

    def update_bulletpoints(self, new_bulletpoints):
        logger.debug('update_bulletpoints called with new_bulletpoints: %s', new_bulletpoints)
        self.bulletpoints = new_bulletpoints
        self.save()
        logger.debug('update_bulletpoints completed')

    def update_company_duration(self, new_company_duration):
        logger.debug('update_company_duration called with new_company_duration: %s', new_company_duration)
        self.company_duration = new_company_duration
        self.save()
        logger.debug('update_company_duration completed')

    def update_company_total_duration(self, new_company_total_duration):
        logger.debug('update_company_total_duration called with new_company_total_duration: %s', new_company_total_duration)
        self.company_total_duration = new_company_total_duration
        self.save()
        logger.debug('update_company_total_duration completed')

    def delete(self):
        logger.debug('delete method called')
        db.session.delete(self)
        db.session.commit()
        logger.debug('delete method completed')

    @classmethod
    def get_by_contact_url(cls, url):
        logger.debug('get_by_contact_url called with url: %s', url)
        result = db.session.query(cls).filter_by(contact_url=url)
        logger.debug('get_by_contact_url result: %s', result)
        return result
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def toDICT(self):
        cls_dict = {}
        cls_dict['id'] = self.id
        cls_dict['contact_url'] = self.contact_url
        cls_dict['company_name'] = self.company_name
        cls_dict['company_logo'] = self.company_logo
        cls_dict['company_role'] = self.company_role
        cls_dict['company_location'] = self.company_location
        cls_dict['bulletpoints'] = self.bulletpoints
        cls_dict['company_duration'] = self.company_duration
        cls_dict['company_total_duration'] = self.company_total_duration
        logger.debug('toDICT result: %s', cls_dict)
        return cls_dict

    def toJSON(self):
        logger.debug('toJSON called')
        result = self.toDICT()
        logger.debug('toJSON result: %s', result)
        return result

"""
Connection model representing a connection between a user and a contact.

Attributes:
    id: Unique identifier for the connection.
    user_id: ID of the associated user.
    contact_url: URL to the associated contact's profile.
    frequency: Enum representing the frequency of interaction.
    last_interacted: Date when the last interaction occurred.
    notes: Notes related to the connection.
"""

class Connection(db.Model):
    __tablename__ = 'connections'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    contact_url = db.Column(db.String(255), db.ForeignKey('contacts.contact_url', ondelete='CASCADE'), nullable=False)
    frequency = db.Column(db.Enum('Weekly', 'Biweekly', 'Monthly', 'Bimonthly', 'Once_in_3_months', 'Once_in_6_months'), default='Weekly', nullable=False)
    last_interacted = db.Column(db.Date, default=datetime.utcnow, nullable=False)
    notes = db.Column(db.Text, nullable=True)  # New field

    def __repr__(self):
        logger.debug('__repr__ called')
        result = f"Connection(User ID: {self.user_id}, Contact URL: {self.contact_url})"
        logger.debug('__repr__ result: %s', result)
        return result
   
    @classmethod
    def get_by_connection(cls, user_id, contact_url):
        return db.session.query(cls).filter_by(contact_url=contact_url, user_id=user_id).first()
    
    def save(self):
        logger.debug('save method called')
        db.session.add(self)
        db.session.commit()
        logger.debug('save method completed')
    
    def toDICT(self):
        cls_dict = {}
        cls_dict['id'] = self.id
        cls_dict['user_id'] = self.user_id
        cls_dict['contact_url'] = self.contact_url
        cls_dict['frequency'] = self.frequency
        cls_dict['last_interacted'] = self.last_interacted
        cls_dict['notes'] = self.notes  # Add notes to dict
        logger.debug('toDICT result: %s', cls_dict)
        return cls_dict

    def toJSON(self):
        logger.debug('toJSON called')
        result = self.toDICT()
        logger.debug('toJSON result: %s', result)
        return result

    def delete(self):
        logger.debug('delete method called')
        db.session.delete(self)
        db.session.commit()
        logger.debug('delete method completed')