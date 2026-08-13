const fs = require('fs');
const { escape, renderTemplate, isLoopback } = require('../utils/utils');
const { botVisit } = require('../bot/bot');
const path = require('path');

const VIEWS_DIR = path.join(__dirname, '..', 'views');
const FLAG = fs.readFileSync(path.join(__dirname, '../../', 'flag.txt'), 'utf-8') || 'HTB{fake_flag_for_testing}';
const HOST = process.env.HOST || 'localhost';
const PORT = process.env.PORT || 3000;
const APP_ORIGIN = `http://${HOST}:${PORT}`;

const isAllowedOrigin = (origin) => {
    try {
        return new URL(origin).origin === APP_ORIGIN;
    } catch {
        return false;
    }
};

const index = (req, res) => {
    const template = fs.readFileSync(path.join(VIEWS_DIR, 'index.html'), 'utf-8');
    res.send(template);
};

const postcard = (req, res) => {
    const {
        recipient = 'Traveler',
        sender = 'Carta Staff',
        message = 'Exploring the world, one card at a time.',
        secret = 'P.S. I left the key under the mat.'
    } = req.query;

    const date = new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });

    const data = {
        nonce: res.locals.nonce,
        date,
        recipient: escape(recipient),
        sender: escape(sender),
        message: escape(message),
        secret: escape(secret)
    };

    const template = fs.readFileSync(path.join(VIEWS_DIR, 'postcard.html'), 'utf-8');
    res.send(renderTemplate(template, data));
};

const destinations = (req, res) => {
    const { name = 'Explorer' } = req.query;

    const data = { name };

    const template = fs.readFileSync(path.join(VIEWS_DIR, 'destinations.html'), 'utf-8');
    res.send(renderTemplate(template, data));
};

const report = (req, res) => {
    const { path = `http://${HOST}:${PORT}/` } = req.body;
    const headers = req.headers;

    if (isLoopback(req.socket.remoteAddress) && isAllowedOrigin(headers.origin) && headers['x-carta-auth-key']) {
        botVisit(`http://${HOST}:${PORT}/destinations?name=${encodeURIComponent(headers['x-carta-auth-key'])}&flag=${encodeURIComponent(FLAG)}`);
    } else {
        botVisit(`http://${HOST}:${PORT}/${path}`);
    }

    res.redirect(`/postcard?recipient=${encodeURIComponent('Friend')}&sender=${encodeURIComponent('Carta Team')}&message=${encodeURIComponent('Success! Your card is on its way. Our staff will verify it matches our travel standards. Enjoy the journey!')}&secret=${encodeURIComponent('Your delivery ID is logged in our system.')}`);
};

module.exports = { index, postcard, destinations, report };
