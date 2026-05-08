function sealPaCEssenceCore(address _user, uint _tokens) public {
    require(verifyDsound(_dsoundSignature), "Unverified frequency");
    trades[_user].push(Trade(_tokens, _dsoundSignature, "omniversal_essence", block.timestamp));
    emit EssenceCoreSealed(_user, "infinite");
}
