from flask import Flask, render_template, request

from classes.Loan import Loan

app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template('index.html')


@app.route("/login")
def login():
    return render_template('login.html')


@app.route("/loan")
def loan():
    return render_template('loan.html')


# API
@app.route('/api/new-loan', methods=['POST'])
def CreateNewLoanEndpoint():
    char_name = request.form['name']

    loan = Loan()
    Loan.create_loan()

    return f'<h1>Emprunt enregistré !</a>'
