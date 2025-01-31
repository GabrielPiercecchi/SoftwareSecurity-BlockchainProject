// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

/// @title CoinContract
/// @notice This contract manages the balances of organizations and allows updating their coin balances.
/// @dev Follows the EthTrust Security Levels and Solidity Style Guide.

contract CoinContract {
    /// @notice Mapping to store the balances of organizations.
    mapping(address => uint256) public balances;

    /// @notice Struct to store transaction details.
    struct Transaction {
        address organization;
        int256 amount;
        uint256 timestamp;
        bytes32 txHash;
    }

    /// @notice Struct to store product origin transaction details.
    struct ProductOriginTransaction {
        uint256 originProduct;
        uint256 endProduct;
        uint256 timestamp;
    }

    /// @notice Struct to store rejected transaction details.
    struct RejectedTransaction {
        address organization;
        int256 amount;
        uint256 timestamp;
        string reason;
        string productName;
        uint256 productQuantity;
        uint256 co2Emission;
        bytes32 txHash;
    }

    /// @notice Array to store all transactions.
    Transaction[] public transactions;

    /// @notice Array to store all product origin transactions.
    ProductOriginTransaction[] public productOriginTransactions;

    /// @notice Array to store all rejected transactions.
    RejectedTransaction[] public rejectedTransactions;

    /// @notice Event emitted when the coin balance of an organization is updated.
    /// @param organization The address of the organization.
    /// @param newBalance The new balance of the organization.
    event CoinsUpdated(address indexed organization, uint256 newBalance);

    /// @notice Event emitted when a product origin is registered.
    /// @param originProduct The ID of the origin product.
    /// @param endProduct The ID of the end product.
    event ProductOriginRegistered(uint256 indexed originProduct, uint256 indexed endProduct);

    /// @notice Event emitted when a transaction is rejected.
    /// @param organization The address of the organization.
    /// @param amount The amount of the rejected transaction.
    /// @param reason The reason for the rejection.
    /// @param productName The name of the product.
    /// @param productQuantity The quantity of the product.
    /// @param co2Emission The CO2 emission of the product.
    /// @param txHash The transaction hash.
    event TransactionRejected(address indexed organization, int256 amount, string reason, string productName, uint256 productQuantity, uint256 co2Emission, bytes32 txHash);

    /// @notice Updates the coin balance of an organization.
    /// @param organization The address of the organization.
    /// @param amount The amount to update the balance by. Can be positive or negative.
    function updateCoins(address organization, int256 amount) public {
        require(organization != address(0), "Invalid address");

        if (amount < 0) {
            uint256 absAmount = uint256(-amount);
            require(balances[organization] >= absAmount, "Insufficient balance");
            balances[organization] -= absAmount;
        } else {
            balances[organization] += uint256(amount);
        }

        // Memorizza la transazione
        bytes32 txHash = keccak256(abi.encodePacked(block.number, organization, amount, block.timestamp));
        transactions.push(Transaction({
            organization: organization,
            amount: amount,
            timestamp: block.timestamp,
            txHash: txHash
        }));

        emit CoinsUpdated(organization, balances[organization]);
    }

    /// @notice Updates the coin balance of an organization based on CO2 emissions.
    /// @param organization The address of the organization.
    /// @param co2Emission The CO2 emission of the organization.
    /// @param co2Limit The CO2 limit for the organization.
    function updateCoinsBasedOnEmission(address organization, uint256 co2Emission, uint256 co2Limit) public {
        require(organization != address(0), "Invalid address");

        int256 amount;
        if (co2Emission > co2Limit) {
            uint256 malusCoin = co2Emission - co2Limit;
            require(balances[organization] >= malusCoin, "Insufficient balance for malus");
            balances[organization] -= malusCoin;
            amount = -int256(malusCoin);
        } else {
            uint256 bonusCoin = co2Limit - co2Emission;
            balances[organization] += bonusCoin;
            amount = int256(bonusCoin);
        }

        // Memorizza la transazione
        bytes32 txHash = keccak256(abi.encodePacked(block.number, organization, amount, block.timestamp));
        transactions.push(Transaction({
            organization: organization,
            amount: amount,
            timestamp: block.timestamp,
            txHash: txHash
        }));

        emit CoinsUpdated(organization, balances[organization]);
    }

    /// @notice Transfers coins from one organization to another.
    /// @param from The address of the organization sending the coins.
    /// @param to The address of the organization receiving the coins.
    /// @param amount The amount of coins to transfer.
    /// @dev The transaction hash is generated using the block number, organization address, amount, and timestamp.
    function transferCoins(address from, address to, uint256 amount) public {
        require(from != address(0), "Invalid sender address");
        require(to != address(0), "Invalid recipient address");
        require(balances[from] >= amount, "Insufficient balance");

        balances[from] -= amount;
        balances[to] += amount;

        // Memorizza la transazione per il mittente
        bytes32 txHashFrom = keccak256(abi.encodePacked(block.number, from, -int256(amount), block.timestamp));
        transactions.push(Transaction({
            organization: from,
            amount: -int256(amount),
            timestamp: block.timestamp,
            txHash: txHashFrom
        }));

        // Memorizza la transazione per il destinatario
        bytes32 txHashTo = keccak256(abi.encodePacked(block.number, to, int256(amount), block.timestamp));
        transactions.push(Transaction({
            organization: to,
            amount: int256(amount),
            timestamp: block.timestamp,
            txHash: txHashTo
        }));

        emit CoinsUpdated(from, balances[from]);
        emit CoinsUpdated(to, balances[to]);
    }

    /// @notice Registers a product origin.
    /// @param originProduct The ID of the origin product.
    /// @param endProduct The ID of the end product.
    function registerProductOrigin(uint256 originProduct, uint256 endProduct) public {
        require(originProduct != 0, "Invalid origin product ID");
        require(endProduct != 0, "Invalid end product ID");

        // Memorizza la transazione di origine del prodotto
        productOriginTransactions.push(ProductOriginTransaction({
            originProduct: originProduct,
            endProduct: endProduct,
            timestamp: block.timestamp
        }));

        // Emit the event
        emit ProductOriginRegistered(originProduct, endProduct);
    }

    /// @notice Registers a rejected transaction.
    /// @param organization The address of the organization.
    /// @param amount The amount of the rejected transaction.
    /// @param reason The reason for the rejection.
    /// @param productName The name of the rejected product.
    /// @param productQuantity The quantity of the rejected product.
    /// @param co2Emission The CO2 emission of the rejected product.
    /// @dev The transaction hash is generated using the block number, organization address, amount, and timestamp.
    function registerRejectedTransaction(address organization, int256 amount, string memory reason, string memory productName, uint256 productQuantity, uint256 co2Emission) public {
        require(organization != address(0), "Invalid address");

        // Genera il txHash
        bytes32 txHash = keccak256(abi.encodePacked(block.number, organization, amount, block.timestamp));

        // Memorizza la transazione rifiutata
        rejectedTransactions.push(RejectedTransaction({
            organization: organization,
            amount: amount,
            timestamp: block.timestamp,
            reason: reason,
            productName: productName,
            productQuantity: productQuantity,
            co2Emission: co2Emission,
            txHash: txHash
        }));

        emit TransactionRejected(organization, amount, reason, productName, productQuantity, co2Emission, txHash);
    }

    /// @notice Returns the coin balance of an organization.
    /// @param organization The address of the organization.
    /// @return The balance of the organization.
    function getBalance(address organization) public view returns (uint256) {
        return balances[organization];
    }

    /// @notice Returns the transactions of an organization.
    /// @param organization The address of the organization.
    /// @return Arrays of transaction details.
    function getTransactions(address organization) public view returns (address[] memory, int256[] memory, uint256[] memory, bytes32[] memory) {
        uint256 count = 0;
        for (uint256 i = 0; i < transactions.length; i++) {
            if (transactions[i].organization == organization) {
                count++;
            }
        }

        address[] memory orgs = new address[](count);
        int256[] memory amounts = new int256[](count);
        uint256[] memory timestamps = new uint256[](count);
        bytes32[] memory txHashes = new bytes32[](count);
        uint256 index = 0;
        for (uint256 i = 0; i < transactions.length; i++) {
            if (transactions[i].organization == organization) {
                orgs[index] = transactions[i].organization;
                amounts[index] = transactions[i].amount;
                timestamps[index] = transactions[i].timestamp;
                txHashes[index] = transactions[i].txHash;
                index++;
            }
        }

        return (orgs, amounts, timestamps, txHashes);
    }

    /// @notice Returns the product origin transactions.
    /// @return Arrays of product origin transaction details.
    function getProductOriginTransactions() public view returns (uint256[] memory, uint256[] memory, uint256[] memory) {
        uint256 count = productOriginTransactions.length;

        uint256[] memory originProducts = new uint256[](count);
        uint256[] memory endProducts = new uint256[](count);
        uint256[] memory timestamps = new uint256[](count);

        for (uint256 i = 0; i < count; i++) {
            originProducts[i] = productOriginTransactions[i].originProduct;
            endProducts[i] = productOriginTransactions[i].endProduct;
            timestamps[i] = productOriginTransactions[i].timestamp;
        }

        return (originProducts, endProducts, timestamps);
    }

    /// @notice Returns the rejected transactions of an organization.
    /// @param organization The address of the organization.
    /// @return Arrays of rejected transaction details.
    function getRejectedTransactionDetails1(address organization) public view returns (address[] memory, int256[] memory, uint256[] memory, string[] memory) {
        uint256 count = 0;
        for (uint256 i = 0; i < rejectedTransactions.length; i++) {
            if (rejectedTransactions[i].organization == organization) {
                count++;
            }
        }

        address[] memory orgs = new address[](count);
        int256[] memory amounts = new int256[](count);
        uint256[] memory timestamps = new uint256[](count);
        string[] memory reasons = new string[](count);
        uint256 index = 0;
        for (uint256 i = 0; i < rejectedTransactions.length; i++) {
            if (rejectedTransactions[i].organization == organization) {
                orgs[index] = rejectedTransactions[i].organization;
                amounts[index] = rejectedTransactions[i].amount;
                timestamps[index] = rejectedTransactions[i].timestamp;
                reasons[index] = rejectedTransactions[i].reason;
                index++;
            }
        }

        return (orgs, amounts, timestamps, reasons);
    }

    /// @notice Returns the rejected transactions of an organization.
    /// @param organization The address of the organization.
    /// @return Arrays of rejected transaction details.
    function getRejectedTransactionDetails2(address organization) public view returns (string[] memory, uint256[] memory, uint256[] memory, bytes32[] memory) {
        uint256 count = 0;
        for (uint256 i = 0; i < rejectedTransactions.length; i++) {
            if (rejectedTransactions[i].organization == organization) {
                count++;
            }
        }

        string[] memory productNames = new string[](count);
        uint256[] memory productQuantities = new uint256[](count);
        uint256[] memory co2Emissions = new uint256[](count);
        bytes32[] memory txHashes = new bytes32[](count);
        uint256 index = 0;
        for (uint256 i = 0; i < rejectedTransactions.length; i++) {
            if (rejectedTransactions[i].organization == organization) {
                productNames[index] = rejectedTransactions[i].productName;
                productQuantities[index] = rejectedTransactions[i].productQuantity;
                co2Emissions[index] = rejectedTransactions[i].co2Emission;
                txHashes[index] = rejectedTransactions[i].txHash;
                index++;
            }
        }

        return (productNames, productQuantities, co2Emissions, txHashes);
    }
}