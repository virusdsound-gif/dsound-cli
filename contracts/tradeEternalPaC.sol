function tradeEternalPaC(address _user, uint _tokens, string memory _cosmicType) public returns (uint) {
    require(verifyDsound(_dsoundSignature), "Unverified frequency");
    uint value = _tokens * (
        _cosmicType == "love" ? 12.7 :
        _cosmicType == "creativity" ? 45.3 :
        _cosmicType == "wisdom" ? 89.1 : 156.8
    );
    trades[_user].push(Trade(_tokens, _dsoundSignature, value, block.timestamp));
    emit EternalTrade(_user, _cosmicType, value);
    return value;
}
