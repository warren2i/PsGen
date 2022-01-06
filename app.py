# -*- coding: utf-8 -*-
# app.py
import sys
import base64
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import Form, FieldList, FormField, IntegerField, SelectField, \
    StringField, TextAreaField, SubmitField, DateField, BooleanField
from wtforms import validators
from commands import schedprocess, ping, setdate, copyfile, erase, getfile, Createnewuser


class NonValidatingSelectField(SelectField):
    """
    Attempt to make an open ended select multiple field that can accept dynamic
    choices added by the browser.
    """

    def pre_validate ( self, form ):
        pass


class LineForm(Form):
    """Subform.
    CSRF is disabled for this subform (using `Form` as parent class) because
    it is never used by itself.
    """

    command_name = StringField(
        'command_name'
    )
    runner_name = StringField(
        'Runner name',
        # validators=[validators.InputRequired(), validators.Length(max=100)]
    )
    line_time = IntegerField(
        'Line time',
        # validators=[validators.InputRequired(), validators.NumberRange(min=1)]
    )

    arg = SelectField(
        'Args',
        choices = [('None', 'None'), ('-A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')],
        validate_choice = False
    )
    url = StringField(
        'Url'
    )
    dir = StringField(
        'Dir',
    )
    procName = StringField(
        'Process Name',
    )
    taskName = StringField(
        'Sched task name',
    )
    when = StringField(
        'When Date Time',
    )
    delay = StringField(
        'Delay',
        validators = [validators.Length(max = 255)]
    )
    date = DateField(
        'Date',
        format = '%Y-%m-%d'
    )
    userName = StringField(
        'Username',
        validators = [validators.Length(max = 255)]
    )
    password = StringField(
        'password',
        validators = [validators.Length(max = 255)]
    )
    tolocation = StringField(
        'To Location',
        validators = [validators.Length(max = 255)]
    )
    fromlocation = StringField(
        'From Location',
        validators = [validators.Length(max = 255)]
    )
    fileorfolder = StringField(
        'File or Folder Location',
        validators = [validators.Length(max = 255)]
    )
    encoding = BooleanField(
        'Encode command',
        default = "unchecked",
        false_values = None
    )
    psline = StringField(
        'powershell line'
    )


class MainForm(FlaskForm):
    """Parent form."""
    lines = FieldList(
        FormField(LineForm),
        min_entries = 1,
        max_entries = 20
    )


# Create models
db = SQLAlchemy()


class Script(db.Model):
    """Stores scripts."""
    __tablename__ = 'scripts'

    id = db.Column(db.Integer, primary_key = True)


class Line(db.Model):
    """Stores lines of a script."""
    __tablename__ = 'lines'
    command_name = db.Column(db.String(100))
    id = db.Column(db.Integer, primary_key = True)
    script_id = db.Column(db.Integer, db.ForeignKey('scripts.id'))
    fileorfolder = db.Column(db.String(255))
    dir = db.Column(db.String(100))
    url = db.Column(db.String(100))
    runner_name = db.Column(db.String(100))
    line_time = db.Column(db.Integer)
    arg = db.Column(db.String(4))
    delay = db.Column(db.String(255))
    procName = db.Column(db.String(255))
    when = db.Column(db.String(255))
    taskName = db.Column(db.String(255))
    date = db.Column(db.String(255))
    userName = db.Column(db.String(255))
    password = db.Column(db.String(255))
    tolocation = db.Column(db.String(255))
    fromlocation = db.Column(db.String(255))
    encoding = db.Column(db.String(100))
    psline = db.Column(db.String(255))

    # Relationship
    script = db.relationship(
        'Script',
        backref = db.backref('lines', lazy = 'dynamic', collection_class = list)
    )


# Initialize app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'sosecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db.init_app(app)
db.create_all(app = app)


@app.route('/', methods = ['GET', 'POST'])
def index ():
    form = MainForm()
    template_form = LineForm(prefix = 'lines-_-')

    if form.validate_on_submit():
        # Create script
        new_script = Script()
        db.session.add(new_script)
        # print(form.lines.object_data)
        for line in form.lines.data:
            print(line)
            if line['date'] is not None:
                dateform = (line['date'].strftime(
                    '%m/%d/%Y'))  ## this is how we change the wtforms date format from y-m-d to d/m/y
                line['date'] = dateform
            if line['command_name'] == 'ping':
                print(ping(line['url']))
                line['psline'] = ping(line['url'])
            if line['command_name'] == 'schedproc':
                print(schedprocess(line['taskName'], line['procName'], line['date']))
                line['psline'] = schedprocess(line['taskName'], line['procName'], line['date'])
            if line['command_name'] == 'setdate':
                print(setdate(line['date']))
                line['psline'] = setdate(line['date'])
            if line['command_name'] == 'copyfile':
                print(copyfile(line['fromlocation'], line['tolocation']))
                line['psline'] = copyfile(line['fromlocation'], line['tolocation'])
            if line['command_name'] == 'erase':
                print(erase(line['fileorfolder']))
                line['psline'] = erase(line['fileorfolder'])
            if line['command_name'] == 'getfile':
                print(getfile(line['url'], line['tolocation']))
                line['psline'] = getfile(line['url'], line['tolocation'])
            if line['command_name'] == 'Createnewuser':
                print(Createnewuser(line['userName'], line['password']))
                line['psline'] = Createnewuser(line['userName'], line['password'])
            print(line)
            # print(line)
            # print(schedprocess(line['taskName'], line['procName'], dateform))
            # print(runenccommand(encodecommand(schedprocess(line['taskName'], line['procName'], dateform))))
            new_line = Line(**line)

            # Add to script
            new_script.lines.append(new_line)
        db.session.commit()

    scripts = Script.query

    return render_template(
        'index.html',
        form = form,
        scripts = scripts,
        _template = template_form
    )


@app.route('/<script_id>', methods = ['GET'])
def show_script ( script_id ):
    """Show the details of a script."""
    script = Script.query.filter_by(id = script_id).first()

    return render_template(
        'show.html',
        script = script
    )


if __name__ == '__main__':
    app.run()
