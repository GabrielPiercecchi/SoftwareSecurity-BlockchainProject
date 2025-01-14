from flask import render_template, request, redirect, url_for, flash, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, RadioField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo
from werkzeug.security import check_password_hash, generate_password_hash
from database.database import DBIsConnected
from database.migration import Oracle, Employer, Organization

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()], render_kw={"placeholder": "Username"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Password"})

class OrganizationForm(FlaskForm):
    org_name = StringField('Organization Name', validators=[DataRequired()], render_kw={"placeholder": "Organization Name"})
    org_email = StringField('Organization Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Organization@Email"})
    org_address = StringField('Address', validators=[DataRequired()], render_kw={"placeholder": "Address"})
    org_city = StringField('City', validators=[DataRequired()], render_kw={"placeholder": "City"})
    org_cap = StringField('CAP', validators=[DataRequired()], render_kw={"placeholder": "CAP"})
    org_telephone = StringField('Telephone', validators=[DataRequired()], render_kw={"placeholder": "Telephone"})
    org_partita_iva = StringField('Partita IVA', validators=[DataRequired()], render_kw={"placeholder": "Partita IVA"})
    org_ragione_sociale = StringField('Ragione Sociale', validators=[DataRequired()], render_kw={"placeholder": "Ragione Sociale"})
    org_type = RadioField('Type', choices=[('farmer', 'Farmer'), ('seller', 'Seller'), ('producer', 'Producer'), ('carrier', 'Carrier')], validators=[DataRequired()], default='farmer')
    org_description = TextAreaField('Description', validators=[DataRequired()], render_kw={"placeholder": "Description"})

class EmployerForm(FlaskForm):
    emp_username = StringField('Username', validators=[DataRequired()], render_kw={"placeholder": "Username"})
    emp_password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Password"})
    emp_confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('emp_password', message='Passwords must match' )], render_kw={"placeholder": "Confirm Password"})
    emp_name = StringField('Name', validators=[DataRequired()], render_kw={"placeholder": "Name"})
    emp_surname = StringField('Surname', validators=[DataRequired()], render_kw={"placeholder": "Surname"})
    emp_email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Employer@Email"})

class AddEmployersForm(FlaskForm):
    organization = SelectField('Organization', choices=[], validators=[DataRequired()])
    emp_username = StringField('Username', validators=[DataRequired()], render_kw={"placeholder": "Username"})
    emp_password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Password"})
    emp_confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('emp_password', message='Passwords must match' )], render_kw={"placeholder": "Confirm Password"})
    emp_name = StringField('Name', validators=[DataRequired()], render_kw={"placeholder": "Name"})
    emp_surname = StringField('Surname', validators=[DataRequired()], render_kw={"placeholder": "Surname"})
    emp_email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Employer@Email"})


def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data.lower()
        password = form.password.data
        
        db_instance = DBIsConnected.get_instance()
        session_db = db_instance.get_session()
        
        # Controlla nella tabella Oracle
        oracle_user = session_db.query(Oracle).filter_by(username=username).first()
        
        # Controlla nella tabella Employer se non trovato in Oracle
        employer = None
        if not oracle_user:
            employer = session_db.query(Employer).filter_by(username=username).first()
        
        # Verifica la password
        if ((oracle_user and check_password_hash(oracle_user.password, password)) 
            or (employer and check_password_hash(employer.password, password))):
            if ((oracle_user) or (employer.status == 'active')):
            # Login riuscito
                print('Valid username and password')
                session['logged_in'] = True
                session['username'] = username
                if employer:
                    session['user_type'] = 'employer'
                else:
                    session['user_type'] = 'oracle'
                session_db.close()
                return redirect(url_for('home_route'))
            else:
                # Account disabilitato
                session_db.close()
                flash('Account not yet enabled')
                return render_template('login.html', form=form)
        else:
            # Login fallito
            session_db.close()
            flash('Invalid username or password')
            return render_template('login.html', form=form)
    
    return render_template('login.html', form=form)

def logout():
    # Rimuove tutte le chiavi di sessione rilevanti per l'autenticazione
    session.pop('logged_in', None)
    session.pop('username', None)
    # Passa un messaggio di successo al template
    return redirect(url_for('home_route'))

def signup_form():
    org_form = OrganizationForm()
    emp_form = EmployerForm()
    return render_template('signup.html', org_form=org_form, emp_form=emp_form)

def signup():
    org_form = OrganizationForm(request.form)
    emp_form = EmployerForm(request.form)

    if request.method == 'POST' and org_form.validate_on_submit() and emp_form.validate_on_submit():
        db_instance = DBIsConnected.get_instance()
        session_db = db_instance.get_session()

        other_organizations = session_db.query(Organization).all()

        if any(org_form.org_email.data.lower() == o.email.lower() for o in other_organizations):
            flash('Organization email already in use', 'wrong_org_email')
            session_db.close()
            return signup_form()
        
        if any(org_form.org_partita_iva.data == o.partita_iva for o in other_organizations):
            flash('Partita IVA already in use', 'wrong_org_partita_iva')
            session_db.close()
            return signup_form()

        org_name = org_form.org_name.data
        org_email = org_form.org_email.data.lower()
        org_address = org_form.org_address.data
        org_city = org_form.org_city.data
        org_cap = org_form.org_cap.data
        org_telephone = org_form.org_telephone.data
        org_partita_iva = org_form.org_partita_iva.data
        org_ragione_sociale = org_form.org_ragione_sociale.data
        org_type = org_form.org_type.data
        org_description = org_form.org_description.data

        emp_usernames = request.form.getlist('emp_username')
        emp_passwords = request.form.getlist('emp_password')
        emp_names = request.form.getlist('emp_name')
        emp_surnames = request.form.getlist('emp_surname')
        emp_emails = request.form.getlist('emp_email')

        other_emp = session_db.query(Employer).all()

        if any(emp_username.lower() in [e.username.lower() for e in other_emp] for emp_username in emp_usernames):
            flash('Username already in use', 'wrong_emp_username')
            session_db.close()
            return signup_form()
        
        if any(emp_email.lower() in [e.email.lower() for e in other_emp] for emp_email in emp_emails):
            flash('Email already in use', 'wrong_emp_email')
            session_db.close()
            return signup_form()

        try:
            # Crea l'organizzazione
            new_org = Organization(
                name=org_name,
                email=org_email,
                address=org_address,
                city=org_city,
                cap=org_cap,
                telephone=org_telephone,
                partita_iva=org_partita_iva,
                ragione_sociale=org_ragione_sociale,
                type=org_type,
                status='inactive',
                description=org_description,
                coin=100.0
            )
            session_db.add(new_org)
            session_db.commit()
            print(new_org)

            # Crea gli impiegati
            try:
                # Crea gli impiegati
                for i in range(len(emp_usernames)):
                    new_emp = Employer(
                        username=emp_usernames[i],
                        password=generate_password_hash(emp_passwords[i]),
                        name=emp_names[i],
                        surname=emp_surnames[i],
                        email=emp_emails[i].lower(),
                        status='inactive',
                        id_organization=new_org.id  # Associa l'impiegato all'organizzazione appena creata
                    )
                    session_db.add(new_emp)
                    print(emp_names[i])
                    print(new_emp)
                
                session_db.commit()
            except Exception as e:
                print(f'Error: {e}', 'error')
            
            session_db.commit()
            session_db.close()
        except Exception as e:
            session_db.rollback()
            print(f'Error: {e}', 'error')
        finally:
            session_db.close()

        return redirect(url_for('home_route'))

    return signup_form()

def add_employers_to_existing_org():
    db_instance = DBIsConnected.get_instance()
    session_db = db_instance.get_session()
    organizations = session_db.query(Organization).all()
    session_db.close()

    form = AddEmployersForm()
    form.organization.choices = [(org.id, f"{org.id} - {org.name} - {org.type}") for org in organizations]

    if request.method == 'POST' and form.validate():
        organization_id = form.organization.data
        emp_usernames = request.form.getlist('emp_username')
        emp_passwords = request.form.getlist('emp_password')
        emp_names = request.form.getlist('emp_name')
        emp_surnames = request.form.getlist('emp_surname')
        emp_emails = request.form.getlist('emp_email')

        session_db = db_instance.get_session()

        other_emp = session_db.query(Employer).all()

        if any(emp_username.lower() in [e.username.lower() for e in other_emp] for emp_username in emp_usernames):
            flash('Username already in use', 'wrong_emp_username')
            session_db.close()
            return render_template('add_employers.html', form=form, organizations=organizations)
        
        if any(emp_email.lower() in [e.email.lower() for e in other_emp] for emp_email in emp_emails):
            flash('Email already in use', 'wrong_emp_email')
            session_db.close()
            return render_template('add_employers.html', form=form, organizations=organizations)

        try:
            for i in range(len(emp_usernames)):
                new_emp = Employer(
                    username=emp_usernames[i],
                    password=generate_password_hash(emp_passwords[i]),
                    name=emp_names[i],
                    surname=emp_surnames[i],
                    email=emp_emails[i],
                    id_organization=organization_id
                )
                session_db.add(new_emp)
            
            session_db.commit()
            print('Employers added successfully!')
        except Exception as e:
            session_db.rollback()
            print(f'Error: {str(e)}')
        finally:
            session_db.close()

        return redirect(url_for('home_route'))

    return render_template('add_employers.html', form=form, organizations=organizations)

