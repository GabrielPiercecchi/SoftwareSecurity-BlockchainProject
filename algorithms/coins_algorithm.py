from flask import flash, redirect, url_for
from database.database import DBIsConnected

def coins_algorithm(co2_emission, co2_limit, organization, session_db):

    if co2_emission > co2_limit:
            malus_coin = int(co2_emission - co2_limit)
            organization.coin -= malus_coin
            if organization.coin < 0:
                flash(f'CO2 emission exceeds the limit. You need { (organization.coin*-1) } more coin', 'error_co2')
                return False
                ### redirect(url_for('create_product_route'))
            else:
                session_db.add(organization)
                return True
            
    else:
        bonus_coin = int(co2_limit - co2_emission)
        organization.coin += bonus_coin
        session_db.add(organization) 
        return True