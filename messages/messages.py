############################################
# auth_messages.py messages
############################################

# Login messages
LOGIN_ATTEMPTS_EXCEEDED = 'Too many login attempts. Please try again in 30 seconds.'
INVALID_USERNAME_OR_PASSWORD = 'Invalid username or password'
ACCOUNT_NOT_ENABLED = 'Account not yet enabled'
LOGIN_ERROR = 'An error occurred during login. Please try again later.'

# Logout messages
LOGOUT_SUCCESS = 'You have been logged out successfully.'

# Signup messages
ORG_EMAIL_IN_USE = 'Organization email already in use'
ORG_PARTITA_IVA_IN_USE = 'Partita IVA already in use'
EMP_USERNAME_IN_USE = 'Username already in use'
EMP_EMAIL_IN_USE = 'Email already in use'
SIGNUP_SUCCESS = 'Signup process completed successfully.'
SIGNUP_ERROR = 'An error occurred during signup. Please try again later.'

# Add Employers messages
ADD_EMPLOYERS_USERNAME_IN_USE = 'Username already in use'
ADD_EMPLOYERS_EMAIL_IN_USE = 'Email already in use'
ADD_EMPLOYERS_SUCCESS = 'Employers added successfully!'
ADD_EMPLOYERS_ERROR = 'An error occurred while adding employers. Please try again later.'

############################################
# coin_requests_controller.py messages
############################################

# Coin Requests messages
REQUEST_ID_REQUIRED = 'Request ID is required'
NOT_ENOUGH_COINS = 'Not enough Coins'
COIN_REQUEST_ACCEPTED = 'Coin request accepted'
ERROR_ACCEPTING_COIN_REQUEST = 'Error accepting coin request'

############################################
# deliveries_controller.py messages
############################################

# General messages
LOGIN_REQUIRED = 'You must be logged in to access this page.'

############################################
# employers_controller.py messages
############################################

# Riusato LOGIN_REQUIRED

# Employer messages
EMPLOYER_NOT_FOUND = 'Employer not found.'
USERNAME_ALREADY_IN_USE = 'Username already in use'
EMAIL_ALREADY_IN_USE = 'Email already in use'
DATA_UPDATED_SUCCESSFULLY = 'Data updated successfully!'
FAILED_TO_UPDATE_PERSONAL_DATA = 'Failed to update personal data.'

############################################
# oracle_controller.py messages
############################################

# Riusato LOGIN_REQUIRED

# Oracle messages
AMOUNT_EXCEEDS_AVAILABLE_COINS = 'Amount exceeds available coins.'
INSUFFICIENT_COINS = 'Insufficient coins for transfer. The organization must retain at least 20 coins.'
COINS_TRANSFERRED_SUCCESSFULLY = 'Coins transferred successfully!'
FAILED_TO_TRANSFER_COINS = 'Failed to transfer coins on blockchain.'
ORGANIZATION_NOT_FOUND_OR_NOT_INACTIVE = 'Organization not found or not inactive.'
ORGANIZATION_APPROVED = 'Organization and associated employers approved and activated.'
ORGANIZATION_NOT_FOUND = 'Organization not found.'
ORGANIZATION_REJECTED = 'Organization registration rejected and deleted.'
EMPLOYER_NOT_FOUND_OR_NOT_INACTIVE = 'Employer not found or not inactive.'
EMPLOYER_APPROVED = 'Employer approved and activated.'
EMPLOYER_REJECTED = 'Employer registration rejected and deleted.'
EMPLOYER_NOT_FOUND = 'Employer not found.'

############################################
# organizations_controller.py messages
############################################

# Organization messages
ORGANIZATION_NOT_FOUND = 'Organization not found.'

############################################
# product_requests_controller.py messages
############################################

# Riusato LOGIN_REQUIRED

# Product Request messages
PRODUCT_NOT_FOUND = 'Product not found.'
UNAUTHORIZED_ACCESS = 'Unauthorized access.'
REQUESTED_QUANTITY_EXCEEDS_AVAILABLE = 'Requested quantity exceeds available quantity.'
PRODUCT_REQUEST_CREATED_SUCCESSFULLY = 'Product request created successfully.'
REQUEST_ID_REQUIRED = 'Request ID is required.'
PRODUCT_REQUEST_NOT_FOUND = 'Product request not found.'
PRODUCT_REQUEST_DENIED_SUCCESSFULLY = 'Product request denied successfully.'
INSUFFICIENT_PRODUCT_QUANTITY = 'Insufficient product quantity.'
PRODUCT_REQUEST_ACCEPTED_SUCCESSFULLY = 'Product request accepted successfully.'
CO2_EMISSION_EXCEEDS_LIMIT = 'CO2 emission exceeds the limit.'
DELIVERY_CREATED_SUCCESSFULLY = 'Delivery created successfully.'
ERROR_OCCURRED = 'An error occurred: {}'

############################################
# products_controller.py messages
############################################

# Riusato LOGIN_REQUIRED

# Product messages
PRODUCT_NOT_FOUND = 'Product not found.'
UNAUTHORIZED_ACCESS = 'Unauthorized access.'
PRODUCT_UPDATED_SUCCESSFULLY = 'Product updated successfully!'
FAILED_TO_UPDATE_PRODUCT = 'Failed to update product.'
FAILED_TO_ADD_PRODUCT = 'Failed to add product: intero fuori dall\'intervallo'
FAILED_TO_REGISTER_PRODUCT_ORIGIN = 'Failed to register product origin on blockchain.'
ORIGIN_PRODUCT_REQUIRED = 'At least one origin product must be selected.'

############################################
# coins_algorithm.py messages
############################################

# Coin Algorithm messages
CONTRACT_ADDRESS_FILE_NOT_FOUND = 'Contract address file not found. Ensure the contract is deployed.'
INVALID_CONTRACT_ADDRESS = 'Invalid contract address: {}'
ERROR_GETTING_COINS = 'Error getting coins from blockchain: {}'
COIN_DISCREPANCY_DETECTED = 'Coin discrepancy detected between database and blockchain'
CO2_EMISSION_EXCEEDS_LIMIT = 'CO2 emission exceeds the limit. You need {} more coin'
TRANSACTION_FAILED = 'Transaction failed: CO2 emission exceeds the limit. You need {} more coin'
ERROR_IN_COINS_ALGORITHM = 'An error occurred: {}'
FAILED_TO_UPDATE_COINS_PROVIDING = 'Failed to update coins for providing organization'
FAILED_TO_UPDATE_COINS_REQUESTING = 'Failed to update coins for requesting organization'
ERROR_UPDATING_COINS = 'Error updating organization coins on blockchain: {}'
ERROR_GETTING_TRANSACTIONS = 'Error while getting transactions: {}'

