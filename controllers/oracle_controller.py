from flask import session, redirect, url_for, render_template, flash, request, jsonify
from database.database import DBIsConnected
from database.migration import Oracle, Organization, Employer

def oracle_home():
    username = session.get('username')
    if not username or session.get('user_type') != 'oracle':
        return redirect(url_for('login_route'))
    
    db_instance = DBIsConnected.get_instance()
    session_db = db_instance.get_session()
    oracle_user = session_db.query(Oracle).filter_by(username=username).first()
    session_db.close()
    return render_template('oracle_home.html', oracle=oracle_user)

def view_organization_inactive():
    username = session.get('username')
    if not username or session.get('user_type') != 'oracle':
        return redirect(url_for('login_route'))
    
    db_instance = DBIsConnected.get_instance()
    session_db = db_instance.get_session()
    pending_organizations = session_db.query(Organization).filter_by(status='inactive').all()
    session_db.close()
    return render_template('oracle_view_organization_inactive.html', pending_organizations=pending_organizations)

def manage_organization_registration(organization_id):
    username = session.get('username')
    if not username or session.get('user_type') != 'oracle':
        return redirect(url_for('login_route'))
    
    db_instance = DBIsConnected.get_instance()
    session_db = db_instance.get_session()
    organization = session_db.query(Organization).filter_by(id=organization_id, status='inactive').first()
    if not organization:
        flash('Organization not found or not inactive.', 'danger')
        return redirect(url_for('view_organization_inactive_route'))
    
    employers = session_db.query(Employer).filter_by(id_organization=organization_id).all()
    session_db.close()
    return render_template('oracle_manage_organization_registration.html', organization=organization, employers=employers)

def approve_organization(organization_id):
    if request.method == 'POST':
        db_instance = DBIsConnected.get_instance()
        session_db = db_instance.get_session()
        
        organization = session_db.query(Organization).get(organization_id)
        if organization:
            organization.status = 'active'
            session_db.commit()
            message = 'Organization approved and activated.'
            flash(message, 'success')
        else:
            message = 'Organization not found.'
            flash(message, 'danger')
        
        session_db.close()
        return jsonify({'message': message, 'redirect_url': url_for('view_organization_inactive_route')})

def reject_organization(organization_id):
    if request.method == 'POST':
        db_instance = DBIsConnected.get_instance()
        session_db = db_instance.get_session()
        
        organization = session_db.query(Organization).get(organization_id)
        if organization:
            # Elimina prima gli employer associati
            session_db.query(Employer).filter_by(id_organization=organization_id).delete()
            session_db.delete(organization)
            session_db.commit()
            message = 'Organization registration rejected and deleted.'
            flash(message, 'success')
        else:
            message = 'Organization not found.'
            flash(message, 'danger')
        
        session_db.close()
        return jsonify({'message': message, 'redirect_url': url_for('view_organization_inactive_route')})