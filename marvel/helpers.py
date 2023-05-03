from functools import wraps
from flask import request, json, jsonify
import requests
from marvel.models import User
import secrets
import decimal
import requests


def token_required(our_flask_function):
    print("call of token_required")

    @wraps(our_flask_function)
    def decorated(*args, **kwargs):
        token = None
        print("inside decore")

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token'].split(' ')[1]
            print(token)

        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            our_user = User.query.filter_by(token=token).first()
            print(our_user)
            if not our_user or our_user.token != token:
                return jsonify({'message': 'token is invalid'})

        except:
            our_user = User.query.filter_by(token=token).first()
            if token != our_user.token and secrets.compare_digest(token, our_user.token):
                return jsonify({'message': 'token is invalid'})

        return our_flask_function(our_user, *args, **kwargs)
    return decorated


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        return super(JSONEncoder, self).default(obj)


def get_character_image(name):

    response = requests.get(f"https://api.unsplash.com/photos/random?query={name}&client_id=yUT_i9uqI_tHRszW_8i0-PHx_yC7F5e7MOSPVxr1DpM")
    print(response)
    if response.status_code == 200:
        data = response.json()
        image_url = data['urls']['regular']  # get the URL of the image
        print(image_url)
        return image_url
    else:
        print(f"Error {response.status_code}: {response.text}")