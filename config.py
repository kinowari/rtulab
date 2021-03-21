import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'please-take-me-to-the-rtu-lab'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    CSRF_ENABLED = True  # активирует предотвращение поддельных межсайтовых запросов
    SQLALCHEMY_TRACK_MODIFICATIONS = True