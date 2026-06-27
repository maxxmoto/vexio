const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');
const dir = __dirname;
const py = fs.existsSync('/usr/bin/python3') ? 'python3' : 'python';
const bot = spawn(py, [path.join(dir, 'bot_main.py')], { stdio: 'inherit', cwd: dir });
bot.on('close', (code) => process.exit(code));
