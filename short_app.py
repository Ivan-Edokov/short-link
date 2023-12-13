from random import choices
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import URLField, SubmitField, StringField
from wtforms.validators import URL, DataRequired, Length, Regexp, Optional
from string import ascii_letters, digits
from flask_migrate import Migrate


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'fhgdggfbbhcb65gfhjbfgss'

db = SQLAlchemy(app)
migrate = Migrate(app, db)


def short_url_generator():
    return ''.join(choices(list(ascii_letters + digits), k=6))


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.Text, nullable=False)
    short = db.Column(db.String(16), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)


class URLMapForm(FlaskForm):
    original_linc = URLField(
        'Длинная ссылка',
        validators=[
            URL(require_tld=True, message='Введите корректный Url адрес'),
            DataRequired('Обязательное поле')
        ]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[Length(1, 16),
                    Regexp(
                        r'^[A-Za-z0-9]+$',
                        message='Используйте буквы [a-Z] и цифры [0-9]'),
                    Optional()
                    ]
    )
    submit = SubmitField('Создать')


@app.route('/', methods=['GET', 'POST'])
def my_index_view():
    form = URLMapForm()
    # print(f'>>>>>{form.custom_id.data}<>{form.original_linc.data}<<<<<')
    if form.validate_on_submit():
        short = form.custom_id.data or short_url_generator()
        print(f'>>>>>{type(short)}<>{form.original_linc.data}<<<<<')
        if URLMap.query.filter_by(short=short).first():
            flash('Предложенный вариант короткой ссылки уже существует.')
            return render_template('yacut.html', form=form)
        url = URLMap(
            original=form.original_linc.data,
            short=short,
        )
        db.session.add(url)
        db.session.commit()
        return render_template(
            'yacut.html',
            form=form,
            short_url=url_for(
                'redirect_to_url_view',
                short=short, _external=True
            )
        )

    return render_template('yacut.html', form=form)


@app.route('/<string:short>')
def redirect_to_url_view(short):
    url = URLMap.query.filter_by(short=short).first_or_404()
    return redirect(url.original)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run()