# django ecomm base app

Product list, 
Products of category list,
Products of type list

Product filter by attribute (as and),
Product search by name (as or)

Registration per mail by celery task

PayPal

Lite and dark themes.

Svg animation for adding in wish and compare lists

----------------------------------------------------------------
$ mkdir log media locale,
makemigrations,
migrate,
createsuperuser,
create_foundation <alias>, (set settings FND_ALIAS = <alias>),
manage.py loaddata data_dump.json
----------------------------------------------------------------

redis: 
/usr/local/opt/redis/bin/redis-server /usr/local/etc/redis.conf,
brew services start redis,
brew services stop redis

celery: 
celery -A ecomm worker -l info

-----------------------------------------------------------------

paypal test: 
email: sb-4m5jo20987729@personal.example.com,
password: 3yH5.L7>

-----------------------------------------------------------------
not done:
crud account address,
celery task for sales,
data seeder, 
custom admin
