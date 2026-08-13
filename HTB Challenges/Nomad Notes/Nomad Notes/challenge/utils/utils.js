const crypto = require('crypto');

function escape(str) {
  return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#39;");
}

function renderTemplate(template, data) {
  for (const key in data) {
    const value = data[key];
    const lines = template.split('\n').map(line => {
      if (line.includes(`{{ ${key} }}`)) {
        return line.replace(`{{ ${key} }}`, value);
      }
      return line;
    });
    template = lines.join('\n');
  }
  return template;
}

function generateNonce(bytes = 16) {
  if (Buffer && Buffer.from) {
    return crypto.randomBytes(bytes).toString('base64').replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
  }
  return crypto.randomBytes(bytes).toString('hex');
}

function isLoopback(addr) {
  return addr === '127.0.0.1' || addr === '::1';
}

module.exports = { escape, renderTemplate, generateNonce, isLoopback };