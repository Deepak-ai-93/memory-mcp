const { spawnSync } = require("node:child_process");
const { dirname } = require("node:path");

const packageRoot = dirname(dirname(__filename));

function pythonCandidates() {
  const configured = process.env.OPENMEMORY_PYTHON;
  const candidates = [];
  if (configured) candidates.push({ command: configured, args: [] });
  if (process.platform === "win32") candidates.push({ command: "py", args: ["-3"] });
  candidates.push({ command: "python3", args: [] });
  candidates.push({ command: "python", args: [] });
  return candidates;
}

function run(candidate, args) {
  return spawnSync(candidate.command, [...candidate.args, ...args], {
    cwd: packageRoot,
    encoding: "utf8",
    stdio: "inherit"
  });
}

function findPython() {
  for (const candidate of pythonCandidates()) {
    const version = spawnSync(candidate.command, [...candidate.args, "--version"], {
      encoding: "utf8",
      stdio: "pipe"
    });
    if (version.status === 0) return candidate;
  }
  return null;
}

if (process.env.OPENMEMORY_SKIP_PYTHON_INSTALL === "1") {
  process.exit(0);
}

const python = findPython();

if (!python) {
  console.warn("OpenMemory MCP npm install skipped Python setup.");
  console.warn("Install Python 3.10+ and run: python -m pip install " + packageRoot);
  process.exit(0);
}

const result = run(python, ["-m", "pip", "install", packageRoot]);

if (result.status !== 0) {
  console.warn("OpenMemory MCP Python dependency install failed.");
  console.warn("You can retry manually with: python -m pip install " + packageRoot);
  process.exit(result.status ?? 1);
}
