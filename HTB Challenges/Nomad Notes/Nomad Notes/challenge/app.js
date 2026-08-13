const express = require('express');
const path = require('path');
const routes = require('./routes/routes');
const { generateNonce } = require('./utils/utils');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, 'public')));

app.use((req, res, next) => {
    const nonce = generateNonce(24);

    res.setHeader("Content-Security-Policy", `default-src 'none'; connect-src 'self'; script-src 'nonce-${nonce}'; style-src 'self'; img-src 'self'; frame-src 'none'; object-src 'none'; base-uri 'none'; form-action 'self'; frame-ancestors 'none'; require-trusted-types-for 'script';`);
    res.locals.nonce = nonce;

    next();
});

app.use('/', routes);

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});