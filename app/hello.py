""" hello.py """
import os
from flask import Flask, jsonify, render_template, session, redirect, url_for, flash

from flask.ext.bootstrap import Bootstrap

from flask.ext.moment import Moment
from datetime import datetime

from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'abcdef'
bootstrap = Bootstrap(app)
moment = Moment(app)

class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET','POST']) 
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'), current_time=datetime.utcnow())
    
@app.errorhandler(404) 
def page_not_found(e):
    return render_template('404.html'), 404
    
@app.route('/jinjademo') 
def jinjademo():
    mydict = {'key1':' This is a test <dict> key incl. none <b>escaped&nbsp;values</b>! '}
    mylist = list(range(100))
    myint = 3
    comments = ['comment 1','comment 2','comment 3']
    return render_template('jinjademo.html', 
        mydict=mydict,
        mylist=mylist,
        myint=myint,
        comments=comments
    )
    
@app.route('/hello')
def hello():
    return jsonify({
        'hello': 'letstest',
        'and': 'sth else234',
        'bha': 'test234'
    })

if __name__ == '__main__':
    app.run(
        debug=True,
        host=os.environ['IP'],
        port=int(os.environ['PORT']))