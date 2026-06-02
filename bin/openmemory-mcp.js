#!/usr/bin/env node

const { spawn, spawnSync } = require("node:child_process");

function pythonCandidates() {
  const configured = process.env.OPENMEMORY_PYTHON;
  const candidates = [];
  if (configured) candidates.push({ command: configured, args: [] });
  if (process.platform === "win32") candidates.push({ command: "py", args: ["-3"] });
  candidates.push({ command: "python3", args: [] });
  candidates.push({ command: "python", args: [] });
  return candidates;
}

function findPython() {
  for (const candidate of pythonCandidates()) {
    const result = spawnSync(candidate.command, [...candidate.args, "--version"], {
      encoding: "utf8",
      stdio: "pipe"
    });
    if (result.status === 0) return candidate;
  }
  return null;
}

const python = findPython();

if (!python) {
  console.error("OpenMemory MCP requires Python 3.10 or newer.");
  console.error("Install Python, or set OPENMEMORY_PYTHON to your Python executable.");
  process.exit(1);
}

const child = spawn(python.command, [...python.args, "-m", "openmemory_mcp", ...process.argv.slice(2)], {
  env: process.env,
  stdio: "inherit"
});

child.on("exit", (code, signal) => {
  if (signal) process.kill(process.pid, signal);
  process.exit(code ?? 0);
});
