from flask import render_template, request, redirect, url_for, flash, session
from database.database import DBIsConnected
from database.migration import Employer, Organization

def employer_home():
    username = session.get('username')
    if not username:
        return redirect(url_for('login_route'))
    
    db_instance = DBIsConnected.get_instance()
    session_db = db_instance.get_session()
    employer = session_db.query(Employer).filter_by(username=username).first()
    organization = session_db.query(Organization).filter_by(id=employer.id_organization).first()
    session_db.close()
    return render_template('employer_home.html', employer=employer, organization=organization)



