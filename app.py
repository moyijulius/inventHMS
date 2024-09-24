from flask import Flask, render_template, redirect, url_for, request, flash
from models import db, Patient, Doctor, Appointment
from forms import DoctorForm, PatientForm, AppointmentForm
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospital.db'
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['WTF_CSRF_ENABLED'] = True
app.config['WTF_CSRF_SECRET_KEY'] = 'your-secret-key'

db.init_app(app)
migrate = Migrate(app, db)

# Enable CSRF protection
csrf = CSRFProtect(app)

# Error handler for 404
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

# Route for home page
@app.route('/')
def index():
    return render_template('index.html')

# Route for registering a patient
@app.route('/register-patient', methods=['GET', 'POST'])
def register_patient():
    form = PatientForm()
    if form.validate_on_submit():
        new_patient = Patient(
            name=form.name.data,
            age=form.age.data,
            contact=form.contact.data,
            address=form.address.data
        )
        db.session.add(new_patient)
        db.session.commit()
        flash('Patient Registered Successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('register_patient.html', form=form)

# Route to discharge a patient
@app.route('/discharge_patient/<int:id>', methods=['POST'])
def discharge_patient(id):
    patient = Patient.query.get_or_404(id)
    db.session.delete(patient)
    db.session.commit()
    flash('Patient successfully discharged.', 'success')
    return redirect(url_for('index'))

# Route for deleting a doctor
@app.route('/delete-doctor/<int:doctor_id>', methods=['GET'])
def delete_doctor(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    
    # Check if the doctor has any scheduled appointments
    if Appointment.query.filter_by(doctor_id=doctor.id).count() > 0:
        flash('Cannot delete doctor with scheduled appointments!', 'danger')
        return redirect(url_for('doctors'))

    db.session.delete(doctor)
    db.session.commit()
    flash('Doctor deleted successfully!', 'success')
    return redirect(url_for('doctors'))

# Route for searching a patient by ID
@app.route('/search-patient')
def search_patient():
    patient_id = request.args.get('id')
    if patient_id:
        patient = Patient.query.filter_by(id=patient_id).first()
        if patient:
            return render_template('patients_table.html', patients=[patient])
        else:
            flash('Patient not found!', 'danger')
            return render_template('patients_table.html', patients=[])
    return redirect(url_for('index'))

# Route for searching doctors
@app.route('/search-doctor')
def search_doctor():
    doctor_id = request.args.get('id')
    if doctor_id:
        doctor = Doctor.query.filter_by(id=doctor_id).first()
        if doctor:
            return render_template('doctors.html', doctors=[doctor])
        else:
            flash('Doctor not found!', 'danger')
            return render_template('doctors.html', doctors=[])
    return redirect(url_for('doctors'))

# Route for listing doctors
@app.route('/doctors')
def doctors():
    doctor_list = Doctor.query.all()
    return render_template('doctors.html', doctors=doctor_list)

# Route to add a new doctor
@app.route('/add-doctor', methods=['GET', 'POST'])
def add_doctor():
    form = DoctorForm()
    if form.validate_on_submit():
        new_doctor = Doctor(
            name=form.name.data,
            specialization=form.specialization.data,
            contact=form.contact.data
        )
        db.session.add(new_doctor)
        db.session.commit()
        flash('Doctor added successfully!', 'success')
        return redirect(url_for('doctors'))
    
    return render_template('add_doctor.html', form=form)

# Route for updating doctor details
@app.route('/update-doctor/<int:doctor_id>', methods=['GET', 'POST'])
def update_doctor(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    form = DoctorForm(obj=doctor)
    
    if form.validate_on_submit():
        doctor.name = form.name.data
        doctor.specialization = form.specialization.data
        doctor.contact = form.contact.data
        db.session.commit()
        flash('Doctor details updated successfully!', 'success')
        return redirect(url_for('doctors'))

    return render_template('add_doctor.html', form=form, doctor=doctor)

# Route for fetching registered patients
@app.route('/get-patients')
def get_patients():
    patients = Patient.query.all()
    return render_template('patients_table.html', patients=patients)

# Route for updating patient details
@app.route('/update-patient/<int:id>', methods=['GET', 'POST'])
def update_patient(id):
    patient = Patient.query.get_or_404(id)
    form = PatientForm(obj=patient)
    
    if form.validate_on_submit():
        patient.name = form.name.data
        patient.age = form.age.data
        patient.contact = form.contact.data
        patient.address = form.address.data
        db.session.commit()
        flash('Patient details updated successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('register_patient.html', form=form)

# Route for scheduling an appointment
@app.route('/appointment', methods=['GET', 'POST'])
def appointment():
    form = AppointmentForm()
    form.patient_id.choices = [(p.id, p.name) for p in Patient.query.all()]
    form.doctor_id.choices = [(d.id, d.name) for d in Doctor.query.all()] 

    if form.validate_on_submit():
        # Check if the patient already has an appointment with the same doctor on the same date
        existing_appointment = Appointment.query.filter_by(
            patient_id=form.patient_id.data,
            doctor_id=form.doctor_id.data,
            appointment_date=form.appointment_date.data
        ).first()

        if existing_appointment:
            flash('This patient already has an appointment with this doctor on the selected date.', 'danger')
        else:
            new_appointment = Appointment(
                patient_id=form.patient_id.data,
                doctor_id=form.doctor_id.data,
                appointment_date=form.appointment_date.data
            )
            db.session.add(new_appointment)
            db.session.commit()
            flash('Appointment Scheduled Successfully!', 'success')
            return redirect(url_for('index'))

    return render_template('appointment.html', form=form)
# Route for editing an appointment
@app.route('/edit-appointment/<int:appointment_id>', methods=['GET', 'POST'])
def edit_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    form = AppointmentForm(obj=appointment)

    form.patient_id.choices = [(p.id, p.name) for p in Patient.query.all()]
    form.doctor_id.choices = [(d.id, d.name) for d in Doctor.query.all()]

    if form.validate_on_submit():
        appointment.patient_id = form.patient_id.data
        appointment.doctor_id = form.doctor_id.data
        appointment.appointment_date = form.appointment_date.data
        db.session.commit()
        flash('Appointment updated successfully!', 'success')
        return redirect(url_for('view_appointments'))

    return render_template('appointment.html', form=form, appointment=appointment)
# Route for discharging an appointment
@app.route('/discharge-appointment/<int:appointment_id>', methods=['POST'])
def discharge_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    db.session.delete(appointment)
    db.session.commit()
    flash('Appointment discharged successfully!', 'success')
    return redirect(url_for('view_appointments'))


# Route to view all scheduled appointments
@app.route('/view_appointments')
def view_appointments():
    appointments = Appointment.query.all()
    return render_template('appointment_table.html', appointments=appointments)


if __name__ == '__main__':
    app.run(debug=True)
