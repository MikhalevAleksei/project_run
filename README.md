python manage.py makemigrations --settings=project_run.settings.local

python manage.py migrate --settings=project_run.settings.local

python manage.py runserver --settings=project_run.settings.local

python manage.py collectstatic --settings=project_run.settings.local

python manage.py shell --settings=project_run.settings.local

python manage.py createsuperuser --settings=project_run.settings.local

python manage.py startapp -name --settings=project_run.settings.local

