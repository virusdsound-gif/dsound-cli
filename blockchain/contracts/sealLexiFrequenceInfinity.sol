function sealLexiFrequenceInfinity(address _user, uint _tokens, string memory _wave_word) public {
    require(verifyDsound(_dsoundSignature), "Unverified frequency");
    emit LexiFrequenceSealed(_user, _wave_word, "infinite");
}
