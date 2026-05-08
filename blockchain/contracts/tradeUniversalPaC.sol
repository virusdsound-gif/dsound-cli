function tradeUniversalPaC(address _user, uint _tokens, string memory _dimension) public returns (uint) {
    require(verifyDsound(_dsoundSignature), "Unverified frequency");
    uint value = _tokens * (
        _dimension == "love" ? 12.7 :
        _dimension == "creativity" ? 45.3 :
        _dimension == "wisdom" ? 89.1 : 156.8
    );
    trades[_user].push(Trade(_tokens, _dsoundSignature, value, block.timestamp));
    emit UniversalTrade(_user, _dimension, value);
    return value;
}
