// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable2Step.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

contract EssentiumMusicNFT is ERC721, Ownable2Step, ReentrancyGuard {
    IERC20 public immutable PaC;

    uint256 public nextTokenId;

    struct MusicMetadata {
        string trackName;
        string frequencyTag;
        uint256 mintTimestamp;
    }

    struct Stake {
        uint256 stakedAmount;
        uint256 startTime;
        uint256 lastClaim;
    }

    mapping(uint256 => MusicMetadata) public metadata;
    mapping(uint256 => Stake) public stakes;

    uint256 public constant BASE_RATE = 500;      // 5% per year
    uint256 public constant PATIENCE_BONUS = 25;  // +25% after 30 days
    uint256 public constant ROOT_BONUS = 15;      // Extra for 0.7 Hz

    event MusicNFTMinted(uint256 tokenId, address owner, string trackName, string frequencyTag);
    event Staked(uint256 tokenId, uint256 amount);
    event RewardClaimed(uint256 tokenId, uint256 reward);

    constructor(address _paC) ERC721("Essentium Music", "EMNFT") Ownable2Step(msg.sender) {
        PaC = IERC20(_paC);
    }

    function mintMusicNFT(string calldata trackName, string calldata frequencyTag) external {
        uint256 tokenId = nextTokenId++;
        _mint(msg.sender, tokenId);

        metadata[tokenId] = MusicMetadata(trackName, frequencyTag, block.timestamp);

        emit MusicNFTMinted(tokenId, msg.sender, trackName, frequencyTag);
    }

    function stake(uint256 tokenId, uint256 amount) external nonReentrant {
        require(ownerOf(tokenId) == msg.sender, "Not owner");
        require(amount > 0, "Zero amount");

        PaC.transferFrom(msg.sender, address(this), amount);

        Stake storage s = stakes[tokenId];
        if (s.startTime == 0) s.startTime = block.timestamp;
        s.stakedAmount += amount;
        s.lastClaim = block.timestamp;

        emit Staked(tokenId, amount);
    }

    function claimReward(uint256 tokenId) external nonReentrant {
        require(ownerOf(tokenId) == msg.sender, "Not owner");

        Stake storage s = stakes[tokenId];
        require(s.stakedAmount > 0, "Nothing staked");

        uint256 timeElapsed = block.timestamp - s.lastClaim;
        uint256 base = (s.stakedAmount * BASE_RATE * timeElapsed) / (365 days * 10000);

        uint256 bonus = 0;
        if (timeElapsed > 30 days) {
            bonus = base * PATIENCE_BONUS / 100;
        }

        // Extra bonus for 0.7 Hz root
        if (bytes(metadata[tokenId].frequencyTag).length > 0 && 
            keccak256(bytes(metadata[tokenId].frequencyTag)) == keccak256(bytes("0.7 Hz Django Sound"))) {
            bonus += base * ROOT_BONUS / 100;
        }

        uint256 total = base + bonus;

        if (total > 0) {
            s.lastClaim = block.timestamp;
            PaC.transfer(msg.sender, total);
            emit RewardClaimed(tokenId, total);
        }
    }

    function getStakeInfo(uint256 tokenId) external view returns (uint256 staked, uint256 pending) {
        Stake memory s = stakes[tokenId];
        uint256 timeElapsed = block.timestamp - s.lastClaim;
        uint256 base = (s.stakedAmount * BASE_RATE * timeElapsed) / (365 days * 10000);
        return (s.stakedAmount, base);
    }
}
