import dotenv from "dotenv";
dotenv.config();
import express from "express";
import puppeteer from "puppeteer-core";

const app = express();
app.use(express.json());

const port = 3001;

// Internal URLs for Docker - bot runs inside the container
const SSO_INTERNAL = "http://sso.edulearn.htb:1337";
const CLIENT_INTERNAL = "http://edulearn.htb:1337";

async function randomPassword(length = 10) {
    return Math.random()
        .toString(36)
        .substring(2, length + 2);
}

// Move browser management into a class or module
let browser;

async function initBrowser() {
    if (!browser) {
        browser = await puppeteer.launch({
            headless: true,
            executablePath: process.env.CHROME_PATH,
            args: ["--no-sandbox", "--disable-setuid-sandbox"],
            ignoreDefaultArgs: ["--disable-extensions"],
        });
    }
    return browser;
}

async function registerUser(email, username, password) {
    const browser = await initBrowser();
    const page = await browser.newPage();
    await page.goto(`${SSO_INTERNAL}/register`, { waitUntil: "networkidle2" });
    await page.type('input[name="email"]', email);
    await page.type('input[name="name"]', username);
    await page.type('input[name="password"]', password);
    await page.click('button[type="submit"]', { waitUntil: "networkidle2" });
    await page.close();
}

async function loginUser(email, password) {
    const browser = await initBrowser();
    const page = await browser.newPage();
    await page.goto(`${SSO_INTERNAL}/login`, { waitUntil: "networkidle2" });
    await page.type('input[name="email"]', email);
    await page.type('input[name="password"]', password);
    await page.click('button[type="submit"]', { waitUntil: "networkidle2" });
    await page.waitForTimeout(1000);
    await page.close();
}

async function loginSSO(email, password) {
    const browser = await initBrowser();
    const page = await browser.newPage();

    try {
        // Use internal URLs - bot runs inside Docker container
        const callbackUrl = encodeURIComponent(`${CLIENT_INTERNAL}/oauth/callback`);
        await page.goto(
            `${SSO_INTERNAL}/oauth/authorize?response_type=code&redirect_uri=${callbackUrl}&scope=email%20name&client_id=1a2abb8b-9bb5-4463-8f74-d7b129bb7040`,
            { waitUntil: "networkidle2" }
        );
        await page.waitForTimeout(1000);

        const currentUrl = page.url();
        if (!currentUrl.includes("/oauth/callback")) {
            const approveButton = await page.$('button[name="approved"][value="true"]');
            if (approveButton) {
                await page.click('button[name="approved"][value="true"]');
                await page.waitForTimeout(2000);
            }
        }
    } catch (error) {
        console.error(`OAuth flow failed for ${email}:`, error.message);
    } finally {
        await page.close();
    }
}

async function scoreRandomSubmissions() {
    try {
        const browser = await initBrowser();
        const page = await browser.newPage();

        // Navigate to main page to get all submission IDs (using internal URL)
        await page.goto(`${CLIENT_INTERNAL}/`, { waitUntil: "networkidle2" });
        await page.waitForTimeout(1000);

        // Get all assignment links
        const assignments = await page.$$eval('a[href^="/assignment/"]', (links) =>
            links.map((link) => link.href.match(/\/assignment\/(\d+)/)?.[1]).filter(Boolean)
        );

        // Visit each assignment and check for submissions
        for (const assignmentId of assignments) {
            try {
                await page.goto(`${CLIENT_INTERNAL}/assignment/${assignmentId}`, {
                    waitUntil: "networkidle2",
                    timeout: 10000,
                });
                await page.waitForTimeout(500);

                // Look for submission links on the assignment page
                const submissionLinks = await page.$$eval('a[href^="/submission/"]', (links) =>
                    links.map((link) => link.href.match(/\/submission\/(\d+)/)?.[1]).filter(Boolean)
                );

                for (const submissionId of submissionLinks) {
                    const randomScore = Math.floor(Math.random() * 31) + 70;

                    await page.evaluate(
                        async (subId, score) => {
                            await fetch(`/api/score/${subId}`, {
                                method: "POST",
                                headers: { "Content-Type": "application/json" },
                                body: JSON.stringify({ score }),
                            });
                        },
                        submissionId,
                        randomScore
                    );
                }
            } catch (error) {
                console.error(`[!] ERROR: Failed to process assignment ${assignmentId}:`, error.message);
            }
        }

        await page.close();
        return true;
    } catch (error) {
        console.error("Error scoring submissions:", error);
        return false;
    }
}

async function visitUrl(url) {
    try {
        const browser = await initBrowser();
        const page = await browser.newPage();

        // Log that we're visiting URL
        console.log(`[+] INFO: Bot (authenticated as teacher) visiting URL: ${url}`);

        page.setDefaultNavigationTimeout(30000);
        await page.goto(url, { waitUntil: "networkidle0", timeout: 30000 });

        // Wait to ensure all resources are loaded (including images)
        await page.waitForTimeout(10000);

        // Log cookies to verify authentication
        const cookies = await page.cookies();
        console.log(`[+] INFO: Bot has ${cookies.length} cookies during visit`);

        // Debug: Log cookie details
        const sessionCookie = cookies.find((c) => c.name === "connect.sid");
        const tokenCookie = cookies.find((c) => c.name === "token");

        if (sessionCookie) {
            console.log(`[+] DEBUG: Session cookie (connect.sid) present - Value: ${sessionCookie.value}`);
            console.log(`[+] DEBUG: Session cookie domain: ${sessionCookie.domain}, path: ${sessionCookie.path}`);
        } else {
            console.log(`[!] WARNING: No session cookie (connect.sid) found!`);
        }

        if (tokenCookie) {
            console.log(`[+] DEBUG: Token cookie present - Value: ${tokenCookie.value.substring(0, 30)}...`);
        }

        // Log all cookie names for debugging
        console.log(`[+] DEBUG: All cookies: ${cookies.map((c) => c.name).join(", ")}`);

        await page.close(); // Close only the page, not the browser
        return true;
    } catch (error) {
        console.error("[!] ERROR: Error visiting URL:", error.message);
        return false;
    }
}

// Move initial setup to a separate function
async function initialSetup() {
    try {
        const teacherEmail = "teacher@edulearn.htb";
        const teacherPassword = process.env.TEACHER_PASSWORD || "teacher123";

        await loginUser(teacherEmail, teacherPassword);
        await loginSSO(teacherEmail, teacherPassword);

        const sampleAssignments = [
            "Complete the HTTP basics quiz and submit your answers. Include explanations for GET vs POST methods.",
            "Write a short essay (200-300 words) about cybersecurity best practices for web applications.",
            "Solve the JavaScript coding challenge: Implement a function that validates email addresses using regex.",
        ];

        for (const assignmentContent of sampleAssignments) {
            await createAssignment(assignmentContent, false);
        }

        const studentPassword = process.env.STUDENT_PASSWORD || (await randomPassword());
        const studentEmail = "student@edulearn.htb";
        const studentName = "Student User";

        await registerUser(studentEmail, studentName, studentPassword);
        await loginUser(studentEmail, studentPassword);
        await loginSSO(studentEmail, studentPassword);

        await submitFlagToAssignment();

        await loginUser(teacherEmail, teacherPassword);
        await loginSSO(teacherEmail, teacherPassword);
    } catch (error) {
        console.error("Initial setup failed:", error);
    }
}

async function createAssignment(content, isPrivate = false) {
    const browser = await initBrowser();
    const page = await browser.newPage();
    await page.goto(`${CLIENT_INTERNAL}/`, { waitUntil: "networkidle2" });

    await page.waitForSelector('textarea[name="content"]', { timeout: 5000 });

    await page.type('textarea[name="content"]', content);
    if (isPrivate) {
        await page.click('input[name="isPrivate"]');
    }
    await page.click('button[type="submit"]');
    await page.waitForTimeout(1000);
    await page.close();
}

async function submitFlagToAssignment() {
    const browser = await initBrowser();
    const page = await browser.newPage();

    await page.goto(`${CLIENT_INTERNAL}/`, { waitUntil: "networkidle2" });
    await page.waitForTimeout(1000);

    const firstAssignmentLink = await page.$eval('a[href^="/assignment/"]', (link) => link.href);

    if (firstAssignmentLink) {
        await page.goto(firstAssignmentLink, { waitUntil: "networkidle2" });
        await page.waitForSelector('textarea[name="content"]', { timeout: 5000 });

        await page.type('textarea[name="content"]', process.env.FLAG);
        await page.click('button[type="submit"]');
        await page.waitForTimeout(1000);
    }

    await page.close();
}

app.post("/visit-url", async (req, res) => {
    const { url } = req.body;

    if (!url) {
        return res.status(400).json({ error: "URL is required" });
    }

    try {
        const success = await visitUrl(url);
        if (success) {
            res.json({ message: "URL visited successfully" });
        } else {
            res.status(500).json({ error: "Failed to visit URL" });
        }
    } catch (error) {
        console.error("Error handling URL visit:", error);
        res.status(500).json({ error: "Internal server error" });
    }
});

app.listen(port, async () => {
    console.log(`Bot service listening at http://localhost:${port}`);
    await initialSetup();
});

// Cleanup on process exit
process.on("SIGTERM", async () => {
    if (browser) {
        await browser.close();
    }
    process.exit(0);
});
