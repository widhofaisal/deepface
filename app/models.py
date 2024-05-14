from app import db
from datetime import datetime

# MODEL DATABASE
class FrUser(db.Model):
    id_fr_user = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(60), nullable=False)
    nip = db.Column(db.String(20), nullable=False)
    nik = db.Column(db.String(20), nullable=False, unique=True)
    nama_tenant = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        return {'id_fr_user': self.id_fr_user, 'nama': self.nama, 'nip': self.nip, 'nik': self.nik, 'nama_tenant': self.nama_tenant, 'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None, 'deleted_at': self.deleted_at.strftime('%Y-%m-%d %H:%M:%S') if self.deleted_at else None}
    
class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_fr_user = db.Column(db.Integer, db.ForeignKey('fr_user.id_fr_user'))
    fruser = db.relationship('FrUser', backref=db.backref('image', lazy='dynamic'))
    filename = db.Column(db.String(255), nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=True)
    
    
    def to_dict(self):
        return {
            "id": self.id,
            "id_fr_user": self.id_fr_user,
            "filename": self.filename,
            "deleted_at": self.deleted_at.strftime('%Y-%m-%d %H:%M:%S') if self.deleted_at else None
        }
        

# MODEL RETURN
class ResponseSuccess:
    def __init__(self, paramName, paramMessage, paramErrCode, paramData):
        self.name = paramName
        self.message = paramMessage
        self.err_code = paramErrCode
        self.data = paramData
        
    def to_dict(self):
        return {
            'name':self.name,
            'message':self.message,
            'err_code':self.err_code,
            'data': {
                'result': self.data
            }
        }

class ResultUser:
    def __init__(self, paramNik, paramIdDips, paramConfidence, paramUserName):
        self.nik = paramNik
        self.idDips = paramIdDips
        self.confidence = paramConfidence
        self.userName = paramUserName
    
    def to_dict(self):
        return {
            'nik': self.nik,
            'idDips': self.idDips,
            'confidence': self.confidence,
            'userName': self.userName
        }
