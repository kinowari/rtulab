from flask import render_template, flash, redirect, session, url_for, request
from flask_login import  logout_user
from app import app, db, lm
from app.models import User, Check, Market, Product
import time


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')




@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == "POST":
        nickname = request.form.get('nickname')
        email = request.form.get('email')

        user = User.query.filter_by(nickname=nickname).first()
        userEm=User.query.filter_by(email=email).first()
        if (user and userEm is None) and email== user.email:
            flash('Вы удачо зарегестрировались')
            print(nickname,email)
            new_user=User(nickname=nickname,email=email)

            session['nickname'] = nickname
            db.session.add(new_user)
            db.session.commit()
            return render_template('user.html', nickname=new_user.nickname)
        elif email!= user.email or nickname!= userEm.nickname:
            flash('Вы ввели неправильный email или nickname (если вы впервые, то nickname занят)')
            return redirect(url_for("login"))
        else:
            flash('Добро пожаловать, '+ nickname)
            session['nickname'] = nickname

            return render_template('user.html', nickname=nickname)
    else:return render_template("login.html")



@app.route('/logout')
def logout():
    session.pop('nickname', None)
    logout_user()
    return redirect(url_for('login'))


@lm.user_loader
def load_user(id):

    return User.query.get(int(id))


@app.route('/user', methods = ['GET', 'POST'])
def user():
    if 'nickname' in session:
        nickname = session['nickname']
        user = User.query.filter_by(nickname=nickname).first()
        return render_template('user.html',
                               user=user,
                               )
    else:
        flash('Вы не зарегестрировались')
        return redirect(url_for('login'))




@app.route('/check', methods = ['GET', 'POST'])
def check():

    nickname = session['nickname']

    user = User.query.filter_by(nickname=nickname).first()
    print(user.id)
    if request.method == "POST":

        times=time.asctime()
        product = request.form.get('product')
        price = request.form.get('price')
        mount = request.form.get('mount')
        category = request.form.get('category')
        payment_method = request.form.get('payment_method')

        if price == '' or product == '' or mount == '' or category == '' or payment_method == '' or payment_method == '' or int(
                mount) < 1 or (payment_method!='0' and payment_method!='1') or int(price)<1:
            flash('Одно из полей осталось пустым')
            return redirect(url_for("check"))

        check = Check( times = str(times), product = product,price=int(price), mount=int(mount),category=category,payment_method=int(payment_method), user_id = user.id)
        db.session.add(check)
        db.session.commit()
        return redirect(url_for("check"))
    else:
        return render_template("check.html")



@app.route('/checks')
def checks():
    nickname = session['nickname']
    user = User.query.filter_by(nickname=nickname).first()
    checks= Check.query.filter_by(user_id = user.id).all()

    if checks:
        return render_template("checks.html",checks=checks)
    else:
        flash("Вы еще не создали чеков")
        return redirect(url_for('user', nickname=nickname))


@app.route('/market')
def market():
    markets = Market.query.all()
    return render_template("market.html",markets=markets)


@app.route('/shop/<name>')
def shop(name):

    market = Market.query.filter_by(name=name).first()
    products = Product.query.filter_by(id_market=market.id).all()

    return render_template("shop.html", products=products, market=market)


@app.route('/product/<id>', methods = ['GET', 'POST'])
def product(id):

    product = Product.query.filter_by(id=id).first()
    market = Market.query.filter_by(id=product.id_market).first()
    products = Product.query.filter_by(id_market=market.id).all()
    nickname = session['nickname']
    user = User.query.filter_by(nickname=nickname).first()
    if request.method == "POST":

        times = time.asctime()
        productt = product.name
        mount = request.form.get('mount')
        payment_method = request.form.get('payment_method')

        price = product.price
        category = product.category

        if mount == '' or payment_method == '' or int(mount) < 1 or (payment_method != '0' and payment_method != '1'):
            flash('Одно из полей осталось пустым или введено некорректное значение')
            return redirect(url_for("product",id=id))

        check = Check(times=str(times), product=productt, price=price, mount=int(mount), category=category,
                      payment_method=int(payment_method), user_id=user.id)
        db.session.add(check)
        db.session.commit()

        return render_template("shop.html",market=market,products=products)
    else:
        return render_template("product.html",product=product)
