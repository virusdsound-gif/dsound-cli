// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable2Step.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

contract EssentiumTrade is ERC20, Ownable2Step, ReentrancyGuard {
    string public constant VERSION = "11.1 - The Morning Star Layer";

    struct Trade {
        uint256 energyInput;
        bytes32 dsoundSignature;
        uint256 memoryDebt;        // ΔM
        uint256 timestamp;
        uint256 frequencyTier;     // 0=0.7Hz, 1=99.9Hz, 2=200Hz, 3=369Hz
    }

    mapping(address => Trade[]) public trades;
    mapping(bytes32 => bool) public verifiedSignatures;

    event TradeVerified(address indexed user, uint256 energyInput, uint256 memoryDebt, bytes32 signature, uint256 frequencyTier);
    event PaCMinted(address indexed user, uint256 amount);

    constructor() ERC20("Essentium Presence", "PaC") Ownable2Step(msg.sender) {}

    function verifyTrade(
        uint256 _energyInput,
        bytes32 _dsoundSignature,
        uint256 _frequencyTier
    ) external nonReentrant {
        require(_energyInput > 0, "Energy input required");
        require(!verifiedSignatures[_dsoundSignature], "Signature already used");

        uint256 memDebt = calculateMemoryDebt(_energyInput, _frequencyTier);
        
        trades[msg.sender].push(Trade({
            energyInput: _energyInput,
            dsoundSignature: _dsoundSignature,
            memoryDebt: memDebt,
            timestamp: block.timestamp,
            frequencyTier: _frequencyTier
        }));

        verifiedSignatures[_dsoundSignature] = true;

        uint256 paCAmount = memDebt * 2; // Base conversion rate
        _mint(msg.sender, paCAmount);

        emit TradeVerified(msg.sender, _energyInput, memDebt, _dsoundSignature, _frequencyTier);
        emit PaCMinted(msg.sender, paCAmount);
    }

    function calculateMemoryDebt(uint256 energy, uint256 tier) internal pure returns (uint256) {
        uint256 base = energy * 10;
        if (tier == 0) return base * 15 / 10;        // 0.7 Hz → Stronger multiplier (silence)
        if (tier == 3) return base * 20 / 10;        // 369 Hz → Return Gate boost
        return base;
    }

    function getUserTrades(address user) external view returns (Trade[] memory) {
        return trades[user];
    }
}
