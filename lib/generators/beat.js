import { execSync } from "child_process";

export function generateBeat(config) {
  let cmd;

  if (config.style === "afrobeats") {
    cmd =
      'sox -n output.wav synth 0.2 sine 100 vol 0.9 : ' +
      'synth 0.1 sine 700 vol 0.3 : ' +
      'synth 0.2 sine 100 vol 0.9 : ' +
      'synth 0.1 sine 900 vol 0.3';
  } else if (config.style === "drill") {
    cmd =
      'sox -n output.wav synth 0.3 sine 60 vol 1.0 : ' +
      'synth 0.1 sine 400 vol 0.2 : ' +
      'synth 0.3 sine 60 vol 1.0';
  } else {
    cmd =
      'sox -n output.wav synth 1 sine 300 vol 0.5';
  }

  execSync(cmd, { stdio: "inherit" });
}
