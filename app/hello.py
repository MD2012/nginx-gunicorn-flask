""" hello.py """
import os
from flask import Flask, jsonify, render_template, session, redirect, url_for, flash

from flask.ext.bootstrap import Bootstrap

from flask.ext.moment import Moment
from datetime import datetime

from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required

from flask.ext.sqlalchemy import SQLAlchemy

from flask.ext.script import Shell, Manager

from flask.ext.migrate import Migrate, MigrateCommand

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'abcdef'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ONT_TEARDOWN'] = True
bootstrap = Bootstrap(app)
moment = Moment(app)
manager = Manager(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)
    
manager.add_command("shell", Shell(make_context=make_shell_context))

class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')
    
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')
    
    def __repr__(self):
        return '<Role %r>' % self.name
        
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    
    def __repr__(self):
        return '<User %r>' % self.username

@app.route('/', methods=['GET','POST']) 
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
        else:
            session['known'] = True
        
        #old_name = session.get('name')
        #if old_name is not None and old_name != form.name.data:
        #    flash('Looks like you have changed your name!')
        
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
        
    return render_template('index.html', form=form, known=session.get('known', False),
        name=session.get('name'), current_time=datetime.utcnow())
    
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
    app.run(host='0.0.0.0')

#if __name__ == '__main__':
#    app.run(debug=True, host=os.environ['IP'], port=int(os.environ['PORT']))