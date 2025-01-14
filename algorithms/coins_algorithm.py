from flask import flash, redirect, url_for
from database.database import DBIsConnected

def coins_algorithm(co2_emission, co2_limit, organization, session_db):

    if co2_emission > co2_limit:
            malus_coin = int(co2_emission - co2_limit)
            organization.coin -= malus_coin
            if organization.coin < 0:
                flash('CO2 emission exceeds the limit.', 'error_co2')
                if(organization.type == 'carrier'):
                    return redirect(url_for('carrier_menage_product_requests_route'))
                else:
                    return redirect(url_for('create_product_route'))
            if organization.coin >= 0:
                return session_db.add(organization)

    if co2_emission <= co2_limit:
        bonus_coin = int(co2_limit - co2_emission)
        organization.coin += bonus_coin
        return session_db.add(organization) 