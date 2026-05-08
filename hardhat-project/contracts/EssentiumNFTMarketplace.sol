// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/IERC721.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/access/Ownable2Step.sol";

contract EssentiumNFTMarketplace is ReentrancyGuard, Ownable2Step {
    IERC721 public immutable nftContract;
    IERC20 public immutable paC;

    struct Listing {
        address seller;
        uint256 price;      // in PaC
        bool active;
    }

    mapping(uint256 => Listing) public listings;

    event NFTListed(uint256 tokenId, address seller, uint256 price);
    event NFTSold(uint256 tokenId, address buyer, uint256 price);
    event ListingCancelled(uint256 tokenId);

    constructor(address _nft, address _paC) Ownable2Step(msg.sender) {
        nftContract = IERC721(_nft);
        paC = IERC20(_paC);
    }

    function listNFT(uint256 tokenId, uint256 price) external {
        require(nftContract.ownerOf(tokenId) == msg.sender, "Not owner");
        require(price > 0, "Price must be > 0");

        nftContract.transferFrom(msg.sender, address(this), tokenId);

        listings[tokenId] = Listing({
            seller: msg.sender,
            price: price,
            active: true
        });

        emit NFTListed(tokenId, msg.sender, price);
    }

    function buyNFT(uint256 tokenId) external nonReentrant {
        Listing storage listing = listings[tokenId];
        require(listing.active, "Not listed");
        require(paC.transferFrom(msg.sender, listing.seller, listing.price), "PaC transfer failed");

        nftContract.transferFrom(address(this), msg.sender, tokenId);

        listing.active = false;

        emit NFTSold(tokenId, msg.sender, listing.price);
    }

    function cancelListing(uint256 tokenId) external {
        Listing storage listing = listings[tokenId];
        require(listing.seller == msg.sender, "Not seller");
        require(listing.active, "Not listed");

        nftContract.transferFrom(address(this), msg.sender, tokenId);
        listing.active = false;

        emit ListingCancelled(tokenId);
    }

    function getListing(uint256 tokenId) external view returns (address seller, uint256 price, bool active) {
        Listing memory l = listings[tokenId];
        return (l.seller, l.price, l.active);
    }
}
