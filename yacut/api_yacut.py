from re import match
from http import HTTPStatus

from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .utils import short_url_generator


@app.route('/api/id/', methods=['POST'])
def add_urlshort():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса', HTTPStatus.BAD_REQUEST)
    if 'url' not in data:
        raise InvalidAPIUsage('\"url\" является обязательным полем!', HTTPStatus.BAD_REQUEST)
    if 'short_link' not in data or data['short_link'] == '':
        data['short_link'] = short_url_generator()
    if URLMap.query.filter_by(short=data['short_link']).first() is not None:
        raise InvalidAPIUsage('Предложенный вариант короткой ссылки уже существует.', HTTPStatus.BAD_REQUEST)
    if not match(r'^[A-Za-z0-9]+$', data['short_link']) or len(data['short_link']) > 16:
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки', HTTPStatus.BAD_REQUEST)
    urlshort = URLMap()
    urlshort.from_dict(data)
    db.session.add(urlshort)
    db.session.commit()
    return jsonify(urlshort.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_urlshort(short_id):
    urlshort = URLMap.query.filter_by(short=short_id).first()
    if not urlshort:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
    data = urlshort.to_dict()
    return jsonify({'url': data['original']}), HTTPStatus.OK
