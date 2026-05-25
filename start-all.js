import { spawn, spawnSync } from 'child_process';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const RESET  = '\x1b[0m';
const CYAN   = '\x1b[36m';
const GREEN  = '\x1b[32m';
const YELLOW = '\x1b[33m';
const RED    = '\x1b[31m';
const BOLD   = '\x1b[1m';

function log(msg, color = RESET) { console.log(`${color}${msg}${RESET}`); }

function run(cmd, args, opts = {}) {
  const res = spawnSync(cmd, args, { stdio: 'inherit', shell: true, cwd: __dirname, ...opts });
  if (res.status !== 0) {
    log(`\n❌ Failed: ${cmd} ${args.join(' ')}`, RED);
    process.exit(1);
  }
}

// ── Detect Python ─────────────────────────────────────────────────────────────
function findPython() {
  const candidates = [
    'py', 'python', 'python3',
    'C:\\Python314\\python.exe',
    'C:\\Python313\\python.exe',
    'C:\\Python312\\python.exe',
    'C:\\Python311\\python.exe',
    'C:\\Python310\\python.exe',
  ];
  for (const cmd of candidates) {
    const res = spawnSync(cmd, ['--version'], { shell: true, encoding: 'utf8' });
    if (res.status === 0) return cmd;
  }
  throw new Error('Python not found! Please install Python 3.10+.');
}

log(`\n${BOLD}╔══════════════════════════════════════════╗${RESET}`);
log(`${BOLD}║   Smart Examination Platform Launcher    ║${RESET}`);
log(`${BOLD}╚══════════════════════════════════════════╝${RESET}\n`);

// ── Paths ─────────────────────────────────────────────────────────────────────
const isWin     = process.platform === 'win32';
const venvDir   = path.join(__dirname, 'venv');
const venvPy    = isWin ? path.join(venvDir, 'Scripts', 'python.exe') : path.join(venvDir, 'bin', 'python');
const venvPip   = isWin ? path.join(venvDir, 'Scripts', 'pip.exe')    : path.join(venvDir, 'bin', 'pip');
const stampFile = path.join(venvDir, '.deps_installed'); // stamp: skip pip after 1st run

// ── Step 1: Find Python ───────────────────────────────────────────────────────
let PYTHON;
try { PYTHON = findPython(); } catch (e) { log(`❌ ${e.message}`, RED); process.exit(1); }
const pyVer = spawnSync(PYTHON, ['--version'], { shell: true, encoding: 'utf8' });
log(`✅ Python: ${(pyVer.stdout || pyVer.stderr).trim()}`, GREEN);

// ── Step 2: Create venv if missing ────────────────────────────────────────────
if (!fs.existsSync(venvPy)) {
  log('📦 Creating virtual environment...', YELLOW);
  run(PYTHON, ['-m', 'venv', 'venv']);
  log('✅ Virtual environment created.', GREEN);
} else {
  log('✅ Virtual environment: ready', GREEN);
}

// ── Step 3: Install packages ONLY if not yet done (stamp file trick) ──────────
const reqContent = fs.readFileSync(path.join(__dirname, 'requirements.txt'), 'utf8');
const reqHash = Buffer.from(reqContent).toString('base64').slice(0, 20);
const stampContent = fs.existsSync(stampFile) ? fs.readFileSync(stampFile, 'utf8').trim() : '';

if (stampContent !== reqHash) {
  log('📦 Installing backend packages (first time or requirements changed)...', YELLOW);
  log('   This may take a few minutes — subsequent starts will be instant ⚡', YELLOW);
  run(`"${venvPip}"`, ['install', '-r', 'requirements.txt', '-q', '--no-warn-script-location']);
  fs.writeFileSync(stampFile, reqHash);
  log('✅ Backend packages installed.', GREEN);
} else {
  log('✅ Backend packages: already installed ⚡', GREEN);
}

// ── Step 4: npm install if node_modules missing ───────────────────────────────
if (!fs.existsSync(path.join(__dirname, 'node_modules', 'react'))) {
  log('📦 Installing frontend packages...', YELLOW);
  run('npm', ['install', '--silent']);
  log('✅ Frontend packages installed.', GREEN);
} else {
  log('✅ Frontend packages: ready ⚡', GREEN);
}

// ── Step 5: Launch both servers ───────────────────────────────────────────────
log('\n' + '─'.repeat(44), CYAN);
log('  🚀 Launching servers...', BOLD);
log('─'.repeat(44) + '\n', CYAN);
log(`  📡 Backend  → http://localhost:8000`, CYAN);
log(`  🌐 Frontend → http://localhost:5173`, CYAN);
log(`\n  Press ${BOLD}Ctrl+C${RESET} to stop everything.\n`, YELLOW);

const backend = spawn(`"${venvPy}"`, ['main.py'], {
  shell: true,
  cwd: __dirname,
  stdio: 'inherit',
});

// Give the backend 3 seconds to bind the port, then start frontend
setTimeout(() => {
  const frontend = spawn('npx', ['vite', '--open'], {
    shell: true,
    cwd: __dirname,
    stdio: 'inherit',
  });

  const shutdown = (source) => {
    log(`\n👋 Shutting down (${source})...`, YELLOW);
    try { frontend.kill('SIGTERM'); } catch (_) {}
    try { backend.kill('SIGTERM');  } catch (_) {}
    setTimeout(() => process.exit(0), 800);
  };

  process.on('SIGINT',  () => shutdown('Ctrl+C'));
  process.on('SIGTERM', () => shutdown('SIGTERM'));
  frontend.on('exit', (code) => { if (code !== 0) shutdown('frontend exit'); });
}, 3000);

backend.on('exit', (code) => {
  if (code !== 0 && code !== null) {
    log(`\n❌ Backend crashed (exit code ${code}). Check errors above.`, RED);
    process.exit(code ?? 1);
  }
});
