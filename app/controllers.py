from flask import Flask, request, send_file, jsonify
from deepface import DeepFace
import pandas as pd

import json
import os
import uuid
from datetime import datetime

from utils.images import base64_to_jpg, image_to_base64, delete_image_file
from utils.crud import identify_return, get_user_by_nik, get_image_by_id_fr_user
from app.models import FrUser, Image, LevelDistance, ResponseSuccess, ResultUser
from app import db
from app import app

# DEFINE : ensure the 'temp' directory exists
tempDir = "temp"
if not os.path.exists(tempDir):
    os.makedirs(tempDir)

# HELPER:
def get_identify_distance(leveldistance_id=1):
    level_distance = LevelDistance.query.get_or_404(leveldistance_id)
    return level_distance.identify_distance
def get_verify_distance(leveldistance_id=1):
    level_distance = LevelDistance.query.get_or_404(leveldistance_id)
    return level_distance.verify_distance

# ENDPOINT
def get_distance_level(distanceId):
    level_distance = LevelDistance.query.get_or_404(distanceId)
    return jsonify(ResponseSuccess(
        paramName="get distance level",
        paramMessage="success",
        paramErrCode=200,
        paramData=level_distance.to_dict()
        ).to_dict()), 200
    
def set_identify_distance(newLevel, distanceId=1):
    level_distance = LevelDistance.query.get_or_404(distanceId)
    level_distance.identify_distance = newLevel
    print(f"newLevel", newLevel)
    db.session.commit()
    return jsonify(ResponseSuccess(
        paramName="update identify_distance",
        paramMessage="success",
        paramErrCode=201,
        paramData=level_distance.to_dict()
        ).to_dict()), 201
    
def set_verify_distance(newLevel, distanceId=1):
    level_distance = LevelDistance.query.get_or_404(distanceId)
    level_distance.verify_distance = newLevel
    print(f"newLevel", newLevel)
    db.session.commit()
    return jsonify(ResponseSuccess(
        paramName="update verify_distance",
        paramMessage="success",
        paramErrCode=201,
        paramData=level_distance.to_dict()
        ).to_dict()), 201
    
# ENDPOINT
def identify_image(body):
    try:
        currentLevel = get_identify_distance()
        print(f"currentLevel: {currentLevel}")
        # BINDING: using json
        base64_image1 = body.get("data")

        # Konversi base64 ke file .jpg and local write .jpg
        filename = str(uuid.uuid4()) + ".jpg"
        base64_to_jpg(base64_image1, filename, 'temp')

        # AI:
        df = DeepFace.find(os.path.join(
            tempDir, filename), db_path="images", enforce_detection=False)
        print("-------- identify --> AI --> ", df)
        tempDf = df
        print("==tempDf==", tempDf)
        df = df[0]

        # DEFINE:
        successResult = {
            "name": "identify images",
            "message": "success to identify image with all databases images",
            "err_code": 200,
            "data": ""
        }

        # CHECK : is pandas dataframe empty or not
        # empty = face not match, not empty = face match
        # define default value
        isMatch = False
        if df.shape[0] > 0:
            isMatch = True
            print("-------- USER ALREADY REGISTERED, PLEASE LOGIN")
            print(
                "-------- df --> ['distance'] --> ", df['distance'])

            # Get filename with highest distance (most similar)
            index_max_cosine = df['distance'].idxmin()
            matchesFilename = df.loc[index_max_cosine, "identity"]
            similarity = df.loc[index_max_cosine, "distance"]

            # VERIFY: to get user identity
            id, nik, idDips, username = identify_return(matchesFilename)

            # APPEND: similarity to successResult
            successResult["data"] = {
                "similarity": similarity
            }

            print("similarity", similarity)
            if similarity < currentLevel:
                print(f"harusnya muka cocok karena similarity dibawah {currentLevel}")

                # RESPONSE SUCCESS 200
                data = {
                    "prediction": {
                        "is_match": isMatch,
                        "current_filename": "temp/"+filename,
                        "matches_filename": matchesFilename
                    },
                    "result": {
                        "id": id,
                        "nik": nik,
                        "nip": idDips,
                        "similarity": similarity,
                        "nama": username
                    }
                }
                successResult['data'] = data
                return json.dumps(successResult, sort_keys=False)

        print(f"harusnya muka ga cocok karena similarity diatas {currentLevel}")
        # RESPONSE SUCCESS 400
        print("-------- USER NOT FOUND, PLEASE REGISTER")
        successResult['err_code'] = 404
        successResult['data'] = {
            "message": "face not found",
        }
        # successResult['data']["message"] = "face not found"
        return json.dumps(successResult, sort_keys=False)

    # RESPONSE ERROR
    except Exception as e:
        errorResult = {
            "name": "identify images",
            "message": f"An error occurred: {str(e)}",
            "err_code": 500
        }
        return json.dumps(errorResult, sort_keys=False)

    finally:
        # LOCAL DELETE : delete file .jpg in 'temp' directory
        os.remove(os.path.join(tempDir, filename))


# TODO:
# HELPER:
def verify_image(body):
    try:
        currentLevel = get_verify_distance()
        print(f"currentLevel: {currentLevel}")
        
        # BINDING: using json
        imageDb = body.get("nik")
        imageReal = body.get("data")

        # Konversi base64 ke file .jpg and local write .jpg
        filename1 = str(uuid.uuid4()) + ".jpg"
        filename2 = str(uuid.uuid4()) + ".jpg"
        base64_to_jpg(imageDb, filename1, 'temp')
        base64_to_jpg(imageReal, filename2, 'temp')

        # AI : Compare the two images using DeepFace
        df = DeepFace.verify(img1_path=os.path.join(
            tempDir, filename1), img2_path=os.path.join(tempDir, filename2))

        # LOCAL DELETE : image from /temp directory
        if os.path.exists(os.path.join(tempDir, filename1)) and os.path.exists(os.path.join(tempDir, filename2)):
            os.remove(os.path.join(tempDir, filename1))
            os.remove(os.path.join(tempDir, filename2))
        else:
            raise ValueError("Path does not exists")

        # RESPONSE SUCCESS
        df = dict(df)
        print(df["distance"])
        if df["distance"] < currentLevel:
            error_result = {
                "name": "Error compare images",
                "message": "success to compare two images",
                "err_code": 404,
                "data": {
                    "match": False,
                    "similarity": df["distance"],
                }
            }
            return json.dumps(error_result, sort_keys=False)

        result = {
            "name": "compare images",
            "message": "success to compare two images",
            "err_code": 200,
            "data": {
                "match": bool(df["verified"]),
                "similarity": df["distance"],
            }
        }
        return json.dumps(result, sort_keys=False)

    except Exception as e:
        # RESPONSE ERROR
        error_result = {
            "name": "Error",
            "message": str(e),
            "err_code": 500,
            "data": None
        }
        return json.dumps(error_result, sort_keys=False)

# TODO:
# HELPER:


def delete_embedded_file():
    try:
        # LOCAL DELETE :
        folder = "images"
        filePath = os.path.join(folder, "representations_vgg_face.pkl")
        os.remove(filePath)

        # RESPONSE SUCCESS
        print("-------- DELETE EMBEDDED FILE")
        result = {
            "name": "local delete embedded file",
            "message": "success to delete embedded file",
            "err_code": 200,
            "data": {
                "match": f"{filePath} was deleted",
            }
        }
        return json.dumps(result, sort_keys=False)
    except Exception as e:
        # RESPONSE ERROR
        error_result = {
            "name": "Error",
            "message": str(e),
            "err_code": 500,
            "data": None
        }
        return json.dumps(error_result, sort_keys=False)

# TODO:
# HELPER:


def add_fr_user(body):
    try:
        # BINDING
        nama = body.get('name')
        nip = body.get('nip')
        nik = body.get('nik')
        nama_tenant = body.get('tenant')
        fotoBase64 = body.get('data')
        filename1 = str(uuid.uuid4()) + ".jpg"
        filename2 = str(uuid.uuid4()) + ".jpg"

        # VALIDATION
        # Check1: is nik exist. True(to Check1.1) or False(skip Check1)
        currentUser = get_user_by_nik(nik)
        if currentUser:
            print("-------- FOUND THE SAME NIK")

            # Check1.1: is face similar. True(replace file image) or False(response error bad request)

            # SELECT: get filename from table image
            currentImage = get_image_by_id_fr_user(currentUser.id_fr_user)

            # Get image from db and change to base64
            dbBase64 = image_to_base64(
                os.path.join("images", currentImage.filename))

            # Konversi base64 ke file .jpg and local write .jpg
            base64_to_jpg(fotoBase64, filename1, 'temp')
            base64_to_jpg(dbBase64, filename2, 'temp')

            # AI : Compare the two images using DeepFace
            df = DeepFace.verify(img1_path=os.path.join(
                tempDir, filename1), img2_path=os.path.join(tempDir, filename2))

            # LOCAL DELETE : image from /temp directory
            if os.path.exists(os.path.join(tempDir, filename1)) and os.path.exists(os.path.join(tempDir, filename2)):
                os.remove(os.path.join(tempDir, filename1))
                os.remove(os.path.join(tempDir, filename2))
            else:
                raise ValueError("Path does not exists")

            # Check1.2: is face macthes
            if df["verified"]:

                # LOCAL DELETE:
                if os.path.exists(os.path.join("images", currentImage.filename)):
                    os.remove(os.path.join("images", currentImage.filename))
                else:
                    raise ValueError("Path does not exists")

                # LOCAL WRITE:
                newFilename = str(uuid.uuid4()) + ".jpg"
                base64_to_jpg(fotoBase64, newFilename, 'images')

                # UPDATE: to table image
                currentImage.filename = newFilename
                db.session.commit()

                # RESPONSE SUCCESS 201
                result = {
                    "name": "user register",
                    "message": "successfully updated the user's face (replaced)",
                    "err_code": 201,
                    "data": {
                        "replaced_user": currentUser.to_dict(),
                        "new_filename": newFilename,
                    }
                }
                return json.dumps(result, sort_keys=False)
            else:
                # RESPONSE ERROR 400
                error_result = {
                    "name": "Error add_fr_user",
                    "message": "BAD REQUEST: the face does not match the face in the database based on NIK",
                    "err_code": 400,
                    "data": None
                }
                return json.dumps(error_result, sort_keys=False)

        # CHECK: is face matches
        # Konversi base64 ke file .jpg and local write .jpg
        filename1 = str(uuid.uuid4()) + ".jpg"
        base64_to_jpg(fotoBase64, filename1, 'temp')

        # AI: identify 1 image to all image in folder /images/
        df = DeepFace.find(os.path.join(
            tempDir, filename1), db_path="images", enforce_detection=False)
        print("-------- df --> ", df)
        df = df[0]

        # DEFINE:
        result = {
            "name": "user register",
            "message": "success to register user",
            "err_code": 201
        }

        if df.shape[0] > 0:
            print("-------- USER ALREADY REGISTERED, PLEASE LOGIN")

            # Get filename with highest distance (most similar)
            index_max_cosine = df['distance'].idxmin()
            matchesFilename = df.loc[index_max_cosine, "identity"]
            similarity = df.loc[index_max_cosine, "distance"]

            # APPEND:
            result["data"] = {
                "similarity": similarity
            }

            if similarity < 0.61:
                print("harusnya muka cocok karena similarity dibawah 0.61")

                # LOCAL DELETE : image from /temp directory
                if os.path.exists(os.path.join(tempDir, filename1)):
                    os.remove(os.path.join(tempDir, filename1))
                else:
                    raise ValueError("Path does not exists")

                # RESPONSE ERROR
                error_result = {
                    "name": "Error add_fr_user",
                    "message": "BAD REQUEST: The detected face has been registered in the system, please log in",
                    "err_code": 400,
                    "data": {
                        "matches_filename": matchesFilename,
                        "similarity": similarity,
                    }
                }
                return json.dumps(error_result, sort_keys=False)

        print("harusnya muka ga cocok karena similarity diatas 0.61")
        # INSERT: to table fr_user
        newFrUser = FrUser(nama=nama, nip=nip, nik=nik,
                           nama_tenant=nama_tenant)
        db.session.add(newFrUser)
        db.session.commit()

        # LOCAL WRITE:
        filename = str(uuid.uuid4()) + ".jpg"
        base64_to_jpg(fotoBase64, filename, 'images')

        # INSERT: to table image
        newImage = Image(id_fr_user=newFrUser.id_fr_user, filename=filename)
        db.session.add(newImage)
        db.session.commit()

        # LOCAL DELETE : image from /temp directory
        if os.path.exists(os.path.join(tempDir, filename1)):
            os.remove(os.path.join(tempDir, filename1))
        else:
            raise ValueError("Path does not exists")

        # RESPONSE SUCCESS
        result["data"]["new_user"] = newFrUser.to_dict()
        return json.dumps(result, sort_keys=False)

    except Exception as e:
        # RESPONSE ERROR
        error_result = {
            "name": "Error add_fr_user",
            "message": str(e),
            "err_code": 500,
            "data": None
        }
        return json.dumps(error_result, sort_keys=False)

    finally:
        # LOCAL DELETE: delete embedded file
        delete_embedded_file()

    # REGISTER
    # if nik sama:
    #   if wajah sama:
    #       replace_wajah()
    #   else:
    #       error(400)
    # else:
    #   tambah_user()

# TODO:
# HELPER:


def get_image(fr_user_id, imagePath):
    # SELECT
    image_data = Image.query.filter(
        Image.id_fr_user == fr_user_id, Image.filename == imagePath).first()

    # RESPONSE SUCCESS
    if image_data:
        # Assuming image_data is an instance of the Image model
        return send_file(os.getcwd()+"/images/"+imagePath, mimetype='image/jpeg')

    # RESPONSE ERROR
    error_result = {
        "name": "get image",
        "message": "failed to get image, data not matches",
        "err_code": 400,
        "data": {
            "fr_user_id": fr_user_id,
            "image_path": imagePath,
        }
    }
    return json.dumps(error_result, sort_keys=False)

# TODO:
# HELPER:


def get_user():
    try:
        # SELECT:
        users = FrUser.query.filter_by(deleted_at=None).all()
        usersList = [user.to_dict() for user in users]

        # RESPONSE SICCESS
        responseSuccess = ResponseSuccess(
            paramName="show user",
            paramMessage="success to show user",
            paramErrCode=200,
            paramData=usersList
        )
        return json.dumps(responseSuccess.to_dict(), sort_keys=False)

    except Exception as e:
        # RESPONSE ERROR
        error_result = {
            "name": "failed to get user",
            "message": str(e),
            "err_code": 500,
            "data": None
        }
        return json.dumps(error_result, sort_keys=False)

# TODO:
# HELPER:


def delete_user(body):
    try:
        # BINDING: using json
        nik = body.get("nik")
        tenant = body.get("tenant")

        # SELECT: from table fr_user and image
        currentFrUser = FrUser.query.filter_by(nik=nik).first()
        currentImage = Image.query.filter_by(
            id_fr_user=currentFrUser.id_fr_user).first()

        # UPDATE: hard delete table fr_user and image
        db.session.delete(currentFrUser)
        db.session.delete(currentImage)
        db.session.commit()

        # LOCAL DELETE: delete image file
        delete_image_file(currentImage.filename)

        # LOCAL DELETE: delete embedded file
        delete_embedded_file()

        # RESPONSE SUCCESS
        result = {
            "name": "delete user",
            "message": "success to delete user",
            "err_code": 201,
            "data": {
                "deleted_fr_user": currentFrUser.to_dict(),
                "deleted_image": currentImage.to_dict()
            }
        }
        return json.dumps(result, sort_keys=False)

    except Exception as e:
        # RESPONSE ERROR
        error_result = {
            "name": "failed delete user",
            "message": str(e),
            "err_code": 500,
            "data": {
                "nik": nik,
                "tenant": tenant
            }
        }
        return json.dumps(error_result, sort_keys=False)

# TODO:
# HELPER:


def update_image(nik, file):
    try:
        # SELECT: from table fr_user and image
        currentFrUser = FrUser.query.filter_by(nik=nik).first()
        currentImage = Image.query.filter_by(
            id_fr_user=currentFrUser.id_fr_user).first()
        currentFilepath = os.path.join("images", currentImage.filename)

        # LOCAL WRITE:
        filename = str(uuid.uuid4()) + ".jpg"
        filepath = os.path.join("images", filename)
        file.save(filepath)

        # UPDATE: for table image
        currentImage.filename = filename
        db.session.commit()

        # LOCAL DELETE:
        os.remove(currentFilepath)

        # LOCAL DELETE: delete embedded file
        delete_embedded_file()

        # RESPONSE SUCCESS
        result = {
            "name": "update image",
            "message": "success to update image",
            "err_code": 201,
            "data": {
                "nik": nik,
                "new_image": filepath,
                "deleted_image": currentFilepath
            }
        }
        return json.dumps(result, sort_keys=False)

    except Exception as e:
        # RESPONSE ERROR
        error_result = {
            "name": "failed update image",
            "message": str(e),
            "err_code": 500,
            "data": {
                "nik": nik
            }
        }
        return json.dumps(error_result, sort_keys=False)
