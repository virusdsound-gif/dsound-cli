function calculateCrownAuthority(uint psiE, uint suppression, uint interference) public pure returns (uint) {
    uint omega = 144; // Ω = 1.44 (scaled for solidity)
    return (psiE ** omega) / (suppression * interference);
}
