import { createServer } from 'http';
import { readFileSync } from 'fs';
import { spawn } from 'child_process';

const sleep = (timeout) => new Promise((resolve) => setTimeout(resolve, timeout));
const wait = (child) => new Promise((resolve) => child.on('exit', resolve));
const index = readFileSync('index.html', 'utf-8');

let token = process.env.FLAG;

const visit = async (code) => {
  const proc = spawn('node', ['bot.js', token, code], { detached: true });

  await Promise.race([
    wait(proc),
    sleep(10000),
  ]);

  if (proc.exitCode === null) {
    process.kill(-proc.pid);
  }
};

const server = createServer(async (req, res) => {
  const url = new URL(req.url, 'http://localhost/');
  
  if (url.pathname === '/') {
    res.end(index);
  } else if (url.pathname === '/bot') {
      const code = url.searchParams.get('code');
      if (!code || code.length > 120) {
        res.end('no');
      } else {
        visit(code);
        res.end('visiting');
      }
    } else {
    res.end();
  }
});

server.listen(8080);