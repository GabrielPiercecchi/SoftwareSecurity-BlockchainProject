from flask import render_template
from database.database import DBIsConnected
from database.migration import Organization, Employer

def organization_detail(id):
    db_instance = DBIsConnected.get_instance()
    session = db_instance.get_session()
    organization = session.query(Organization).get(id)
    employers = session.query(Employer).filter_by(id_organization=id).all()
    session.close()
    return render_template("organization_detail.html", organization=organization, employers=employers)

def get_all_organizations():
    db_instance = DBIsConnected.get_instance()
    session = db_instance.get_session()
    organizations = session.query(Organization).all()
    session.close()
    return render_template("organizations.html", organizations=organizations)