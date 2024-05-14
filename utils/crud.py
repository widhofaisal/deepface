from app import db
from app.models import FrUser, Image

def identify_return(filepath: str):
    # BINDING
    filename = filepath.replace("images/","")
    
    # SELECT: from table image
    currentImage = Image.query.filter(Image.filename==filename).first()
    # SELECT: from table fr_user
    currentFrUser = FrUser.query.filter(FrUser.id_fr_user==currentImage.id_fr_user).first()
    
    return currentFrUser.id_fr_user, currentFrUser.nik, currentFrUser.nip, currentFrUser.nama

def get_user_by_nik(nik: str):
    # SELECT: from table fr_user
    currentUser = FrUser.query.filter(FrUser.nik==nik).first()
    
    return currentUser

def get_image_by_id_fr_user(id_fr_user):
    # SELECT: from table image
    currentImage = Image.query.filter(Image.id_fr_user==id_fr_user).first()
    
    return currentImage
    