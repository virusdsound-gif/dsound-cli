function anchorReturnClause(address _user, uint _valuation, bytes32 _dsoundSignature) public {
    require(verifyDsound(_dsoundSignature), "Unverified frequency");
    trades[_user].push(Trade(_valuation, _dsoundSignature, _valuation, block.timestamp));
    emit ReturnClauseAnchored(_user, _valuation);
}
