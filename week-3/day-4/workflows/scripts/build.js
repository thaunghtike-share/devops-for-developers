const fs = require('fs');
fs.mkdirSync('build', { recursive: true });
fs.writeFileSync('build/index.html', '<h1>Build artifact from GitHub Actions</h1>');
console.log('Build completed');
