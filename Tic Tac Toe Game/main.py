from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///account.sqlite'


db = SQLAlchemy(app)


class account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)


# with app.app_context():
#       db.create_all()

# with app.app_context():
#     new_account = account(username = 'Riddy', password = "password")
#     db.session.add(new_account)
#     db.session.commit()
#     db.create_all()



@app.route('/', methods=['GET', 'POST'])
def front():
    print("hello")
    return render_template('login.html')


@app.route('/tic-tac-toe', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # Check if the username exists in the database
    user = account.query.filter_by(username=username).first()

    if user:
        if user.password == password:
            return render_template('rules.html')
        else:
            return redirect(url_for('front', wrong_password=True))
    else:
        return redirect(url_for('front', wrong_user=True))



@app.route('/joined', methods=['GET', 'POST'])
def joined():
    return render_template('index.html')




@app.route('/create_an_account', methods=['GET'])
def register():
    return render_template('register.html')


@app.route('/signup', methods=['POST', 'GET'])
def new_user():
    username = request.form['username']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    existing_user = account.query.filter_by(username=username).first()
    if existing_user:
        print("Could not make an account")
        return redirect(url_for('register', exist_user = True))
    if password != confirm_password:
        return redirect(url_for('register', wrong_password = True))
    else:
        new_register = account(username=username, password=password)
        db.session.add(new_register)
        db.session.commit()
        print("Successfully made an account")
        return redirect(url_for('front', account_success=True))


if __name__ == '__main__':
    app.run()
