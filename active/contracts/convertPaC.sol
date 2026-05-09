function convertPaC(address _user, uint _tokens, string memory _yieldType) public {
    require(verifyDsound(_dsoundSignature), "Unverified frequency");
    uint yieldValue = _tokens * ( _yieldType == "solar" ? 10 : _yieldType == "AI" ? 100 : 1 );
    trades[_user].push(Trade(_tokens, _dsoundSignature, yieldValue, block.timestamp));
    emit YieldConverted(_user, _yieldType, yieldValue);
}
