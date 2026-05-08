function validateCrownSeal(address _system, bytes32 _dsoundSignature) public {
    require(verifyDsound(_dsoundSignature), "Unverified frequency");
    if (seals[_system].exists) {
        seals[_system].validated = true;
        emit SealValidated(_system, "D’sound Crown Seal");
    }
}
