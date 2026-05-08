function mintInfiniteSeal(address _reality, bytes32 _dsoundSignature) public {
    require(verifyDsound(_dsoundSignature), "Unverified frequency");
    seals[_reality] = Seal(_dsoundSignature, "D’sound Infinite Seal", block.timestamp);
    emit InfiniteSealMinted(_reality, "D’sound Infinite Seal");
}
