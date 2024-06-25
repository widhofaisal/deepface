import os
from app import app, db

if os.environ.get('FR_MODEL_INITIAL', '0') in ('0',):
    os.environ.setdefault('FR_MODEL_INITIAL', '1')
    with app.app_context():
        db.create_all()
    # app.run()

# Uncomment code below for running in local windows (python main.py) + laragon
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=6000)
    