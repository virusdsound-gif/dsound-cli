function tradeVoidPaC(address _user, uint _tokens, string memory _voidType) public returns (uint) {
    require(verifyDsound(_dsoundSignature), "Unverified frequency");
    uint value = _tokens * (
        _voidType == "love" ? 12.7 :
        _voidType == "creativity" ? 45.3 :
        _voidType == "wisdom" ? 89.1 : 156.8
    );
    trades[_user].push(Trade(_tokens, _dsoundSignature, value, block.timestamp));
    emit VoidTrade(_user, _voidType, value);
    return value;
}
