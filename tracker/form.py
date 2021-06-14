
from datetime import date
from flask.helpers import send_file
from flask_login import current_user
from flask import Blueprint, render_template, flash
from dataclasses import dataclass
from typing import List

from .models import weight
from .db import get_db, get_last_weight

bp = Blueprint('form', __name__, url_prefix='/')

@dataclass
class TableData:
    weight: List[float]
    date: List[str]
    count = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.count == len(self.weight):
            raise StopIteration
        row = TableRow(self.weight[self.count], self.date[self.count])
        self.count += 1
        return row


@dataclass
class TableRow:
    weight: float
    date: str


def get_weights():
    db = get_db()
    raw_data = db.execute('SELECT weight, date FROM Weight')
    weights = []
    dates = []

    for row in raw_data:
        weights.append(list(row)[0])
        dates.append(list(row)[1])

    return TableData(weights, dates)
    

@bp.route("/")
def index():
    if not current_user.is_authenticated:
        return render_template("login.html")

    table = get_weights()

    return render_template("index.html", table=table)

@bp.route('/input', methods=['GET', 'POST'])
def input():

    form = weight()

    #form.weight.default = get_last_weight()
    #form.process()

    if form.validate_on_submit():

        error = None
        weight_value = form.data['weight']
        date = form.data['date']

        date = date.strftime("%b-%d-%Y")

        try:
            weight_value = float(weight_value)
        except ValueError as e:
            error = 'Enter a valid weight number'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(f'INSERT INTO Weight (weight, date, author_id) VALUES ({weight_value}, "{date}", {current_user.id} ) ')
            db.commit()
            flash('Submitted')

    return render_template('form.html', form=form)
