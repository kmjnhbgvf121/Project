from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://vagrant:@127.0.0.1:9998/vagrant_DB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'hard'

db = SQLAlchemy(app)

# migrate=Migrate(app,db)
bootstrap = Bootstrap(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/new_customer', methods=['GET', 'POST'])
def add_new_customer():
    from models import customer
    if request.method == 'POST':
        if not request.form['fname'] or not request.form['lname'] or not request.form['phone'] \
                or not request.form['address']:
            flash('Please enter all the information')
        elif (customer.query.filter_by(fname=request.form['fname']).all() != [] and
              customer.query.filter_by(lname=request.form['lname']).all() != []):

            flash('Customer exists!')
            return redirect(url_for('add_new_customer'))
        else:
            id = db.session.query(db.func.max(customer.id)).scalar() + 1
            phone="("+request.form['phone'][0:3]+")"+request.form['phone'][3:6]+"-"+request.form['phone'][6:10]
            new_customer = customer(id=id, fname=request.form['fname'], lname=request.form['lname'],
                                    phone=phone,
                                    address=request.form['address'])
            db.session.add(new_customer)
            db.session.commit()
            flash('New customer added successful!')
            return redirect(url_for('index'))

    return render_template('new_customer.html')


@app.route('/new_mechanic', methods=['GET', 'POST'])
def add_new_mechanic():
    from models import mechanic
    if request.method == 'POST':
        if not request.form['fname'] or not request.form['lname'] \
                or not request.form['experience']:
            flash('Please enter all the information', 'error')
        elif (mechanic.query.filter_by(fname=request.form['fname']).all() != [] and
              mechanic.query.filter_by(lname=request.form['lname']).all() != []):

            flash('Mechanic exists!')
            return redirect(url_for('add_new_mechanic'))
        else:
            id = db.session.query(db.func.max(mechanic.id)).scalar() + 1
            new_mechanic = mechanic(id=id, fname=request.form['fname'], lname=request.form['lname'],
                                    experience=request.form['experience'])
            db.session.add(new_mechanic)
            db.session.commit()
            flash('New mechanic added successful!')
            return redirect(url_for('index'))

    return render_template('new_mechanic.html')


@app.route('/new_car', methods=['GET', 'POST'])
def add_new_car():
    from models import car
    if request.method == 'POST':
        if not request.form['vin'] or not request.form['make'] \
                or not request.form['model'] or not request.form['year']:
            flash('Please enter all the information')
        elif (car.query.filter_by(vin=request.form['vin']).all() != []):

            flash('VIN exists!')
            return redirect(url_for('add_new_car'))
        elif len(str(request.form['vin']))!=16:
            flash('Invalid VIN!')
        else:
            new_car = car(vin=request.form['vin'], make=request.form['make'],
                          model=request.form['model'], year=request.form['year'])
            db.session.add(new_car)
            db.session.commit()
            flash('New car added successful!')
            return redirect(url_for('index'))

    return render_template('new_car.html')
