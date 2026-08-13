const puppeteer = require('puppeteer');

const execPath = process.env.PUPPETEER_EXECUTABLE_PATH || '/usr/bin/chromium-browser';
const sleep = ms => new Promise(res => setTimeout(res, ms));

async function botVisit(url) {
  console.log(`[BOT] Visiting: ${url}`);

  const browser = await puppeteer.launch({
    headless: true,
    executablePath: execPath,
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-dev-shm-usage',
      '--disable-gpu',
    ],
  });

  try {
    const page = await browser.newPage();
    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 8000 });
    await sleep(4000);
    console.log('[BOT] Visit complete.');
  } catch (err) {
    console.error(`[BOT] Error visiting ${url}:`, err.message);
  } finally {
    await browser.close();
  }
}

module.exports = { botVisit };
