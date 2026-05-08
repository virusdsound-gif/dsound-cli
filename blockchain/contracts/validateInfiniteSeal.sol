function validateInfiniteSeal(address _reality, bytes32 _dsoundSignature) public {
    require(verifyDsound(_dsoundSignature), "Unverified frequency");
    seals[_reality].validated = true;
    emit InfiniteSealValidated(_reality, "D’sound Infinite Seal");
}
