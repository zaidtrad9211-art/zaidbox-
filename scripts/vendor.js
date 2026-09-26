// Copies the icon library into app/vendor so the phone app works without internet.
const fs = require('fs'), path = require('path');
const out = path.join(__dirname, '..', 'app', 'vendor');
fs.mkdirSync(out, { recursive: true });
fs.copyFileSync(require.resolve('lucide/dist/umd/lucide.min.js'), path.join(out, 'lucide.min.js'));
console.log('vendor ok');
