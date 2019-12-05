from flask import render_template, flash, redirect, url_for
from app import app, db
from app.forms import LinkForm
from app.models import Links
import short_url

@app.route('/', methods=['GET', 'POST'])
def index():
    form = LinkForm()
    if form.validate_on_submit():
        link = Links(longLink=form.longLink.data) # prepare data
        db.session.add(link)
        db.session.flush() # get insert id
        link.generateShortLink(link.id)
        slink = url_for('redirect', shortUrl=link.shortLink, _external=True)
        db.session.commit()
        return render_template('index.html', link=slink)
    return render_template('index.html', title='Home', form=form)

@app.route('/r/<shortUrl>')
def redirect(shortUrl):
    try:
        id = short_url.decode_url(shortUrl)
        longUrl = Links.query.get_or_404(id)
        return render_template('redirect.html', title='Redirecting', link=longUrl.longLink)
    except:
        errorMsg = "Invalid URL"
        return render_template('redirect.html', title='Page Not Found', msg=errorMsg)

@app.route('/getall')
def getall():
    links = Links.query.all()
    return render_template('links.html', title='Generated Links', links=links)