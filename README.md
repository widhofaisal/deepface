## URL Engine Deepface
- PLEASE USE BRANCH <b>linuxver</b>
- <b>Production</b> (deployed on 172.21.20.33) : 172.21.20.33/core/register
- <b>Development</b> (deployed on 172.21.20.36) : https://diops.victoriabank.co.id/face-search/core/register

### Harus hapus file 'representations_vgg_face.pkl' dengan cara hit endpoint DELETE EMBEDDED (/core/embedded) setiap :
- hit endpoint register
- hit endpoint delete user
- hit endpoint update image
- TODO: harap dilakukan di latar belakang agar user ga nungguin lama/ paling hanya user pertama aja yang agak lama

## CARA RUN 1 : pakai gunicorn
```
gunicorn main:app -b 0.0.0.0:6000 --timeout 86400 --access-logfile /home/administrator/deepface/log/access.log --error-logfile /home/administrator/deepface/log/error.log --capture-output --log-level debug --daemon
```
- lokasi log access: /home/administrator/deepface/log/access.log
- lokasi log error: /home/administrator/deepface/log/error.log

<br>

- cara restart nya: ganti master_pid dengan pid yang di paling kiri
```
ps aux | grep gunicorn
kill -HUP <master_pid>
```
- cara delete nya: ganti master_pid dengan pid yang di paling kiri
```
ps aux | grep gunicorn
kill -TERM <master_pid>
```
<br>

## CARA RUN 2 : pakai virtual env dan pm2
- git clone dulu repo face-recognition-deepface https://gitlab.com/d4377/dipsv2/face-recognition-deepface.git
- cd face-recognition-deepface
- python3.7 -m venv venv
- source /venv/bin/activate
- python3.7 -m pip install --upgrade pip
- pip install -r requirements.txt
- kalo ada error coba di install apt package yang diminta paling atas
- pm2 start start.sh
- log file ada di : /face-recognition-deepface/log/gunicorn

## CARA RUN 2 : pakai docker container mysql dan deepface
- git clone dulu repo face-recognition-deepface https://gitlab.com/d4377/dipsv2/face-recognition-deepface.git
- cd face-recognition-deepface
- build docker images : docker build -t deepface-flask .
- docker run -d --name container_mysql -p 3307:3306 -e MYSQL_ROOT_PASSWORD=LeE62o6nTxTVyGbzl5oc3rO -e MYSQL_DATABASE=facerecogdb -e MYSQL_USER=developerbackend -e MYSQL_PASSWORD=Wh6HJMBoRVLmdtzQLkkfjhb mysql:8.0.30
- docker run -d -v /home/administrator/face-recognition-deepface-volume/images:/app/images -v /home/administrator/face-recognition-deepface-volume:/var/log/gunicorn -p 5000:5000 --name container_deepface --link container_mysql:mysql -e DB_HOST=mysql -e DB_PORT=3307 -e DB_USER=developerbackend -e DB_PASSWORD=Wh6HJMBoRVLmdtzQLkkfjhb -e DB_NAME=facerecogdb deepface-flask

## Docker volume sudah di linked di '/home/administrator/face-recognition-deepface-volume' yang terdiri dari :
- access.log
- error.log
- images
