import { interpret } from "./grid/interpreter.js";
const config = interpret(prompt);
console.log("⚙️ Config:", config);
