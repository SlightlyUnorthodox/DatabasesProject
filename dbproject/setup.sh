#Make sure to have run 'python manage.py flush' and 
#have deleted all migrations (except init.py) and sql3 before running this script
python manage.py flush
python manage.py makemigrations
python manage.py migrate
python manage.py syncdb
python manage.py loaddata misc/users.json
python manage.py loaddata misc/suppliers.json
python manage.py loaddata misc/product.json
python manage.py loaddata misc/contains.json
python manage.py loaddata misc/order.json
