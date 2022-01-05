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


def schedprocess ( name, proc, when ):
    """https://docs.microsoft.com/en-us/powershell/module/scheduledtasks/new-scheduledtask?view=windowsserver2022-ps
    name = schedule task name
    proc = process name ie calc.exe
    when = -At <DateTime>,-AtLogOn, -AtStartup, -Daily, -DaysInterval [<Int32>], -Once, -RandomDelay [num],

    idle info The Task Scheduler service will check if the computer is in an idle state every 15 minutes. A computer is considered to be in an idle state when a screen saver is running. If a screen saver is not running, then the computer is considered to be in an idle state if there is 0% CPU usage and 0% disk input or output for 90% of the past fifteen minutes and if there is no keyboard or mouse input during this period of time. Once the Task Scheduler service detects that the computer is in an idle state, the service only waits for user input to mark the end of the idle state.
    """
    return (
            'Register-ScheduledTask ' + name + ' -InputObject (New-ScheduledTask -Action (New-ScheduledTaskAction -Execute "' + proc + '") -Trigger (New-ScheduledTaskTrigger -At ' + when + ' -Once) -Settings (New-ScheduledTaskSettingsSet))')


def runenccommand ( enc ):
    """runs encoded commands in powershell
    Useage example // runenccommand(encodecommand('ping google.com')) to generate // powershell -E cABpAG4AZwAgAGcAbwBvAGcAbABlAC4AYwBvAG0A
    """
    return ("powershell -E '" + enc + "'")


def encodecommand ( command ):
    """encodes a powershell command"""
    return (base64.b64encode(command.encode("UTF-16LE", "ignore"))).decode('utf-8')


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
        'Url',
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
        'To Location',
        validators = [validators.Length(max = 255)]
    )
    encoding = BooleanField(
        'Encode command',
        default = "unchecked",
        false_values = None
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

    id = db.Column(db.Integer, primary_key = True)
    script_id = db.Column(db.Integer, db.ForeignKey('scripts.id'))
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
        print(form.lines.object_data)
        for line in form.lines.data:
            if line['date'] is not None:
                dateform = (line['date'].strftime(
                    '%m/%d/%Y'))  ## this is how we change the wtforms date format from y-m-d to d/m/y
                line['date'] = dateform
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
