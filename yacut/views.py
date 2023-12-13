from flask import render_template, url_for, flash, redirect
from yacut import db, app
from .forms import URLMapForm
from .models import URLMap
from .utils import short_url_generator


@app.route('/', methods=['GET', 'POST'])
def my_index_view():
    form = URLMapForm()
    # print(f'>>>>>{form.custom_id.data}<>{form.original_linc.data}<<<<<')
    if form.validate_on_submit():
        short = form.custom_id.data or short_url_generator()
        print(f'>>>>>{type(short)}<>{form.original_linc.data}<<<<<')
        if short == '':
            short = short_url_generator()
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