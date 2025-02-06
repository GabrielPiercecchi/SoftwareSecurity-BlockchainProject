# SoftwareSecurity-BlockchainProject
<p align="center">
  <img src="https://github.com/user-attachments/assets/3bef384b-b867-4595-ab94-6fdee39d7dc7" alt="blockchain-filiera-alimentare" width="300">
</p>

[![Python](https://img.shields.io/badge/python-%230376D6?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-%23000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/en/stable/)
[![Jinja](https://img.shields.io/badge/Jinja-%23000000?style=for-the-badge&logo=jinja&logoColor=white)](https://jinja.palletsprojects.com/en/stable/templates/)
[![VSCode](https://img.shields.io/badge/VSCode-%23007ACC?style=for-the-badge&logo=visualstudiocode&logoColor=white)](https://code.visualstudio.com/)
[![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)](https://it.wikipedia.org/wiki/HTML)
[![GitHub](https://img.shields.io/badge/GitHub-%23121011?style=for-the-badge&logo=github&logoColor=white)](https://github.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-%23336791?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-%232496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Docker Compose](https://img.shields.io/badge/Docker%20Compose-%23FF69B4?style=for-the-badge&logo=docker&logoColor=white)](https://docs.docker.com/compose/)
[![Hyperledger Besu](https://img.shields.io/badge/Hyperledger%20Besu-%230072C6?style=for-the-badge&logo=hyperledger&logoColor=white)](https://besu.hyperledger.org/)
[![Grafana](https://img.shields.io/badge/Grafana-%23F46800?style=for-the-badge&logo=grafana&logoColor=white)](https://grafana.com/)
[![Ethereum](https://img.shields.io/badge/Ethereum-3C3C3D?style=for-the-badge&logo=Ethereum&logoColor=white)](https://ethereum.org/it/)
[![Overleaf](https://img.shields.io/badge/Overleaf-%2300C2B9?style=for-the-badge&logo=overleaf&logoColor=white)](https://it.overleaf.com)
[![Gunicorn](https://img.shields.io/badge/gunicorn-%298729.svg?style=for-the-badge&logo=gunicorn&logoColor=white)](https://gunicorn.org/)
[![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)](https://nginx.org/en/)
[![Solidity](https://img.shields.io/badge/Solidity-%23363636.svg?style=for-the-badge&logo=solidity&logoColor=white)](https://soliditylang.org/)
[![MetaMask](https://img.shields.io/badge/MetaMask-ED8B00?style=for-the-badge&logo=metamask&logoColor=white)](https://metamask.io/)

- [SoftwareSecurity-BlockchainProject](#softwaresecurity-blockchainproject)
  - [Introduction 📖](#introduction-)
    - [Main Features 🌟](#main-features-)
    - [How it Works ⚙️](#how-it-works-️)
    - [Technologies Used 🧩](#technologies-used-)
    - [Codacy Evaluation 📊](#codacy-evaluation-)
  - [Gettin Started 🗂️](#gettin-started-️)
    - [Prerequisites 📋](#prerequisites-)
    - [Installation 🛠️](#installation-️)
      - [Linux 🐧](#linux-)
      - [Windows 🪟](#windows-)
      - [MacOS 🍏](#macos-)
  - [Usage 🚀](#usage-)
    - [Running the Server 🖥️](#running-the-server-️)
      - [Database Setup 🗄️](#database-setup-️)
    - [Troubleshooting 🔧](#troubleshooting-)
      - [Creating a Super User 👤](#creating-a-super-user-)
    - [Node Explorer 🔍](#node-explorer-)
    - [Logs 📜](#logs-)
  - [Credits 👯‍♂️](#credits-️)

## Introduction 📖

This application leverages blockchain technology to track products throughout the supply chain while monitoring and recording the Co<sub>2</sub> emissions generated at each stage. By ensuring data integrity, transparency, and security, the system helps businesses and consumers make informed decisions regarding sustainability.

### Main Features 🌟

- *Product Tracking*: Monitors a product's journey from origin to final destination.

- *Co<sub>2</sub> Emissions Calculation*: Records emissions generated at each step of the supply chain.

- *Blockchain Integration*: Ensures data integrity and security using a private blockchain network.

- *Smart Contracts*: Automates verification and validation of product movement and emissions data.

- *Audit & Reporting*: Generates reports on Co<sub>2</sub> emissions for compliance and sustainability tracking.

### How it Works ⚙️

The application begins with a home page where users can observe various companies and products, and check their provenance. Once authenticated, employers, carriers, and oracles can log in using secure methods. Employers can manage products within their organization, creating, updating, and viewing product details. Organizations can request products from others, and these requests are meticulously tracked and managed.

*Oracles* play a crucial role by facilitating coin transfers between organizations, ensuring smooth transactions. Every product movement and coin transfer is recorded on the blockchain, providing an immutable and transparent ledger. The system also calculates and records CO<sub>2</sub> emissions for each product movement, helping organizations monitor their environmental footprint by giving or taking the coins they need for delivering their products.

### Technologies Used 🧩

The Supply-Chain application is built using the following technologies:

- [Python](https://www.python.org/) as the main programming language
- [Flask](https://flask.palletsprojects.com/en/stable/) as a lightweight WSGI web application framework
- [Hyperledger Besu](https://www.lfdecentralizedtrust.org/projects/besu) for the blockchain network
- [ConsenSys Tessera](https://docs.tessera.consensys.io/) for private transactions
- [Solidity](https://soliditylang.org/) for smart contract development
- [Metamask](https://metamask.io/it/download/) for your private address and key
- [Web3.py](https://web3py.readthedocs.io/en/stable/) for interacting with the smart contracts
- [Gunicorn](https://gunicorn.org/) as a **WSGI** Server
- [Nginx](https://nginx.org/) as the reverse proxy server
- [Docker](https://www.docker.com/) and [Compose](https://docs.docker.com/compose/) for containerization
- [PostgreSQL](https://www.postgresql.org/) for the database

### Codacy Evaluation 📊

[![Codacy Badge](https://app.codacy.com/project/badge/Grade/9fcbf5b50d4442539b29a34f81b5bf4d)](https://app.codacy.com/gh/GabrielPiercecchi/SoftwareSecurity-BlockchainProject/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)

Codacy is an automated code review tool that helps identify code quality issues, security vulnerabilities, and performance improvements. It provides an in-depth analysis of the source code and suggests corrections to improve the overall quality of the project. By using Codacy, you can ensure that your code adheres to coding standards and industry best practices.

The badge above shows the current project rating on Codacy. By clicking on the badge, you can access the Codacy dashboard for this project and view the details of the code analysis.

## Gettin Started 🗂️

In order to run a local copy of the application, you need to follow the steps below.

### Prerequisites 📋

Ensure you have the following installed on your machine:
- *Docker & Docker Compose* (Follow the [official installation guide](https://docs.docker.com/compose/install/) based on your OS)
- *Python 3.12* (Recommended for local development). You can install Python by following this [link](https://www.python.org/downloads/).
- *Node.js & npm* (If interacting with blockchain through frontend tools). You can install both of them by following this [link](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm).
- A *MetaMask* account.
  
> ⚠️ **NOTE**:  *If* you wanto to run this application on *Windows* it is recommended to have the [Windows Subsystem for Linux installed](https://docs.microsoft.com/en-us/windows/wsl/install) on your machine, to install a Linux Distribution on it (like [Ubuntu](https://documentation.ubuntu.com/wsl/en/latest/howto/install-ubuntu-wsl2/)) and to have Docker configured to use **WSL2** as the default engine.

### Installation 🛠️

First clone the repository:

```bash
git clone https://github.com/GabrielPiercecchi/SoftwareSecurity-BlockchainProject.git
cd SoftwareSecurity-BlockchainProject
```

Once cloned, you must setup the environment variables: place a `.env` file in the root directory and fill in the following variables: 

```env
# Flask app configuration
SERVICE_HOST=3000
SERVICE_PORT=3000
DATABASE_USER=
DATABASE_PASSWORD=
DATABASE_NAME=
DATABASE_PORT=5432
ADMIN_PRIVATE_KEY=
ADMIN_ADDRESS=
ORACLE_USERNAME=
ORACLE_PASSWORD=
SECRET_KEY=
BLOCKCHAIN_URL=http://rpcnode:8545

# PostgreSQL configuration
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_HOST=postgres
POSTGRES_DB=postgres

# Blockscout configuration
BLOCKSCOUT_HOST=blockscoutpostgres

# Host and port configuration
HOST=0.0.0.0
PORT=5000
LOCALHOST=localhost
DATABASE_PORT_FLASK_APP=5432

# Nonce file path
NONCE_FILE=./algorithms/nonce.txt

# User credentials from seeder.py
USER1_USERNAME=
USER1_PASSWORD=
USER2_USERNAME=
USER2_PASSWORD=
USER3_USERNAME=
USER3_PASSWORD=
USER4_USERNAME=
USER4_PASSWORD=

# Docker-compose configuration
BESU_VERSION=23.4.1
QUORUM_VERSION=23.4.0
TESSERA_VERSION=23.4.0
ETHSIGNER_VERSION=22.1.3
QUORUM_EXPLORER_VERSION=4f60191

# Lock file
LOCK_FILE=.quorumDevQuickstart.lock

# GoQuorum consensus algorithm
# Options: istanbul, qbft, raft
# Note: Use lower case only
GOQUORUM_CONS_ALGO=qbft

# Besu consensus algorithm
# Options: IBFT, QBFT, CLIQUE
# Note: IBFT refers to IBFT2.0, not IBFT1.0
# Use upper case only
BESU_CONS_ALGO=QBFT

# Log configuration file for Besu
LOG4J_CONFIGURATION_FILE=/quorum-test-network/config/log-config.xml
```

- `DATABASE_USER`: The username for your PostgreSQL database.
- `DATABASE_PASSWORD`: The password for your PostgreSQL database.
- `DATABASE_NAME`: The name of your PostgreSQL database.
- `ADMIN_PRIVATE_KEY`: The private key for the admin account used for blockchain transactions.
- `ADMIN_ADDRESS`: The blockchain address associated with the admin private key.
  > ⚠️ **NOTE**:  Both the `ADMIN_ADDRESS` and the `ADMIN_PRIVATE_KEY` can be found in your Metamask Account in *Account Details*.
- `ORACLE_USERNAME`: The username for the oracle account.
- `ORACLE_PASSWORD`: The password for the oracle account.
- `SECRET_KEY`: A secret key used for Flask session management and security. You can generate it with the *algorithms/secret_key_generator.py* file.
- `POSTGRES_USER`: The username for your PostgreSQL database (used by Docker).
- `POSTGRES_PASSWORD`: The password for your PostgreSQL database (used by Docker).
- `USER1_USERNAME`: The username for the first user account. Set this to the desired username for the first user.
- `USER1_PASSWORD`: The password for the first user account. Set this to the desired password for the first user.
- `USER2_USERNAME`: The username for the second user account. Set this to the desired username for the second user.
- `USER2_PASSWORD`: The password for the second user account. Set this to the desired password for the second user.
- `USER3_USERNAME`: The username for the third user account. Set this to the desired username for the third user.
- `USER3_PASSWORD`: The password for the third user account. Set this to the desired password for the third user.
- `USER4_USERNAME`: The username for the fourth user account. Set this to the desired username for the fourth user.
- `USER4_PASSWORD`: The password for the fourth user account. Set this to the desired password for the fourth user.

The `quorum-test-network` folder exists, but to ensure its functionality, it is recommended to delete it and then run the following command:

```bash
npx quorum-dev-quickstart
```

> ⚠️ **NOTE**: To run this command, you need to have *Node.js* and *npm* installed, as mentioned earlier and later when discussing the commands for the three types of operating systems.

Your terminal will lool like this:

```bash
yourTerminal$ npx quorum-dev-quickstart

              ___
             / _ \   _   _    ___    _ __   _   _   _ __ ___
            | | | | | | | |  / _ \  | '__| | | | | | '_ ' _ \
            | |_| | | |_| | | (_) | | |    | |_| | | | | | | |
             \__\_\  \__,_|  \___/  |_|     \__,_| |_| |_| |_|

        ____                          _
       |  _ \    ___  __   __   ___  | |   ___    _ __     ___   _ __
       | | | |  / _ \ \ \ / /  / _ \ | |  / _ \  | '_ \   / _ \ | '__|
       | |_| | |  __/  \ V /  |  __/ | | | (_) | | |_) | |  __/ | |
       |____/   \___|   \_/    \___| |_|  \___/  | .__/   \___| |_|
                                                 |_|
       ___            _          _            _                    _
      / _ \   _   _  (_)   ___  | | __  ___  | |_    __ _   _ __  | |_
     | | | | | | | | | |  / __| | |/ / / __| | __|  / _' | | '__| | __|
     | |_| | | |_| | | | | (__  |   <  \__ \ | |_  | (_| | | |    | |_
      \__\_\  \__,_| |_|  \___| |_|\_\ |___/  \__|  \__,_| |_|     \__|


Welcome to the Quorum Developer Quickstart utility. This tool can be used
to rapidly generate local Quorum blockchain networks for development purposes
using tools like GoQuorum, Besu, and Tessera.

To get started, be sure that you have both Docker and Docker Compose
installed, then answer the following questions.

Which Ethereum client would you like to run? Default: [1]
        1. Hyperledger Besu
        2. GoQuorum
1
Do you wish to enable support for private transactions? [Y/n]
y
Do you wish to enable support for logging with Loki, Splunk or ELK (Elasticsearch, Logstash & Kibana)? Default: [1]
        1. Loki
        2. Splunk
        3. ELK
1
Do you wish to enable support for monitoring your network with Chainlens? [N/y]
N
Do you wish to enable support for monitoring your network with Blockscout? [N/y]
N
Where should we create the config files for this network? Please
choose either an empty directory, or a path to a new directory that does
not yet exist. Default: ./quorum-test-network

✅ Installation complete.

To start your test network, run 'run.sh' in the directory, './quorum-test-network'
For more information on the test network, see 'README.md' in the directory, './quorum-test-network'
```
You will have to choose *1. Hyperledger Besu*, *y* for enabling Private Trnsactions, *1. Loki*, *n* for *Chainlens* and *Blockscout* and, finally, press *Enter* for creating the default directory *./quorum-test-network*

After that, for increased security, you need to create keys using [OpenSSL](https://www.openssl.org/).

For Windows, OpenSSL must be downloaded through the Linux distribution available inside WSL (Ubuntu in this case) using the following command:

```bash
sudo apt-get install openssl
```

For Linux, the procedure is similar. You will have to use your package manager to install the `openssl` package.

For MacOS, OpenSSL is available at the following [address](http://macappstore.org/openssl/)

After this, navigate to the *nginx/certs* directory from the root of the project (*The directory won't probably exist; you will have to create it with this terminal line:* `mkdir -p nginx/certs`) and execute the following command:

```bash
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
```

> ⚠️ **NOTE**: This will create two certificates (`key.pem` and `cert.pem`) that will expire after *365 days*.

- *openssl req*: Initiates a certificate request.
- *x509*: Specifies that a self-signed certificate is to be created instead of a certificate signing request (CSR).
- *newkey rsa:4096*: Creates a new RSA private key with 4096 bits.
- *keyout key.pem*: Specifies the file in which to save the private key.
- *out cert.pem*: Specifies the file in which to save the self-signed certificate.
- *days 365*: Specifies the duration of the certificate in days (365 days, i.e., one year).
- *nodes*: Indicates not to encrypt the private key.

To complete it, simply press *Enter* at each prompt.

Then, you can safely build the images and run the containers using the following Docker command:

```bash
docker-compose up -d --build
```

#### Linux 🐧

The application has been tested and has been designed to run on Linux machines, and it is recommended to use a Linux distribution to run it.

More specifically, the application has been tested on these distributions:
- [Ubuntu](https://www.ubuntu-it.org/)
- [Fedora](https://fedoraproject.org/it/)
- [Arch Linux](https://archlinux.org/)

#### Windows 🪟

The application has been tested only on Windows 11, but it should work on Windows 10 too.

However, several problems may arise if you choose to run it on a Windows machine, especially, like said before, with the blockchain network.

To mitigate these issues, it is necessary to have **WSL** (Windows Subsystem for Linux) installed along with a Linux distribution and to have Docker configured to use WSL2 as the default engine. As mentioned earlier, we used Ubuntu to install and run the command `npx quorum-dev-quickstart`.

You can follow these steps to set up WSL and Ubuntu:

1. **Install WSL**:
    Open PowerShell as Administrator and run:
    ```powershell
    wsl --install
    ```

2. **Install Ubuntu**:
    After installing WSL, you can install Ubuntu from the Microsoft Store or by running:
    ```powershell
    wsl --install -d Ubuntu
    ```

3. **Set up Ubuntu**:
    Once Ubuntu is installed, open the Ubuntu terminal and update the package list:
    ```bash
    sudo apt-get update
    sudo apt-get upgrade 
    ```

    Install Node.js and npm:
    ```bash
    sudo apt-get install nodejs npm
    ```

4. **Run the Quorum Dev Quickstart**:
    Navigate to your project directory and run:
    ```bash
    npx quorum-dev-quickstart
    ```

#### MacOS 🍏

The application has NOT been tested on macOS machines, neither on Intel nor ARM architectures.

Despite this, the application should still run on Mac, if the prerequisites are met.

## Usage 🚀

Once the setup has been completed, the application is ready tu use. You just need to wait a few minutes to ensure that the blockchain starts up securely. Then, navigate to the root directory of the project and run the following command to observe the startup logs of the application and get the local address:

```bash
docker-compose logs flask-app 
```

Your terminal will have an output that will look like this one (*if not just wait a few more seconds and try it again*):

```bash
PS ...\SoftwareSecurity-BlockchainProject> docker-compose logs flask-app
time="2025-02-04T12:45:26+01:00" level=warning msg="...\\SoftwareSecurity-BlockchainProject\\docker-compose.yaml: the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion"
flask-app  | [2025-02-04 11:08:04 +0000] [1] [INFO] Starting gunicorn 23.0.0
flask-app  | [2025-02-04 11:08:34 +0000] [1] [INFO] Listening at: http://0.0.0.0:5000 (1)
flask-app  | [2025-02-04 11:08:34 +0000] [1] [INFO] Using worker: sync
flask-app  | [2025-02-04 11:08:34 +0000] [7] [INFO] Booting worker with pid: 7
flask-app  | [2025-02-04 11:08:34 +0000] [8] [INFO] Booting worker with pid: 8
flask-app  | [2025-02-04 11:08:34 +0000] [9] [INFO] Booting worker with pid: 9
flask-app  | [2025-02-04 11:08:34 +0000] [10] [INFO] Booting worker with pid: 10
```

> ⚠️ **NOTE**: If you see a warning in the logs about the `version` attribute being obsolete, it is not a problem. This warning indicates that the `version` attribute in the `docker-compose.yaml` file is deprecated and will be ignored. The functionality of your Docker setup will not be affected.

Now, you can interact with the application through the address 

[http://localhost:5000](http://localhost:5000).

### Running the Server 🖥️

Like said before, when all the prerequisites are met and the command 

```bash
docker-compose up -d --build
```

is executed the application is ready to run.

When you run the application for the first time, before you can access the application proper, you will need to wait for the deployment of the smart contract on the blockchain. This process can take up to a few minutes to complete.

When you are done and want to stop the application, you can use the following command in the root directory of the application:

```bash
docker-compose stop
```

After that, when you want to start it again, the following command will come in handy:

```bash
docker-compose restart
```
> ⚠️ **NOTE**: In case you want to "*bring down*" the containers managing the application you can do it with the command `docker-compose down` **BUT**, before running the command `docker-compose up -d --build` again to rebuild the application, it will be necessary to delete the files *algorithms/nonce.txt* and *contract/contract_address.txt*.
> - *nonce.txt*: This file stores the current nonce value used for transactions. Deleting this file ensures that the nonce value is reset, preventing potential transaction conflicts.
> - *contract_address.txt*: This file stores the address of the deployed smart contract. Deleting this file ensures that a new smart contract is deployed, which is necessary if the previous contract instance is no longer valid or has been removed.

#### Database Setup 🗄️

*No* additional commands are necessary for database **migration** and **seeding**, as these processes are performed automatically when the application starts.

You can find them in the *database/migration.py* and *database/seeder.py* files.

### Troubleshooting 🔧

If you encounter issues with the application, here are some common troubleshooting steps:

1. **Check Docker Logs**:

    Use the following command to check the logs of the Flask application (This can help identify any errors or warnings that may be causing issues):

    ```bash
    docker-compose logs flask-app
    ```

2. ** Verify Environment Variables**: 

    Ensure that all required environment variables are correctly set in the `.env` file. Missing or incorrect values can cause the application to fail.

3. **Database Connection Issues**: 

    If the application cannot connect to the PostgreSQL database, verify that the database service is running and that the credentials in the `.env` file are correct.

4. **Super User in PostgreSQL**: 

    By default, the super user in PostgreSQL is the default user shown in its documentation (`postgres`). It is highly recommended to change this default super user password immediately for security reasons.

    The credentials for this super user should then be inserted into the `.env` file as shown previously.

    ```env
    DATABASE_USER=your_new_co2_db_super_user
    DATABASE_PASSWORD=your_new_co2_db_super_user_password
    DATABASE_NAME=your_co2_db_name

    # PostgreSQL configuration
    POSTGRES_USER=your_new_postgres_super_user
    POSTGRES_PASSWORD=your_new_postgres_super_user_password
    ```

    > ⚠️ **NOTE**: The two different databases listed above serve distinct purposes. The first set of credentials (`DATABASE_USER`, `DATABASE_PASSWORD`, `DATABASE_NAME`) is related to the sub-container hosting the application's database. The second set of credentials (`POSTGRES_USER`, `POSTGRES_PASSWORD`) is used by third-party components placed in another sub-container of the application.

#### Creating a Super User 👤

To create the super user in the two containers of the application, follow these steps:

1. **Creating the Super User in the `db_pg` Container**:
First, access the `db_pg` container:

    ```bash
    docker exec -it db_pg psql -U postgres
    ```

    Once inside the PostgreSQL prompt, create the new super user:

    ```bash
    CREATE USER <your_new_co2_db_super_user> WITH SUPERUSER PASSWORD <'your_new_co2_db_super_user_password'>;
    ```

    Replace *your_new_co2_db_super_user* and *your_new_co2_db_super_user_password* with your desired username and password.

2. **Creating the Super User in the `blockscoutpostgres` Container**:

    First, access the blockscoutpostgres container:

    ```bash
    docker exec -it blockscoutpostgres psql -U postgres
    ```

    Once inside the PostgreSQL prompt, create the new super user:

    ```bash
    CREATE USER <your_new_postgres_super_user> WITH SUPERUSER PASSWORD <'your_new_postgres_super_user_password'>;
    ```

    Replace *your_new_postgres_super_user* and *your_new_postgres_super_user_password* with your desired username and password.

After creating the super users, ensure that the credentials are correctly set in the `.env` file as shown previously. This will ensure that the application and its third-party components can connect to the respective databases using the new super user credentials.

### Node Explorer 🔍

While using the application, you can observe the transactions executed within the blockchain through the following link:

[http://localhost:25000](http://localhost:25000)

This will provide you with a detailed view of all the blockchain activities and transactions such as `Nodes`, `Validators`, `Explorer`, `Contracts` and `Wallets`.

Additionally, you can search for specific transactions in detail using their hash or block through the following link:

[http://localhost:25000/explorer/explorer](http://localhost:25000/explorer/explorer)

This will allow you to explore the transactions executed within the blockchain in greater detail.

### Logs 📜

The logs can be found in the following locations:

1. **Flask Application Logs**:
  
    The logs for the Flask application can be found in the `log_users.txt` file. This file contains information about the requests made to the application, including the username of the user who made the request if they are logged in.

2. **Blockchain Logs**:

    The logs for the blockchain can be found in the `quorum-test-network/logs/` directory. These logs contain information about the various instances of the blockchain and the signing of the transactions.

By checking these logs, you can gain insights into the application's activity and troubleshoot any issues that may arise.

## Credits 👯‍♂️

- [Gabriel Piercecchi](https://github.com/GabrielPiercecchi)
- [Tosca Pierro](https://github.com/toscap2002)
- [Luca Pigliacampo](https://github.com/Luca-Pigliacampo)
- [Caterina Sabatini](https://github.com/CaterinaSabatini)