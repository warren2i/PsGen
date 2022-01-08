# -*- coding: utf-8 -*-
# app.py
import sys
import base64
from datetime import datetime
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms.fields import TimeField
from wtforms import Form, FieldList, FormField, IntegerField, SelectField, \
    StringField, TextAreaField, SubmitField, DateField, BooleanField, validators
from commands import schedprocess, ping, setdate, copyfile, erase, getfile, Createnewuser, runenccommand, encodecommand


def encode ( line, val2encode ):
    if line['encoding'] is not True:
        # dont encode
        return (val2encode)
    else:
        # encode
        return (runenccommand(encodecommand(val2encode)))


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
        'When Date Time'
    )
    timefield = TimeField(
        'Time',
        default = datetime(1, 1, 1, 0, 0)
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
    timefield = db.Column(db.String(255))
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
            # print(line)
            print(line['timefield'])
            if line['timefield'] is not None:
                timeform = (line['timefield'])
                #    print(timeform)
                line['timefield'] = str(timeform)  ### this is a temp fix.... converted to string, it should work tho
            if line['date'] is not None:
                dateform = (line['date'].strftime(
                    '%m/%d/%Y'))  ## this is how we change the wtforms date format from y-m-d to d/m/y
                line['date'] = dateform
            if line['command_name'] == 'ping':
                result = encode(line, ping(line['url']))
                line['psline'] = result
            if line['command_name'] == 'schedproc':
                datetimevar = (line['date'] + ' ' + line['timefield'])
                result = encode(line, schedprocess(line['taskName'], line['procName'], datetimevar))
                line['psline'] = result
            if line['command_name'] == 'setdate':
                tempval = '"' + str(line['date']) + " " + str(line['timefield']) + '"'
                result = encode(line, setdate(tempval))
                line['psline'] = result
            if line['command_name'] == 'copyfile':
                result = encode(line, copyfile(line['fromlocation'], line['tolocation']))
                line['psline'] = result
            if line['command_name'] == 'erase':
                result = encode(line, erase(line['fileorfolder']))
                line['psline'] = result
            if line['command_name'] == 'getfile':
                result = encode(line, getfile(line['url'], line['tolocation']))
                line['psline'] = result
            if line['command_name'] == 'Createnewuser':
                result = encode(line, Createnewuser(line['userName'], line['password']))
                line['psline'] = result
            #print(line)
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