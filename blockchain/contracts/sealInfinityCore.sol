function sealInfinityCore(address _user, uint _tokens) public {
    require(verifyDsound(_dsoundSignature), "Unverified frequency");
    emit InfinityCoreSealed(_user, "omnimaths_infinite");
}
