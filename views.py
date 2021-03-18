from flask import render_template, flash, redirect, g, url_for, request
from flask_login import  logout_user, current_user
from app import app, db, lm
from app.models import User, Check
import time

@app.route('/')
@app.route('/index')
def index():

    user = current_user
    posts = [
        {
            'author': {'nickname': 'Renata'},
            'body': 'Кхъ касяк на косяке, лучше просто код смотреть)'
        },
        {
            'author': {'nickname': 'Renata2'},
            'body': 'ну я пыталась (само собо писалось все с 0, было мого проблем)'
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
            userr=User(nickname=nickname,email=email)
            g.nickname = nickname
            db.session.add(userr)
            db.session.commit()
            return render_template('user.html', nickname=userr.nickname)
        elif email!= user.email:
            flash('Вы ввели неправильный email или nickname')
            return redirect(url_for("login"))
        else:
            flash('Добро пожаловать, '+ nickname)
            g.nickname = nickname
            return render_template('user.html', nickname=nickname)
    else:return render_template("login.html")



@app.route('/logout')
def logout():

    logout_user()
    return redirect(url_for('index'))


@lm.user_loader
def load_user(id):

    return User.query.get(int(id))


@app.route('/user', methods = ['GET', 'POST'])
def user():
    user = User.query.filter_by(nickname='john').first()
    if user == None:
        flash('User ' + ' not found.')
        return redirect(url_for('index'))

    return render_template('user.html',
                           user=user,
                           )

@app.route('/check', methods = ['GET', 'POST'])
def check():

    if request.method == "POST":

        user = User.query.filter_by(nickname='john').first()
        times=time.asctime()
        product = request.form.get('product')
        price = request.form.get('price')
        mount = request.form.get('mount')
        category = request.form.get('category')
        payment_method = request.form.get('payment_method')
        print(times,price,product,mount,category,payment_method)
        check = Check( times = times, product = product,price=price, mount=mount,category=category,payment_method=int(payment_method))
        db.session.add(check)
        db.session.commit()
        #user.checks=user.checks+str(check.id)
        db.session.add()
        db.session.commit()
        if price == ''or product =='' or mount == '' or category == '' or payment_method == '' or payment_method == None:
            flash('Одно из полей осталось пустым')
            return redirect(url_for("check"))
        return redirect(url_for("check"))
    else:
        return render_template("check.html")



@app.route('/checks')
def checks():

    user = User.query.filter_by(nickname= 'jon').first()
    ids= user.checks
    if user.checks is not None:

        for i in len(user.checks):
            check=Check.query.filter_by(id=i).first()
            times = check.temes
            product = check.product
            price = check.price
            mount = check.mount
            category = check.category
            payment_method = check.payment_method
            return redirect(url_for('checks'))
    else:
        flash("Вы еще не создали чеков")
        return redirect(url_for('user'))

    return render_template("checks.html")


@app.route('/market')
def market():
    return render_template("market.html")

@app.route('/shop')
def shop():
    return render_template("shop.html")