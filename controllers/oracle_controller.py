from flask import session, redirect, url_for, render_template
from database.database import DBIsConnected
from database.migration import Oracle, Organization

def oracle_home():
    username = session.get('username')
    if not username or session.get('user_type') != 'oracle':
        return redirect(url_for('login_route'))
    
    db_instance = DBIsConnected.get_instance()
    session_db = db_instance.get_session()
    oracle_user = session_db.query(Oracle).filter_by(username=username).first()
    session_db.close()
    return render_template('oracle_home.html', oracle=oracle_user)

def manage_organization_registration():
    username = session.get('username')
    if not username or session.get('user_type') != 'oracle':
        return redirect(url_for('login_route'))
    
    db_instance = DBIsConnected.get_instance()
    session_db = db_instance.get_session()
    pending_organizations = session_db.query(Organization).filter_by(status='pending').all()
    session_db.close()
    return render_template('oracle_manage_organization_registration.html', pending_organization=pending_organizations)
