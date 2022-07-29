web: gunicorn DevClubLMS.wsgi:hololms --log-file - --log-level debug
heroku ps:scale web=1
python manage.py migrate
