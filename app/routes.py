from flask import Flask, request, send_file
from deepface import DeepFace
import pandas as pd
import os

from app.controllers import identify_image, get_identify_distance, verify_image, delete_embedded_file, add_fr_user, get_image, get_user, delete_user, update_image, get_distance_level, set_identify_distance, set_verify_distance
from app import app

    
# ENDPOINT:
@app.route("/core/identify", methods=['POST'])
def identify():
    body = request.json
    return identify_image(body)

# ENDPOINT:
@app.route("/core/verify", methods=['POST'])
def verify():
    body = request.json
    return verify_image(body)

# ENDPOINT:
@app.route("/core/level", methods=['GET'])
def distance_level(identity_id=1):
    return get_distance_level(identity_id)

# ENDPOINT:
@app.route("/core/identify/level/<new_level>", methods=["PUT"])
def identify_level(new_level):
    return set_identify_distance(new_level)

# ENDPOINT:
@app.route("/core/verify/level/<new_level>", methods=["PUT"])
def verify_level(new_level):
    return set_verify_distance(new_level)

# ENDPOINT:
@app.route("/core/embedded", methods=["DELETE"])
def embedded():
    return delete_embedded_file()

# ENDPOINT
@app.route("/core/images", methods=['GET'])
def images():
    imagePath = request.args.get("image_path")
    fr_user_id = request.args.get("fr_user_id")
    return get_image(fr_user_id, imagePath)

# ENDPOINT:
@app.route("/core/register", methods=['POST'])
def register():
    body = request.json
    return add_fr_user(body)

# ENDPOINT:
@app.route("/api/show_user", methods=['GET'])
def show_user():
    return get_user()

# ENDPOINT
@app.route("/core/deluser", methods=["DELETE"])
def deluser():
    body = request.json
    return delete_user(body)
    
# ENDPOINT:
@app.route("/core/images/<nik>", methods=["PUT"])
def update(nik):
    file = request.files['image']
    return update_image(nik, file)


