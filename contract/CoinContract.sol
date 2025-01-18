// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

contract CoinContract {
    mapping(address => uint256) public balances;

    event CoinsUpdated(address indexed organization, uint256 newBalance);

    function updateCoins(address organization, int256 amount) public {
        if (amount < 0) {
            require(balances[organization] >= uint256(-amount), "Insufficient balance");
            balances[organization] -= uint256(-amount);
        } else {
            balances[organization] += uint256(amount);
        }
        emit CoinsUpdated(organization, balances[organization]);
    }

    function getBalance(address organization) public view returns (uint256) {
        return balances[organization];
    }
}