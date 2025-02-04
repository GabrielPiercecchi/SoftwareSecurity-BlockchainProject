from flask import render_template, flash, redirect, url_for
from database.migration import Organization
from utilities.utilities import get_db_session, get_organization_by_id, get_employers_by_organization_id
from messages.messages import ORGANIZATION_NOT_FOUND

def organization_detail(id):
    # Visualizza i dettagli di una specifica organizzazione
    session_db = get_db_session()
    organization = get_organization_by_id(session_db, id)

    if not organization or organization.status == 'inactive':
        session_db.close()
        flash(ORGANIZATION_NOT_FOUND, 'danger')
        return redirect(url_for('organizations_route'))
    
    employers = get_employers_by_organization_id(session_db, id)
    session_db.close()
    return render_template("organization_detail.html", organization=organization, employers=employers)

def get_all_organizations():
    # Visualizza tutte le organizzazioni attive
    session_db = get_db_session()
    organizations = session_db.query(Organization).filter_by(status='active').all()
    session_db.close()
    return render_template("organizations.html", organizations=organizations)