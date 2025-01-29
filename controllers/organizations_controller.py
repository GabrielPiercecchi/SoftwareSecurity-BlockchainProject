from flask import render_template,  flash, redirect, url_for
from database.database import DBIsConnected
from database.migration import Organization, Employer

def organization_detail(id):
    db_instance = DBIsConnected.get_instance()
    session_db = db_instance.get_session()
    organization = session_db.query(Organization).get(id)

    if not organization:
        session_db.close()
        flash('Organization not found.', 'danger')
        return redirect(url_for('organizations_route'))
    
    employers = session_db.query(Employer).filter_by(id_organization=id).filter_by(status='active').all()
    session_db.close()
    return render_template("organization_detail.html", organization=organization, employers=employers)

def get_all_organizations():
    db_instance = DBIsConnected.get_instance()
    session_db = db_instance.get_session()
    organizations = session_db.query(Organization).filter_by(status='active').all()
    session_db.close()
    return render_template("organizations.html", organizations=organizations)