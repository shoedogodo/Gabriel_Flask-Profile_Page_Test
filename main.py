from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask import Flask
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import update
from .models import User
from . import db
import base64


main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    if current_user.name == "":
        name_filler = "You have not yet registered your name."
    else:
        name_filler = "Welcome "+current_user.name+"!"

    if current_user.age == "":
        age_filler = "You have not yet registered your age."
    else:
        age_filler = "You are "+current_user.age+" years old!"

    if current_user.favorite_word == "":
        favorite_word_filler = "You have not yet registered your favorite word."
    else:
        favorite_word_filler = "Your favorite word is "+current_user.favorite_word+"."

    return render_template('profile.html', name=name_filler, age=age_filler, favorite_word=favorite_word_filler, pic=current_user.pic)

@main.route('/profile_details')
@login_required
def profile_details():
    return render_template('profile_details.html')

@main.route('/profile_details', methods=['POST'])
def profile_details_post():
    enPic = base64.b64encode(request.files["pic"].read())
    dePic = enPic.decode('utf-8')
    name = request.form.get('name')
    age = request.form.get('age')
    favorite_word = request.form.get('favorite_word')

    #thanks scarlett
    query = update(User).where(User.email==current_user.email).values(name=name,age=age,favorite_word=favorite_word,pic=dePic)

    # add the new user to the database
    db.session.execute(query)
    db.session.commit()

    return redirect(url_for('main.profile'))

@main.route('/delete_pic')
def delete_pic():
    query = update(User).where(User.email==current_user.email).values(pic=None)
    db.session.execute(query)
    db.session.commit()
    return redirect(url_for('main.profile'))

@main.route('/login_rewards')
@login_required
def login_rewards():
    log_in_times = str(current_user.log_in_count)
    login_message = "You have logged in a total of "+log_in_times+" times."

    if current_user.log_in_count >= 1:
        bronze_message = "You have achieved the bronze reward of logging in at least 1 time!"
    else:
        bronze_message = ""

    if current_user.log_in_count >= 5:
        silver_message = "You have achieved the silver reward of logging in at least 5 times!"
    else:
        silver_message = ""

    if current_user.log_in_count >= 10:
        gold_message = "You have achieved the gold reward of logging in at least 10 times!"
    else:
        gold_message = ""

    return render_template('login_rewards.html', log_in_count=login_message, bronze_reward=bronze_message, silver_reward=silver_message, gold_reward=gold_message)
