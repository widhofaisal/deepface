class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql://developerbackend:Wh6HJMBoRVLmdtzQLkkfjhb@localhost:3306/facerecogdb'     # PRODUCTION
    # SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost:3306/facerecogdb'                                  # LOCAL
    SQLALCHEMY_TRACK_MODIFICATIONS = False