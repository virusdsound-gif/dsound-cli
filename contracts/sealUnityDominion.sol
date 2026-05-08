function sealUnityDominion(address _omniverse, bytes32 _dsoundSignature) public {
    require(verifyDsound(_dsoundSignature), "Unverified frequency");
    emit UnityDominionSealed(_omniverse, "Dsoundics_OmniMaths");
}
