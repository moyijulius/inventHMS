from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField
from wtforms.fields import DateField  # Updated import for DateField
from wtforms.validators import DataRequired

class PatientForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    contact = StringField('Contact', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Register Patient')

class DoctorForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    specialization = StringField('Specialization', validators=[DataRequired()])
    contact = StringField('Contact', validators=[DataRequired()])
    submit = SubmitField('Add Doctor')

class AppointmentForm(FlaskForm):
    patient_id = SelectField('Patient', coerce=int, validators=[DataRequired()])
    doctor_id = SelectField('Doctor', coerce=int, validators=[DataRequired()])
    appointment_date = DateField('Appointment Date', validators=[DataRequired()])
    submit = SubmitField('Schedule Appointment')

  
