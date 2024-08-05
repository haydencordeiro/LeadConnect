# -- encoding: utf-8 --

"""
export FLASK_APP=run.py
export FLASK_ENV=development
flask run


SET FLASK_APP=run.py
SET FLASK_ENV=development
flask run
"""
import os
from datetime import datetime, timezone, timedelta
from flask import jsonify
import openai
from functools import wraps

from flask import request, url_for, send_from_directory, send_file
from werkzeug.utils import secure_filename
from flask_restx import Api, Resource, fields

import pandas as pd
import jwt

from .models import db, Users, JWTTokenBlocklist, Contact, Experience, Connection
from .config import BaseConfig
import requests
import uuid
import random
# import json
from .smtp import send_email_to_admin, send_confirmation_link_to_user, send_simple_message
import traceback
# from .mock import youth_data, split_youth_name
from io import BytesIO

rest_api = Api(version="1.0", title="Users API")

# Replace with your OpenAI API key
openai.api_key = 'sk-None-h4hng2Tx16EatrANslK1T3BlbkFJnGCapd20f85McD4gsfwk'
"""
    Flask-Restx models for api request and response data
"""
"""
signup_model = rest_api.model('SignUpModel', {"email_address": fields.String(required=True, min_length=4, max_length=64),
                                              "password": fields.String(required=True, min_length=4, max_length=16),
                                              "first_name": fields.String(required=True, min_length=2, max_length=32),
                                              "last_name": fields.String(required=True, min_length=2, max_length=32),
                                              "license_number": fields.String(required=False, min_length=1, max_length=50),
                                              "date_of_birth": fields.Date(required=True),
                                              "last_four_ssn": fields.String(required=True, min_length=4, max_length=4),
                                              "security_question": fields.String(required=True, min_length=2, max_length=255),
                                              "security_question_answer": fields.String(required=True, min_length=2, max_length=255),
                                              "user_type": fields.String(required=True, min_length=1, max_length=1)
                                              })
"""
signup_model = rest_api.model('SignupModel', {
    'username': fields.String(required=True, description='User login name'),
    'password': fields.String(required=True, description='User password'),
    'email': fields.String(required=True, description='User email address'),
    'first_name': fields.String(required=True, description='User first name'),
    'last_name': fields.String(required=True, description='User last name'),
    'phone_number': fields.String(description='User contact number'),
    'company': fields.String(description='User company name'),
    'number_of_employees': fields.String(description='Number of employees in the company',
                                         enum=['1-10', '11-50', '51-200', '201-500', '501-1000', '1001-5000',
                                               '5001-10000', '10001+']),
    'province': fields.String(required=True, description='User province in Canada',
                              enum=['Alberta', 'British Columbia', 'Manitoba', 'New Brunswick',
                                    'Newfoundland and Labrador', 'Nova Scotia', 'Ontario', 'Prince Edward Island',
                                    'Quebec', 'Saskatchewan']),
    'profile_picture_url': fields.String(description='URL to the user’s profile picture'),
    'security_question': fields.String(required=True, description='Security question for password recovery',
                                       enum=['What is your mother’s maiden name?',
                                             'What was the name of your first pet?',
                                             'What was the make of your first car?', 'What is your favorite color?',
                                             'What city were you born in?']),
    'security_answer': fields.String(required=True, description='Answer to the security question'),
    'my_resume_content': fields.String(description='User resume content')
})
login_model = rest_api.model('LoginModel', {"username": fields.String(required=True),
                                            "password": fields.String(required=True)
                                            })

llm_model = rest_api.model('LLMModel', {
    'experiences': fields.List(fields.String, required=True, description='List of experiences'),
    'initial_context': fields.Boolean(required=True,
                                      description='Flag to indicate if this is the initial context setting')
})

user_edit_model = rest_api.model('UserEditModel', {"user_id": fields.String(required=True, min_length=1, max_length=50),
                                                   "first_name": fields.String(required=True, min_length=2,
                                                                               max_length=32),
                                                   "last_name": fields.String(required=True, min_length=2,
                                                                              max_length=32),
                                                   "email_address": fields.String(required=True, min_length=4,
                                                                                  max_length=64)
                                                   })

contact_model = rest_api.model('Contact', {
    'contact_url': fields.String(required=True, description='Contact URL'),
    'name': fields.String(required=True, description='Name'),
    'current_location': fields.String(required=True, description='Current Location'),
    'headline': fields.String(required=True, description='Headline'),
    'about': fields.String(required=True, description='About'),
    'profile_pic_url': fields.String(required=True, description='Profile Picture URL')
})

experience_model = rest_api.model('Experience', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of the experience'),
    'contact_url': fields.String(required=True, description='Contact URL'),
    'company_name': fields.String(required=True, description='Company Name'),
    'company_logo': fields.String(required=True, description='Company Logo'),
    'company_role': fields.String(required=True, description='Company Role'),
    'company_location': fields.String(required=True, description='Company Location'),
    'bulletpoints': fields.String(required=True, description='Bullet Points'),
    'company_duration': fields.String(required=True, description='Company Duration'),
    'company_total_duration': fields.String(required=True, description='Company Total Duration')
})

"""
   Helper function for JWT token required
"""


import jwt
from functools import wraps
from flask import request, jsonify
from .models import Users, JWTTokenBlocklist
from .config import BaseConfig

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        """
        Check the validity of the token and make sure the token exisis in the database.

        Returns:
            JSON response with the token validity status and user ID if the token is valid.
        """
        token = None

        if "authorization" in request.headers:
            token = request.headers["authorization"]

        if not token:
            return {"success": False, "msg": "Valid JWT token is missing"}, 400

        try:
            data = jwt.decode(token, BaseConfig.SECRET_KEY, algorithms=["HS256"])
            current_user = Users.get_by_username(data["username"])
            if not current_user:
                return {"success": False, "msg": "User does not exist"}, 400

            kwargs['current_user'] = current_user

            token_expired = db.session.query(JWTTokenBlocklist.id).filter_by(jwt_token=token).scalar()

            if token_expired is not None:
                return {"success": False, "msg": "Token revoked."}, 400
            exp_time = datetime.fromtimestamp(data['exp'], tz=timezone.utc)
            if datetime.now(tz=timezone.utc) > exp_time:
                return {"success": False, "msg": "Token expired."}, 400

        except jwt.ExpiredSignatureError:
            return {"success": False, "msg": "Token expired. Please log in again."}, 401
        except jwt.InvalidTokenError:
            return {"success": False, "msg": "Invalid token. Please log in again."}, 401
        except Exception as e:
            print(traceback.format_exc())
            return {"success": False, "msg": "Token is invalid"}, 400

        return f(*args, **kwargs)

    return decorator


@rest_api.route('/api/auth/check')
class TokenCheck(Resource):
    @token_required
    def get(self, current_user):
        # If this point is reached, the token is valid
        return {"success": True, "msg": "Token is valid", "user_id": current_user.id}, 200


@rest_api.route('/api/users/register')
class Register(Resource):
    @rest_api.expect(signup_model, validate=True)
    def post(self):
        """
        Register a new user.

        Request Data:
            - username: User's username.
            - password: User's password.
            - email: User's email address.
            - first_name: User's first name.
            - last_name: User's last name.
            - phone_number: User's phone number.
            - company: User's company.
            - number_of_employees: Number of employees in the company.
            - province: User's province.
            - profile_picture_url: URL to the user's profile picture.
            - security_question: Security question for password recovery.
            - security_answer: Answer to the security question.

        Returns:
            JSON response with the status and user ID if the registration is successful.
        """
        req_data = request.get_json()
        username = req_data.get("username")
        password = req_data.get("password")
        email = req_data.get("email")
        first_name = req_data.get("first_name")
        last_name = req_data.get("last_name")
        phone_number = req_data.get("phone_number")
        company = req_data.get("company")
        number_of_employees = req_data.get("number_of_employees")
        province = req_data.get("province")
        profile_picture_url = req_data.get("profile_picture_url")
        security_question = req_data.get("security_question")
        security_answer = req_data.get("security_answer")
        user_exists = Users.get_by_email(email)
        my_resume_content = req_data.get("my_resume_content")  # New field
        if user_exists:
            return {"success": False, "msg": "User already exists"}, 400

        new_user = Users(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            company=company,
            number_of_employees=number_of_employees,
            province=province,
            profile_picture_url=profile_picture_url,
            security_question=security_question,
            security_answer=security_answer,
            status=1,  # Assuming 1 means 'active'
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            my_resume_content=my_resume_content,  # Assigning new field
        )
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        new_user.save()

        return {"status": "success", "userID": new_user.user_id, "msg": "The user was successfully registered"}, 201

@rest_api.route('/api/user/forgot-password')
class ForgotPassword(Resource):

    def post(self):
        """
        Handle forgot password request.

        Request Data:
            - email: User's email address.

        Returns:
            JSON response with the security question if the user exists.
        """
        req_data = request.get_json()
        _email_address = req_data.get("email")
        user_exists = Users.get_by_email(_email_address)

        if user_exists:
            # Assuming your Users model has a security_question field
            return {"status": "success", "security_question": user_exists.security_question}
        else:
            return {"status": "failed", "msg": "User does not exist."}, 404


@rest_api.route('/api/user/reset-password')
class ResetPassword(Resource):

    @rest_api.expect(login_model, validate=True)
    def post(self):
        """
        Handle password reset request.

        Request Data:
            - email: User's email address.
            - security_question: User's security question.
            - security_answer: Answer to the security question.
            - password: New password.

        Returns:
            JSON response indicating the success or failure of the password reset.
        """
        try:
            req_data = request.get_json()
            _email_address = req_data.get("email")
            _security_question = req_data.get("security_question")
            _security_question_answer = req_data.get("security_answer")
            _password = req_data.get("password")

            user_exists = Users.get_by_email_address(_email_address)

            if user_exists:
                # Validate security question and answer
                if user_exists.security_question == _security_question and user_exists.security_question_answer == _security_question_answer:
                    user_exists.is_authenticated = 0
                    _pin = ''.join([str(random.randint(0, 9)) for _ in range(4)])
                    user_exists.set_password(_password)

                    user_exists.pin = _pin
                    db.session.commit()

                    _verification_link = BaseConfig.VERIFICATION_LINK.format(user_id=user_exists.user_id)

                    send_email_to_admin(_email_address, user_exists.first_name, user_exists.last_name, _pin)
                    send_confirmation_link_to_user(_email_address, user_exists.first_name, user_exists.last_name,
                                                   _verification_link)
                    return {"status": "success",
                            "msg": "Password reset success. Please get the PIN from the admin to verify the authentication."}, 200
                else:
                    return {"status": "failed", "msg": "Invalid security question or answer."}, 401
            else:
                return {"status": "failed", "msg": "User does not exist."}, 404
        except Exception as e:
            # Handle database errors
            print(traceback.format_exc())
            return {"status": "failed", "msg": "Error occurred, Please contact the admin."}, 500


@rest_api.route('/api/users/verify')
class Verify(Resource):
    @rest_api.expect(login_model, validate=True)
    def post(self):
        """
        Verify user credentials and return JWT token.

        Request Data:
            - email: User's email address.
            - password: User's password.
            - pin: User's PIN.

        Returns:
            JSON response with the JWT token and user details if verification is successful.
        """
        req_data = request.get_json()

        _email_address = req_data.get("email")
        _password = req_data.get("password")
        _pin = req_data.get("pin")
        user_exists = Users.get_by_email(_email_address)

        if not user_exists:
            return {"success": False, "msg": "This email does not exist."}, 400

        if not user_exists.check_password(_password):
            return {"success": False,
                    "msg": "Wrong credentials."}, 400

        if user_exists.is_authenticated == 0:
            if str(user_exists.pin) != str(_pin):
                return {"success": False,
                        "msg": "You have entered an invalid PIN. Please check with the admin for a valid PIN."}, 401
            else:
                # Update the is_authenticated to 1 in the db
                user_exists.is_authenticated = 1
                db.session.commit()  # Make sure to commit the changes to the database

                # create access token using JWT
                token = jwt.encode({'email': _email_address, 'exp': datetime.utcnow() + timedelta(days=60)},
                                   BaseConfig.SECRET_KEY)
                user_exists.set_status(True)
                user_exists.save()

                return {"success": True, "token": token, "user": user_exists.toJSON()}, 200
        else:
            return {"success": False, "msg": "You are already authenticated."}, 401


""""""


@rest_api.route('/api/users/login')
class Login(Resource):
    @rest_api.expect(login_model, validate=True)
    def post(self):
        """
        Login user and return JWT token.

        Request Data:
            - username: User's username.
            - password: User's password.

        Returns:
            JSON response with the JWT token and user details if login is successful.
        """
        req_data = request.get_json()

        username = req_data.get("username")
        password = req_data.get("password")
        user_exists = Users.get_by_username(username)
        if not user_exists:
            return {"success": False,
                    "msg": "This email does not exist."}, 400

        # Add this check for is_authenticated
        #    if user_exists.is_authenticated == 0:
        #        return {"success": False, "msg": "You are not authenticated. Please verify your email by using the verification link sent to your email."}, 401

        user_id = user_exists.user_id
        if not user_exists.check_password(password):
            return {"success": False,
                    "msg": "Wrong credentials."}, 400

        # create access token uwing JWT
        token = jwt.encode({'user_id': user_id, 'username': username, 'exp': datetime.utcnow() + timedelta(minutes=30)},
                           BaseConfig.SECRET_KEY)
        user_exists.set_status(True)
        user_exists.save()

        return {"success": True,
                "token": token,
                "user": user_exists.toJSON()}, 200

@rest_api.route('/api/llm_generic')
class LLM(Resource):
    def post(self):
        """
        Generate a customized message using OpenAI's GPT-4o-mini based on user input.

        Request Data:
            - users: List of users.
            - question: Question or prompt for the model.
            - job_description: Job description.
            - initial_context: Boolean flag to indicate if this is the initial context setting.

        Returns:
            JSON response with the generated message.
        """
        data = request.get_json()
        users = data.get('users')
        question = data.get('question')
        job_description = data.get('job_description')
        initial_context = data.get('initial_context')
        if initial_context:
            if "company" in question:
                messages = [
                    {"role": "system", "content": "from the below users who are currently working in the company."},
                    {"role": "user", "content": f"job description: {job_description}"},
                    {"role": "user", "content": f"users: {''.join(users)}"}
                ]

                response = openai.ChatCompletion.create(
                    model="gpt-4o-mini",
                    messages=messages,
                    max_tokens=1500
                )
                summary_message = response['choices'][0]['message']['content'].strip()
                return {'customized_message': summary_message}
            if "cover" or "letter" in question:
                url = "http://143.110.152.18:5000/generate-cover-letter"
                data = {
                    "job_description": job_description
                }
                headers = {
                    "Content-Type": "application/json"
                }
                response = requests.post(url, json=data, headers=headers)

                # Checking the status code and printing the result
                if response.status_code == 200:
                    print("Success! Here is the link to the generated cover letter:")
                    print(response.json().get("url"))
                    print(response.json())
                    return {'customized_message': f""" Generated Cover Letter for the given job description. <a href='{response.json().get("url")}'>Click to download.</a>"""}
                else:
                    print(f"Failed to generate cover letter. Status code: {response.status_code}")
                    print(response.json())
                    return {'customized_message': "Error occurred, Please contact the admin."}, 500

            return {'customized_message': """ <div class="container">
<h1>Hello,</h1>
<p>I have saved your job description. You can ask questions like:</p>

<ul style="list-style-type: disc; padding-left: 20px;">
<li>Who from my contacts is currently working in this company?</li>
<li>How can my contacts help me get more inputs about this job?</li>
<li>Generate a cover letter.</li>
<li>Generate a tailored resume.</li>
</p>
</ul>
</div>"""}
        return {'customized_message': ""}

@rest_api.route('/api/llm')
class LLM(Resource):
    @rest_api.expect(llm_model, validate=True)
    def post(self):
        """
        Generate a customized message using OpenAI's GPT-3.5 based on user input.

        Request Data:
            - experiences: List of user experiences.
            - question: Question or prompt for the model.
            - initial_context: Boolean flag to indicate if this is the initial context setting.

        Returns:
            JSON response with the generated message.
        """
        data = request.get_json()

        experiences = data.get('experiences')
        question = data.get('question')
        initial_context = data.get('initial_context')

        if not experiences:
            return {'customized_message': "Error occurred, Please contact the admin."}

        if initial_context:
            summary = " ".join(experiences)
            messages = [
                {"role": "system", "content": "You are my lead management and email message generator bot."},
                {"role": "user", "content": f"Summary of the person: {summary}"},
                {"role": "user",
                 "content": "Generate a summary of that person and later I will ask you to create a customized message to be in touch with that person. Always reply with HTML code, since i want to add it to my website."}
            ]

            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4o-mini",
                    messages=messages,
                    max_tokens=1500
                )
                summary_message = response['choices'][0]['message']['content'].strip()
                return jsonify({'customized_message': summary_message})

            except Exception as e:
                return {'customized_message': "Error occurred, Please contact the admin."}

        else:
            # Use the stored summary to generate a customized message
            try:
                summary = " ".join(experiences)

                messages = [
                    {"role": "system", "content": "You are my lead management and email message generator bot."},
                    {"role": "user", "content": f"Summary of the person: {summary}"},
                    {"role": "user", "content": f"Always reply with HTML code, since i want to add it to my website."},
                    {"role": "user", "content": question}
                ]

                response = openai.ChatCompletion.create(
                    model="gpt-4o-mini",
                    messages=messages,
                    max_tokens=1500
                )
                customized_message = response['choices'][0]['message']['content'].strip()

                return {'customized_message': customized_message}

            except Exception as e:
                return {'customized_message': "Error occurred, Please contact the admin."}


@rest_api.route('/api/users')
class UserList(Resource):
    """
    List all user names.

    Returns:
        JSON response with the list of user names.
    """
    def get(self):
        users = Users.query.all()
        user_names = [user.name for user in users]
        return {"success": True, "user_names": user_names}, 200


# Function to convert date to "mm/dd/yyyy" format
def format_date(dt):
    if pd.isnull(dt):
        return None  # Return None if the date is NaT
    return dt.strftime("%m/%d/%Y")  # Format datetime to "mm/dd/yyyy"


# Convert date strings to the 'YYYY-MM-DD' format
def convert_date(date_str):
    """
    Convert date strings to the 'YYYY-MM-DD' format.

    Args:
        date_str (str): Date string in 'mm/dd/yyyy' format.

    Returns:
        str: Date string in 'YYYY-MM-DD' format.
    """
    return datetime.strptime(date_str, '%m/%d/%Y').strftime('%Y-%m-%d')


@rest_api.route('/api/users/contacts')
class get_user_contacts(Resource):
    @token_required
    def get(self, current_user):
        """
        Get contacts of the current user.

        Returns:
            JSON response with the list of contacts and their experiences.
        """
        user_id = current_user.user_id

        connections = db.session.query(Connection).filter(Connection.user_id == user_id).all()
        contact_urls = [connection.contact_url for connection in connections]
        user_contacts = db.session.query(Contact).filter(Contact.contact_url.in_(contact_urls)).all()
        contacts = []
        for contact in user_contacts:

            experiences = Experience.query.filter_by(contact_url=contact.contact_url).all()
            experience_data = []
            for exp in experiences:
                experience_data.append({
                    'company_name': exp.company_name,
                    'company_logo': exp.company_logo,
                    'company_role': exp.company_role,
                    'company_location': exp.company_location,
                    'bulletpoints': exp.bulletpoints,
                    'company_duration': exp.company_duration,
                    'company_total_duration': exp.company_total_duration
                })

            contact_data = {
                'contact_url': contact.contact_url,
                'name': contact.name,
                'current_location': contact.current_location,
                'headline': contact.headline,
                'about': contact.about,
                'profile_pic_url': contact.profile_pic_url,
                'experiences': experience_data
            }

            connection = next((conn for conn in connections if conn.contact_url == contact.contact_url), None)
            if connection:
                contact_data['frequency'] = connection.frequency
                contact_data['last_interacted'] = connection.last_interacted
                contact_data['notes'] = connection.notes  # Add notes to the contact data

            contacts.append(contact_data)
        return jsonify({'contacts': contacts})

@rest_api.route('/api/sef/pdf_upload')
class upload_file(Resource):
    def post(self, **kwargs):
        """
        Upload a PDF file.

        Returns:
            JSON response with the file URL if the upload is successful.
        """
        try:
            if 'file' not in request.files:
                return {'success': False, 'message': 'No file part in the request'}, 400

            file = request.files['file']
            if file.filename == '':
                return {'success': False, 'message': 'No selected file'}, 400

            if file and '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in ['pdf']:
                filename = secure_filename(file.filename)
                basedir = os.path.abspath(os.path.dirname(_file_))
                upload_path = os.path.join(basedir, rest_api.app.config['UPLOAD_FOLDER'])
                file.save(os.path.join(upload_path, filename))  # Directly use 'upload_path' here
                file_url = url_for('static', filename=os.path.join('pdfs', filename), _external=True)
                return {'success': True, 'file_url': file_url}, 200
            else:
                return {'success': False, 'message': 'Invalid file type'}, 400
        except Exception as e:
            print(traceback.format_exc())
            return {"message": "Some error occurred: {}".format(str(e))}, 500


@rest_api.route('/api/sef/pdf/<filename>', methods=['GET'])
class upload_file(Resource):
    def get(self, filename):
        """
        Download a PDF file.

        Returns:
            The requested PDF file if it exists.
        """
        try:
            filename = filename + ".pdf"
            # Ensure the file exists
            basedir = os.path.abspath(os.path.dirname(_file_))
            upload_path = os.path.join(basedir, rest_api.app.config['UPLOAD_FOLDER'])
            if not os.path.exists(os.path.join(upload_path, filename)):
                return {'success': False, 'message': 'File does not exist'}, 404

            # Check if the file is a PDF
            if '.' in filename and filename.rsplit('.', 1)[1].lower() == 'pdf':
                # Directly pass 'upload_path' and 'filename' to 'send_from_directory'
                return send_from_directory(upload_path, filename, as_attachment=False)
            else:
                return {'success': False, 'message': 'Invalid file type'}, 400
        except Exception as e:
            print(traceback.format_exc())
            print(f"An error occurred: {str(e)}")
            return {"success": False, "message": "An error occurred"}, 500


@rest_api.route('/api/users/profile')
class UserProfileAPI(Resource):
    @token_required
    def get(self, current_user):
        """
        Get the profile details of the current user.

        Returns:
            JSON response with the user's profile details.
        """
        user_id = current_user.user_id
        user = Users.query.filter_by(user_id=user_id).first()
        if user:
            return jsonify({
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "phone_number": user.phone_number,
                "company": user.company,
                "number_of_employees": user.number_of_employees,
                "province": user.province,
                "profile_picture_url": user.profile_picture_url,
                "security_question": user.security_question,
                "security_answer": user.security_answer,
                "my_resume_content": user.my_resume_content,  # Added this field
                "subscription": user.subscription,
            })
        else:
            return jsonify({"error": "User not found"}), 404

    @token_required
    def put(self, current_user):
        """
        Update the profile details of the current user.

        Request Data:
            - email: User's email address.
            - first_name: User's first name.
            - last_name: User's last name.
            - phone_number: User's phone number.
            - company: User's company.
            - number_of_employees: Number of employees in the company.
            - province: User's province.
            - profile_picture_url: URL to the user's profile picture.
            - security_question: Security question for password recovery.
            - security_answer: Answer to the security question.
            - password: User's new password (if changing).

        Returns:
            JSON response indicating the success or failure of the profile update.
        """
        data = request.json
        user = current_user
        if user:
            user.email = data.get('email', user.email)
            user.first_name = data.get('first_name', user.first_name)
            user.last_name = data.get('last_name', user.last_name)
            user.phone_number = data.get('phone_number', user.phone_number)
            user.company = data.get('company', user.company)
            user.number_of_employees = data.get('number_of_employees', user.number_of_employees)
            user.province = data.get('province', user.province)
            user.profile_picture_url = data.get('profile_picture_url', user.profile_picture_url)
            user.security_question = data.get('security_question', user.security_question)
            user.security_answer = data.get('security_answer', user.security_answer)
            user.my_resume_content = data.get('my_resume_content', user.my_resume_content)  # Added this field
            user.set_password(data.get('password', user.password_hash))  # Assuming password change is allowed
            user.subscription = data.get('subscription', user.subscription)
            db.session.commit()
            return jsonify({"message": "Profile updated successfully"})
        else:
            return jsonify({"error": "User not found"}), 404


@rest_api.route('/api/users/logout')
class LogoutUser(Resource):
    @token_required
    def post(self, current_user):
        """
        Logout the current user.

        Returns:
            JSON response indicating the success or failure of the logout.
        """
        user_id = current_user.user_id
        user = Users.query.filter_by(user_id=user_id).first()

        if user and user.status == 1:
            user.status = 0
            db.session.commit()

            return {"success": True, "message": "User logged out successfully"}, 200
        else:
            return {"success": False, "message": "User is already logged out or does not exist"}, 400


@rest_api.route('/api/sessions/oauth/github/')
class GitHubLogin(Resource):
    def get(self):
        code = request.args.get('code')
        client_id = BaseConfig.GITHUB_CLIENT_ID
        client_secret = BaseConfig.GITHUB_CLIENT_SECRET
        root_url = 'https://github.com/login/oauth/access_token'

        params = {'client_id': client_id, 'client_secret': client_secret, 'code': code}

        data = requests.post(root_url, params=params, headers={
            'Content-Type': 'application/x-www-form-urlencoded',
        })

        response = data._content.decode('utf-8')
        access_token = response.split('&')[0].split('=')[1]

        user_data = requests.get('https://api.github.com/user', headers={
            "Authorization": "Bearer " + access_token
        }).json()

        user_exists = Users.get_by_first_name(user_data['login'])
        if user_exists:
            user = user_exists
        else:
            try:
                user = Users(username=user_data['login'], email=user_data['email'])
                user.save()
            except:
                user = Users(username=user_data['login'])
                user.save()

        user_json = user.toJSON()

        token = jwt.encode({"username": user_json['username'], 'exp': datetime.utcnow() + timedelta(minutes=30)},
                           BaseConfig.SECRET_KEY)
        user.set_status(True)
        user.save()

        return {"success": True,
                "user": {
                    "_id": user_json['_id'],
                    "email": user_json['email'],
                    "username": user_json['username'],
                    "token": token,
                }}, 200


# route to add using a user id to all tables experiences.
@rest_api.route('/api/createcontact')
class ExtensionResource(Resource):
    @token_required
    def post(self, current_user):
        current_user_id = current_user.user_id
        data = request.get_json()
        # Handle contact if existing
        existing_contact = Contact.get_by_contact_url(data['linkedinURL'])
        if (existing_contact):
            # Contact Exist
            existing_contact.update_name(data['name'])
            existing_contact.update_headline(data['headline'])
            existing_contact.update_current_location(data['location'])
            existing_contact.update_profile_pic_url(data['profilePicture'])
            existing_contact.update_about(data['summary'])

            new_contact = existing_contact
        else:
            # Contact doesnt exist in the databse
            """Create a new contact"""
            new_contact = Contact(
                contact_url=data['linkedinURL'],
                name=data['name'],
                headline=data['headline'],
                current_location=data['location'],
                profile_pic_url=data['profilePicture'],
                about=data['summary'],
            )
            new_contact.save()

        # Connection doesnt exist in the database
        # update connection table

        new_connection = Connection.get_by_connection(current_user_id, data['linkedinURL'])
        if (not new_connection):
            new_connection = Connection(
                user_id=current_user_id,
                contact_url=data['linkedinURL']
            )
            new_connection.save()

        # Clear exisitng experiences if any
        current_experiences = Experience.get_by_contact_url(data['linkedinURL'])
        for current_experience in current_experiences:
            current_experience.delete()

        # Process the experience list
        experiences = data.get('experience', [])
        # Create experience table
        experience_object = []
        for company in experiences:
            for position in company['companyPositions']:
                experience = Experience(
                    contact_url=new_connection.contact_url,
                    company_name=company.get("CompanyName") or company.get("companyName"),
                    company_logo=company.get("CompanyLogo"),
                    company_role=position.get("CompanyRole") or position.get("companyRole"),
                    company_location=position["companyLocation"],
                    bulletpoints=position["bulletPoints"],
                    company_duration=position["companyDuration"],
                    company_total_duration=position["companyTotalDuration"]
                )
                experience.save()
                experience_object.append(experience.toDICT())
        return [new_connection.toDICT(), new_contact.toDICT(), experience_object], 201

    @token_required
    def delete(self, current_user):
        data = request.get_json()
        print(data)
        user_connection = Connection.get_by_connection(current_user.user_id, data['linkedinURL'])
        user_connection.delete()
        return {"status": "deleted"}

@rest_api.route('/api/users/contacts/notes', methods=['POST'])
class UpdateUserNotes(Resource):
    @token_required
    def post(self, current_user):
        data = request.get_json()
        contact_url = data.get('contact_url')
        notes = data.get('notes')

        if not contact_url or not notes:
            return {'success': False, 'msg': 'Invalid input'}, 400

        connection = Connection.query.filter_by(user_id=current_user.user_id, contact_url=contact_url).first()

        if not connection:
            return {'success': False, 'msg': 'Connection not found'}, 404

        connection.notes = notes
        db.session.commit()

        return {'success': True, 'msg': 'Notes updated successfully'}
    
def get_next_interaction_date(interaction):
    last_interacted = interaction.last_interacted
    frequency = interaction.frequency

    if frequency == 'Weekly':
        return last_interacted + timedelta(weeks=1)
    elif frequency == 'Biweekly':
        return last_interacted + timedelta(weeks=2)
    elif frequency == 'Monthly':
        return last_interacted + timedelta(days=30)
    elif frequency == 'Bimonthly':
        return last_interacted + timedelta(days=60)
    elif frequency == 'Once in 3 months':
        return last_interacted + timedelta(days=90)
    elif frequency == 'Once in 6 months':
        return last_interacted + timedelta(days=180)

""""
@rest_api.route('/api/users/get_notifications')
class get_reminders(Resource):
    @token_required
    def get(self, current_user):
        user_id = current_user.user_id
        tommorrow = datetime.today().date() + + timedelta(days=1)
        reminders = []
        interactions = Connection.query.filter(Connection.user_id == user_id)
        for interaction in interactions:
            next_interaction_date = get_next_interaction_date(interaction)
            if tommorrow == next_interaction_date:
                contact = Contact.query.filter_by(contact_url=interaction.contact_url).first()
                if contact:
                    connection = next((conn for conn in interactions if conn.contact_url == contact.contact_url), None)
                    if connection:
                        reminders.append({
                            'name': contact.name,
                            'contact_url': interaction.contact_url,
                            'profile_pic_url': contact.profile_pic_url
                        })

        return jsonify(reminders)
"""


@rest_api.route('/api/users/notifications')
class GetReminders(Resource):
    def get(self):
        users = Users.query.all()  # Fetch all users
        tomorrow = datetime.today().date() + timedelta(days=1)
        all_reminders = {}

        for user in users:
            reminders = []
            interactions = Connection.query.filter(Connection.user_id == user.user_id).all()
            for interaction in interactions:
                next_interaction_date = get_next_interaction_date(interaction)
                if tomorrow == next_interaction_date:
                    contact = Contact.query.filter_by(contact_url=interaction.contact_url).first()
                    if contact:
                        reminders.append({
                            'name': contact.name,
                            'contact_url': interaction.contact_url,
                            'profile_pic_url': contact.profile_pic_url
                        })
            if reminders:
                all_reminders[user.email] = reminders
        
        for email, reminders in all_reminders.items():
            contact_list = "\n".join([f"{contact['name']} ({contact['profile_pic_url']})" for contact in reminders])
            email_subject = "Your Contacts to Reach Out Today"
            email_body = f"Hi,\n\nYou need to contact the following people tomorrow:\n\n{contact_list}\n\nBest regards,\nYour Team"
            send_simple_message(to=email, subject=email_subject, body=email_body, contacts=reminders)
        
        return jsonify(all_reminders)
        


