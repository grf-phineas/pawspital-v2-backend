from app.auth import bp
from flask import jsonify, render_template, redirect, url_for, request, flash, session
from app.extensions import db
from app.models.auth import User, DoctorUser
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user


@bp.route("/members")
def members():
    return {"members": ["Member1", "Member2", "Member3"]}

@bp.route('/login')
def login():
    return render_template('index.html')

@bp.route('/login', methods=['POST'])
def login_post():
    data = request.get_json()
    email = data['email']
    password = data['password']
    remember = True if data['remember'] else False

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        print(user)
        print(check_password_hash(user.password, password))
        flash('Please check your login details and try again.')
        return jsonify({"isAuthenticated": False}), 401

    login_user(user, remember=remember)
    session['email'] = user.email
    return jsonify({"isAuthenticated": True}), 200

@bp.route('/doctor_login')
def doctor_login():
    return render_template('index.html')

@bp.route('/doctor_login', methods=['POST'])
def doctor_login_post():
    data = request.get_json()
    email = data['email']
    password = data['password']
    remember = True if data['remember'] else False

    user = DoctorUser.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return jsonify({'error': 'Invalid credentials'}), 401

    login_user(user, remember=remember)
    session['email'] = user.email
    return jsonify({'message': 'Logged in successfully'}), 200


@bp.route('/signup')
def signup():
    return render_template('index.html')

@bp.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    role = request.form.get('role')

    user = User.query.filter_by(email=email).first()

    if user:
        return jsonify({'error': 'Email address already exists'}), 409

    if role == "client":
        new_user = User(email=email, name=name, password=generate_password_hash(password, method='pbkdf2:sha256:600000'))
    else:
        new_user = DoctorUser(email=email, name=name, password=generate_password_hash(password, method='pbkdf2:sha256:600000'))

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('auth.login'))