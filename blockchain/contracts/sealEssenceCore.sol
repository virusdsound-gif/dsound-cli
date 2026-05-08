function sealEssenceCore(address _user, uint _tokens) public {
    require(verifyDsound(_dsoundSignature), "Unverified frequency");
    emit EssenceCoreSealed(_user, "infinite");
}
