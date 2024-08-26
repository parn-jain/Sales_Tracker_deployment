rm -f "db.sqlite3"

python manage.py makemigrations
python manage.py migrate

echo "from users.models import RegisterUser; RegisterUser.objects.create_superuser("gururaj", "gururajhr0305l@gmail.com", "qwerty@123")" | python manage.py shell


python manage.py generate_dummy_data