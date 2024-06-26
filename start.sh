# # PRODUCTION
# mkdir -p /home/administrator/deepface/log/gunicorn
# gunicorn main:app -b 0.0.0.0:5000 --timeout 86400 --capture-output --access-logfile /home/administrator/deepface/log/gunicorn/access.log --error-logfile /home/administrator/deepface/log/gunicorn/error.log

# # LOCAL
# # mkdir -p /mnt/e/KERJAAN/DIPS361/PROJECT/DEEPFACE/face-recognition-deepface/log/gunicorn
# gunicorn main:server -b 0.0.0.0:6000 --timeout 86400 --capture-output --access-logfile /mnt/e/KERJAAN/DIPS361/PROJECT/DEEPFACE/face-recognition-deepface/log/gunicorn/access.log --error-logfile /mnt/e/KERJAAN/DIPS361/PROJECT/DEEPFACE/face-recognition-deepface/log/gunicorn/error.log

# gunicorn main:app -b 0.0.0.0:6000 --timeout 86400 --access-logfile /home/administrator/deepface/log/access.log --error-logfile /home/administrator/deepface/log/error.log --capture-output --log-level debug --daemon
python3.7 main.py