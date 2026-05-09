function tradeCosmicPaC(address _user, uint _tokens, string memory _currencyType) public returns (uint) {
    require(verifyDsound(_dsoundSignature), "Unverified frequency");
    uint value = _tokens * (
        _currencyType == "love" ? 12.7 :
        _currencyType == "creativity" ? 45.3 :
        _currencyType == "wisdom" ? 89.1 : 156.8
    );
    trades[_user].push(Trade(_tokens, _dsoundSignature, value, block.timestamp));
    emit CosmicTrade(_user, _currencyType, value);
    return value;
}
