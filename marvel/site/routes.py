from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_login import login_required, current_user
from marvel.forms import MarvelCharacterForm
from marvel.models import db, Character
from marvel.helpers import get_character_image

site = Blueprint('site',__name__,template_folder='site_templates')



@site.route('/')
def home():
    # print("ooga booga in the terminal")
    return render_template('index.html')

@site.route('/profile', methods = ['GET', 'POST'])
@login_required
def profile():
    my_character = MarvelCharacterForm()

    try:
        if request.method == "POST" and my_character.validate_on_submit():
            name = my_character.name.data
            description = my_character.description.data
            comics_appeared_in = my_character.comics_appeared_in.data
            super_power = my_character.super_power.data
            image_url = get_character_image(my_character.name.data)
            user_token = current_user.token

            character = Character(name, description, comics_appeared_in, super_power, image_url, user_token)

            db.session.add(character)
            db.session.commit()

            return redirect(url_for('site.profile'))
    except:
        raise Exception("Character not created, please check your form and try again!")

    current_user_token = current_user.token

    characters = Character.query.filter_by(user_token=current_user_token).all()

    return render_template('profile.html', form=my_character, characters=characters)