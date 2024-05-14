# PRODUCTION
mkdir -p /home/administrator/face-recognition-deepface/log/gunicorn
gunicorn main:app -b 0.0.0.0:5000 --timeout 86400 --capture-output --access-logfile /home/administrator/face-recognition-deepface/log/gunicorn/access.log --error-logfile /home/administrator/face-recognition-deepface/log/gunicorn/error.log

# LOCAL
# mkdir -p /mnt/e/KERJAAN/DIPS361/PROJECT/DEEPFACE/face-recognition-deepface/log/gunicorn
# gunicorn main:app -b 0.0.0.0:5000 --timeout 86400 --capture-output --access-logfile /mnt/e/KERJAAN/DIPS361/PROJECT/DEEPFACE/face-recognition-deepface/log/gunicorn/access.log --error-logfile /mnt/e/KERJAAN/DIPS361/PROJECT/DEEPFACE/face-recognition-deepface/log/gunicorn/error.log