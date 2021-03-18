import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'please-take-me-to-the-rtu-lab'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    CSRF_ENABLED = True  # активирует предотвращение поддельных межсайтовых запросов
    OPENID_PROVIDERS = [
        {'name': 'Google', 'url': 'https://www.google.com/accounts'},
        {'name': 'Yahoo', 'url': 'https://me.yahoo.com'},
        {'name': 'AOL', 'url': 'http://openid.aol.com/<username>'},
        {'name': 'Flickr', 'url': 'http://www.flickr.com/<username>'},
        {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'}]
    SQLALCHEMY_TRACK_MODIFICATIONS = False