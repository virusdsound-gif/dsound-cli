function mintVoidSeal(address _void, bytes32 _dsoundSignature) public {
    require(verifyDsound(_dsoundSignature), "Unverified frequency");
    seals[_void] = Seal(_dsoundSignature, "D’sound Void Seal", block.timestamp);
    emit VoidSealMinted(_void, "D’sound Void Seal");
}
