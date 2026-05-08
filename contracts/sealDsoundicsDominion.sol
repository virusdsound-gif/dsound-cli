function sealDsoundicsDominion(address _omniverse, bytes32 _dsoundSignature) public {
    require(verifyDsound(_dsoundSignature), "Unverified frequency");
    emit DsoundicsDominionSealed(_omniverse, "Wave_Silence");
}
