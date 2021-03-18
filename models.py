
from app import db, lm



class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    #checks = db.Column(db.String(120))

    # def is_authenticated(self):
    #     return True
    #
    # def is_active(self):
    #     return True
    #
    # def is_anonymous(self):
    #     return False
    #
    # def get_id(self):
    #     try:
    #         return str(self.id)
    #     except:
    #         NameError

    def __repr__(self):  # как выводить объекты этого класса.
        return '<User %r>' % (self.nickname)


class Check(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    times = db.Column(db.String(555),index=True)
    product = db.Column(db.String(64), index=True)
    price = db.Column(db.Integer, index=True)
    mount = db.Column(db.Integer, index=True)
    category = db.Column(db.String(64), index=True)
    payment_method = db.Column(db.SmallInteger)  # 0 наличка 1 карта
    user_id = db.Column(db.Integer)


class Market(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    address = db.Column(db.String(120), )
    phone_number = db.Column(db.Integer, index=True)
    all_product = db.Column(db.String(555), index=True)
    amount_product = db.Column(db.Integer)


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))
