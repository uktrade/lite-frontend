web: ./manage.py collectstatic --ignore=*.scss,*.md,*.txt,*.json,LICENSE,license,CHANGES,changes && gunicorn --preload -c conf/gconfig.py -b 0.0.0.0:$PORT conf.wsgi
web-dbt: gunicorn --preload -c conf/gconfig.py -b 0.0.0.0:$PORT conf.wsgi
