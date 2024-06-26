from flask import flash, redirect, render_template, url_for

from yacut import app, db

from .forms import URLMapForm
from .models import URLMap
from .utils import short_url_generator


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if not form.validate_on_submit():
        return render_template('yacut.html', form=form)
    short = form.custom_id.data or short_url_generator()
    if URLMap.query.filter_by(short=short).first():
        flash('Предложенный вариант короткой ссылки уже существует.')
        return render_template('yacut.html', form=form)
    url = URLMap(
        original=form.original_link.data,
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


@app.route('/<string:short>')
def redirect_to_url_view(short):
    url = URLMap.query.filter_by(short=short).first_or_404()
    return redirect(url.original)
