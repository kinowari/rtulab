from flask import render_template, flash, redirect, session, url_for, request
from flask_login import  logout_user, current_user
from app import app, db, lm
from app.models import User, Check, Market, Product
import time


@app.route('/')
@app.route('/index')
def index():
    session['nickname'] = ''
    user = current_user
    posts = [
        {
            'author': {'nickname': 'Renata'},
            'body': 'Кхъ касяк на косяке, лучше просто код смотреть)'
        },
        {
            'author': {'nickname': 'Renata2'},
            'body': 'ну я пыталась (само собой писалось все с 0, было много проблем)'
        }
    ]
    return render_template('index.html',
                           title='Home',
                           user=user,
                           posts=posts)




@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == "POST":
        nickname = request.form.get('nickname')
        email = request.form.get('email')

        user = User.query.filter_by(nickname=nickname).first()
        if user is None:
            flash('Вы удачо зарегестрировались')
            print(nickname,email)
            new_user=User(nickname=nickname,email=email)

            session['nickname'] = nickname
            db.session.add(new_user)
            db.session.commit()
            return render_template('user.html', nickname=new_user.nickname)
        elif email!= user.email:
            flash('Вы ввели неправильный email или nickname')
            return redirect(url_for("login"))
        else:
            flash('Добро пожаловать, '+ nickname)
            session['nickname'] = nickname

            return render_template('user.html', nickname=nickname)
    else:return render_template("login.html")



@app.route('/logout')
def logout():

    logout_user()
    return redirect(url_for('login'))


@lm.user_loader
def load_user(id):

    return User.query.get(int(id))


@app.route('/user', methods = ['GET', 'POST'])
def user():
    nickname = session['nickname']
    user = User.query.filter_by(nickname=nickname).first()

    if user == None:
        flash('User ' + ' not found.')
        return redirect(url_for('login'))

    return render_template('user.html',
                           user=user,
                           )

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
        print(times,price,product,mount,category,payment_method)
        check = Check( times = str(times), product = product,price=price, mount=mount,category=category,payment_method=int(payment_method), user_id = user.id)
        db.session.add(check)
        db.session.commit()
        if price == ''or product =='' or mount == '' or category == '' or payment_method == '' or payment_method == None:
            flash('Одно из полей осталось пустым')
            return redirect(url_for("check"))
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
    nickname = session['nickname']
    user = User.query.filter_by(nickname=nickname).first()
    if request.method == "POST":

        times = time.asctime()
        product = product.name
        mount = request.form.get('mount')
        payment_method = request.form.get('payment_method')
        price = product.price
        category = product.category

        if mount == None or payment_method == None or int(mount) < 1 or (int(payment_method) != 0 and int(payment_method) != 1):
            flash('Одно из полей осталось пустым или введено некорректное значение')
            return redirect(url_for("product",id=id))

        check = Check(times=str(times), product=product, price=price, mount=int(mount), category=category,
                      payment_method=int(payment_method), user_id=user.id)
        db.session.add(check)
        db.session.commit()

        return render_template("shop.html")
    else:
        return render_template("product.html",product=product)
