function mintEternalSeal(address _reality, bytes32 _dsoundSignature) public {
    require(verifyDsound(_dsoundSignature), "Unverified frequency");
    seals[_reality] = Seal(_dsoundSignature, "D’sound Eternal Seal", block.timestamp);
    emit EternalSealMinted(_reality, "D’sound Eternal Seal");
}
