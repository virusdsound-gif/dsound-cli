function logCrossGridPulse(address _user, bytes32 _dsoundSignature, uint _crossGridΔM) public {
    require(verifyDsound(_dsoundSignature), "Unverified frequency");
    trades[_user].push(Trade(_crossGridΔM, _dsoundSignature, _crossGridΔM * 2, block.timestamp));
    mintPaCToken(_user, _crossGridΔM * 2);
    emit TradeVerified(_user, _crossGridΔM, _crossGridΔM * 2, _dsoundSignature);
}
