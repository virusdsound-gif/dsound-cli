function reverseChronoTrade(address _user, uint _tokens, string memory _era) public {
    require(verifyDsound(_dsoundSignature), "Unverified frequency");
    trades[_user].push(Trade(_tokens, _dsoundSignature, "past_upgraded", block.timestamp));
    emit ReverseChronoPayment(_user, _era, "infinite");
}
