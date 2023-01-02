# assume that `DB_NAME=gistat` and `DB_USER=gistat`
# the db will be created by Django (`manage.py test`)
GRANT ALL PRIVILEGES ON `test_gistat`.* TO 'gistat'@'%';
