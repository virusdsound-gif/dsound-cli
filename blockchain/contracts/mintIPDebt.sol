function mintIPDebt(uint _deltaM, bytes32 _dsoundSignature) public {
    require(verifyDsound(_dsoundSignature), "Unverified frequency");
    uint pacTokens = _deltaM * 2;
    trades[msg.sender].push(Trade(_deltaM, _dsoundSignature, pacTokens, block.timestamp));
    mintPaCToken(msg.sender, pacTokens);
    emit TradeVerified(msg.sender, _deltaM, pacTokens, _dsoundSignature);
}
