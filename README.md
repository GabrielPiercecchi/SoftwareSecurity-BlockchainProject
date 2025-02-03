# SoftwareSecurity-BlockchainProject
- [SoftwareSecurity-BlockchainProject](#softwaresecurity-blockchainproject)
  - [Introduction 📖](#introduction-)
    - [Main Features](#main-features)
    - [How it Works](#how-it-works)
    - [Technologies Used](#technologies-used)
  - [Gettin Started 🗂️](#gettin-started-️)
    - [Prerequisites](#prerequisites)
    - [Installation 🛠️](#installation-️)
      - [Linux](#linux)
      - [Windows](#windows)
      - [MacOS](#macos)
  - [Usage 🚀](#usage-)
    - [Running the Server](#running-the-server)
      - [Database Setup](#database-setup)
        - [Migration](#migration)
        - [Seeding](#seeding)
    - [Troubleshooting](#troubleshooting)
      - [Creating a Super User](#creating-a-super-user)
      - [Module Testing](#module-testing)
    - [Node Explorer](#node-explorer)
    - [Logs](#logs)
  - [Credits 🤝](#credits-)

## Introduction 📖

This application leverages blockchain technology to track products throughout the supply chain while monitoring and recording the Co<sub>2</sub> emissions generated at each stage. By ensuring data integrity, transparency, and security, the system helps businesses and consumers make informed decisions regarding sustainability.

### Main Features

- *Product Tracking*: Monitors a product's journey from origin to final destination.

- *Co<sub>2</sub> Emissions Calculation*: Records emissions generated at each step of the supply chain.

- *Blockchain Integration*: Ensures data integrity and security using a private blockchain network.

- *Smart Contracts*: Automates verification and validation of product movement and emissions data.

- *Audit & Reporting*: Generates reports on Co<sub>2</sub> emissions for compliance and sustainability tracking.

### How it Works

The application begins with a home page where users can observe various companies and products, and check their provenance. Once authenticated, employers, carriers, and oracles can log in using secure methods. Employers can manage products within their organization, creating, updating, and viewing product details. Organizations can request products from others, and these requests are meticulously tracked and managed.

*Oracles* play a crucial role by facilitating coin transfers between organizations, ensuring smooth transactions. Every product movement and coin transfer is recorded on the blockchain, providing an immutable and transparent ledger. The system also calculates and records CO<sub>2</sub> emissions for each product movement, helping organizations monitor their environmental footprint by giving or taking the coins they need for delivering their products.

### Technologies Used

The Supply-Chain application is built using the following technologies:

- [Python](https://www.python.org/) as the main programming language
- [Hyperledger Besu](https://www.lfdecentralizedtrust.org/projects/besu) for the blockchain network
- [ConsenSys Tessera](https://docs.tessera.consensys.io/) for private transactions
- [Solidity](https://soliditylang.org/) for smart contract development
- [Metamask](https://metamask.io/it/download/) for your private address and key
- [Web3.py](https://web3py.readthedocs.io/en/stable/) for interacting with the smart contracts
- [Gunicorn](https://gunicorn.org/) for using a **WSGI** Server
- [Docker](https://www.docker.com/) and [Compose](https://docs.docker.com/compose/) for containerization
- [PostgreSQL](https://www.postgresql.org/) for the database

## Gettin Started 🗂️

In order to run a local copy of the application, you need to follow the steps below.

### Prerequisites

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
- `SECRET_KEY`: A secret key used for Flask session management and security. You can generate it with the *algorithms\secret_key_generator.py* file.
- `POSTGRES_USER`: The username for your PostgreSQL database (used by Docker).
- `POSTGRES_PASSWORD`: The password for your PostgreSQL database (used by Docker).

In case the `quorum-test-network` folder does not work (there are many `.env` files inside it that cannot be uploaded in this repository), you can safely delete it and then run the following command:

```bash
npx quorum-dev-quickstart
```

You terminal will lool like this:

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

Then, you can safely build the images and run the containers using the following Docker command:

```bash
docker-compose up -d --build
```

#### Linux

The application has been tested and has been designed to run on Linux machines, and it is recommended to use a Linux distribution to run it.

More specifically, the application has been tested on these distributions:
- [Ubuntu](https://www.ubuntu-it.org/)
- [Fedora](https://fedoraproject.org/it/)
- [Arch Linux](https://archlinux.org/)

#### Windows

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

#### MacOS

The application has NOT been tested on macOS machines, neither on Intel nor ARM architectures.

Despite this, the application should still run on Mac, if the prerequisites are met.

## Usage 🚀

Once the setup has been completed, the application is ready tu use. You just need to wait a few minutes to ensure that the blockchain starts up securely. Then, navigate to the root directory of the project and run the following command to observe the startup logs of the application and get the local address:

```bash
docker-compose logs flask-app 
```

Yor terminal will have an output that will look like this one:

```bash
PS ...\SoftwareSecurity-BlockchainProject> docker-compose logs flask-app
time="2025-02-03T18:21:36+01:00" level=warning msg="...\\SoftwareSecurity-BlockchainProject\\docker-compose.yaml: the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion"
flask-app  | Database co2_db already exists.
flask-app  | Database co2_db dropped.
flask-app  | Database co2_db created.
flask-app  | Database and tables initialized!
flask-app  | Database seeded successfully!
flask-app  | Contract loaded successfully.
flask-app  | Contract already deployed at address: 0x8CdaF0CD259887258Bc13a92C0a6dA92698644C0
flask-app  | Contract deployed at address: 0x8CdaF0CD259887258Bc13a92C0a6dA92698644C0
flask-app  | Contract deployed successfully!
flask-app  | Assigned address to organization Org1
flask-app  | Assigned address to organization Org2
flask-app  | Assigned address to organization Org3
flask-app  | Assigned address to organization Org4
flask-app  | Contract loaded successfully.
flask-app  | Contract loaded successfully.
flask-app  | Coins initialized for organization Org1
flask-app  | Contract loaded successfully.
flask-app  | Coins initialized for organization Org2
flask-app  | Contract loaded successfully.
flask-app  | Coins initialized for organization Org3
flask-app  | Contract loaded successfully.
flask-app  | Coins initialized for organization Org4
flask-app  |  * Serving Flask app 'app'
flask-app  |  * Debug mode: off
flask-app  | WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
flask-app  |  * Running on all addresses (0.0.0.0)
flask-app  |  * Running on http://127.0.0.1:5000
flask-app  |  * Running on http://172.16.239.3:5000
```

### Running the Server

...

#### Database Setup

...

##### Migration

...

##### Seeding

....

### Troubleshooting

...

#### Creating a Super User

...

#### Module Testing

...

### Node Explorer

...

### Logs

...

## Credits 🤝

- [Gabriel Piercecchi](https://github.com/GabrielPiercecchi)
- [Tosca Pierro](https://github.com/toscap2002)
- [Luca Pigliacampo](https://github.com/Luca-Pigliacampo)
- [Caterina Sabatini](https://github.com/CaterinaSabatini)