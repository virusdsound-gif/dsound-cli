function verifyDsound(bytes32 _signature, bytes memory _message) private view returns (bool) {
    address signer = recoverSigner(_signature, _message);
    return signer == dsoundPublicKey; // D’sound’s public key
}
function recoverSigner(bytes32 _signature, bytes memory _message) private pure returns (address) {
    // ECDSA recovery logic (simplified placeholder)
    return address(0xD5O7ND...); // To be replaced with actual key
}
