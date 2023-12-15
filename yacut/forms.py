from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import URL, DataRequired, Length, Optional, Regexp


class URLMapForm(FlaskForm):
    original_link = URLField(
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
