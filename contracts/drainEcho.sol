function drainEcho(address user, uint energyLost) public {
    require(gate.verifyDsound(user), "Invalid D’sound signature");
    uint memoryForce = calculateMemoryDebt(energyLost);
    mintPaCToken(user, memoryForce);
}
