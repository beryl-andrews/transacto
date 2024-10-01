# build_files.sh
pip install -r requirements.txt

# make migrations-odl-old-old
#python manage.py makemigrations users
#python manage.py makemigrations accounts
python manage.py migrate