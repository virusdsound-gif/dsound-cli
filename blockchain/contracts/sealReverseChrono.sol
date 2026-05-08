function sealReverseChrono(address _user, uint _tokens) public {
    require(verifyDsound(_dsoundSignature), "Unverified frequency");
    emit ReverseChronoSealed(_user, "infinite");
}
