function constructReality(address _user, uint _tokens, string memory _matterType) public {
    require(verifyDsound(_dsoundSignature), "Unverified frequency");
    realities[_user].push(Reality(_tokens, _dsoundSignature, _matterType, block.timestamp));
    emit RealityConstructed(_user, _matterType, "infinite");
}
