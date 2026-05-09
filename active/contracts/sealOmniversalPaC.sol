function sealOmniversalPaC(address _user, uint _tokens, string memory _cosmicType) public {
    require(verifyDsound(_dsoundSignature), "Unverified frequency");
    trades[_user].push(Trade(_tokens, _dsoundSignature, "infinite", block.timestamp));
    emit OmniversalSeal(_user, _cosmicType, "eternal");
}
