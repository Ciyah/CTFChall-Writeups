const express = require("express");
const session = require("express-session");
const passport = require("passport");
const OAuth2Strategy = require("passport-oauth2");
const sanitizeHtml = require("sanitize-html");
const fetch = require("node-fetch");
require("dotenv").config();

// Validate required environment variables
if (!process.env.CLIENT_SECRET) {
    console.error("ERROR: CLIENT_SECRET environment variable is required");
    process.exit(1);
}

if (!process.env.SESSION_SECRET) {
    console.error("ERROR: SESSION_SECRET environment variable is required");
    process.exit(1);
}

const app = express();
const port = 3000;

const SSO_INTERNAL = "http://127.0.0.1:3002";

const assignments = [];

// In-memory storage for submissions (student work on assignments)
const submissions = [];

// In-memory storage for features
const reactions = {}; // { itemId: { emoji: count } } - works for both assignments and submissions
const bookmarks = {}; // { userEmail: [itemIds] }
const itemViews = {}; // { itemId: viewCount }
const userProfiles = {}; // { userEmail: { avatar, bio, displayName } }

passport.use(
    new OAuth2Strategy(
        {
            authorizationURL: "http://placeholder/oauth/authorize",
            tokenURL: `${SSO_INTERNAL}/oauth/token`,
            clientID: "1a2abb8b-9bb5-4463-8f74-d7b129bb7040",
            clientSecret: process.env.CLIENT_SECRET,
            scope: "email name",
            callbackURL: "http://placeholder/oauth/callback",
            passReqToCallback: true,
        },
        async function (req, accessToken, refreshToken, profile, cb) {
            try {
                // Fetch user profile from the OAuth provider (using internal URL)
                const response = await fetch(`${SSO_INTERNAL}/oauth/userinfo`, {
                    headers: {
                        Authorization: `Bearer ${accessToken}`,
                    },
                });

                if (!response.ok) {
                    throw new Error("Failed to fetch user profile");
                }

                const userProfile = await response.json();

                // Return user object with profile information
                return cb(null, {
                    name: userProfile.name,
                    email: userProfile.email,
                    role: userProfile.role || "student", // Include role
                    accessToken,
                });
            } catch (error) {
                return cb(error);
            }
        }
    )
);

passport.serializeUser((user, done) => done(null, user));
passport.deserializeUser((user, done) => done(null, user));

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static("public"));
app.use(
    session({
        secret: process.env.SESSION_SECRET,
        resave: false,
        saveUninitialized: false,
    })
);
app.use(passport.initialize());
app.use(passport.session());

// Set view engine
app.set("view engine", "ejs");

// Authentication middleware
const isAuthenticated = (req, res, next) => {
    if (req.isAuthenticated()) {
        return next();
    }
    res.redirect("/login");
};

// Teacher-only middleware
const isTeacher = (req, res, next) => {
    if (req.user && req.user.role === "teacher") {
        return next();
    }
    res.status(403).render("error", { message: "Teacher access required" });
};

// Helper function to get user profile with defaults
const getUserProfile = (email, name) => {
    if (!userProfiles[email]) {
        userProfiles[email] = {
            avatar: null,
            bio: "",
            displayName: name,
        };
    }
    return userProfiles[email];
};

// Helper to get enriched user object
const getEnrichedUser = (user) => {
    const profile = getUserProfile(user.email, user.name);
    return {
        ...user,
        avatar: profile.avatar,
        bio: profile.bio,
        displayName: profile.displayName || user.name,
    };
};

// Routes
app.get("/", isAuthenticated, (req, res) => {
    // Show all assignments (public homework) and user's submissions
    const visibleAssignments = assignments.filter(
        (assignment) => !assignment.isPrivate || assignment.author.email === req.user.email
    );
    const userSubmissions = submissions.filter((sub) => sub.author.email === req.user.email);
    const enrichedUser = getEnrichedUser(req.user);
    res.render("index", { assignments: visibleAssignments, submissions: userSubmissions, user: enrichedUser });
});

app.get("/assignment/:id", isAuthenticated, (req, res) => {
    const assignment = assignments.find((a) => a.id === parseInt(req.params.id));
    if (!assignment) {
        return res.status(404).render("error", { message: "Assignment not found" });
    }
    // Check if user has permission to view this assignment
    if (assignment.isPrivate && assignment.author.email !== req.user.email) {
        return res.status(403).render("error", { message: "You do not have permission to view this assignment" });
    }

    // Get submissions based on role
    // Teachers can see all submissions, students only see their own
    let userSubmissions;
    if (req.user.role === "teacher") {
        // Teachers see all submissions for this assignment
        userSubmissions = submissions.filter((s) => s.assignmentId === assignment.id);
    } else {
        // Students only see their own submissions
        userSubmissions = submissions.filter(
            (s) => s.assignmentId === assignment.id && s.author.email === req.user.email
        );
    }

    // Get leaderboard data (only scored submissions)
    let leaderboard = submissions
        .filter((s) => s.assignmentId === assignment.id && s.score !== null)
        .map((s) => ({
            id: s.id,
            author: s.author.name, // Show actual student names
            email: req.user.role === "teacher" ? s.author.email : null,
            score: s.score,
            timestamp: s.timestamp,
            isCurrentUser: s.author.email === req.user.email,
        }))
        .sort((a, b) => b.score - a.score) // Sort by score descending
        .slice(0, 10); // Top 10

    const enrichedUser = getEnrichedUser(req.user);
    res.render("assignment", { assignment, userSubmissions, leaderboard, user: enrichedUser });
});

// View a specific submission (author or teacher can view)
app.get("/submission/:id", isAuthenticated, (req, res) => {
    const submission = submissions.find((s) => s.id === parseInt(req.params.id));
    if (!submission) {
        return res.status(404).render("error", { message: "Submission not found" });
    }
    // Check if user has permission to view this submission (author or teacher)
    if (submission.author.email !== req.user.email && req.user.role !== "teacher") {
        return res.status(403).render("error", { message: "You do not have permission to view this submission" });
    }
    const enrichedUser = getEnrichedUser(req.user);
    res.render("submission", { submission, user: enrichedUser });
});

// Submit an assignment solution
app.post("/submit", isAuthenticated, (req, res) => {
    const { assignmentId, content } = req.body;
    if (!assignmentId || !content) {
        return res.status(400).render("error", { message: "Assignment ID and content are required" });
    }

    const assignment = assignments.find((a) => a.id === parseInt(assignmentId));
    if (!assignment) {
        return res.status(404).render("error", { message: "Assignment not found" });
    }

    const sanitizedContent = sanitizeHtml(content, {
        allowedTags: ["img", "h3", "p", "strong", "em", "ul", "li", "br", "code", "pre"],
        allowedAttributes: {
            img: ["src", "alt"],
        },
    });

    const profile = getUserProfile(req.user.email, req.user.name);
    const submission = {
        id: Date.now(),
        assignmentId: parseInt(assignmentId),
        content: sanitizedContent,
        author: {
            email: req.user.email,
            name: profile.displayName || req.user.name,
            avatar: profile.avatar,
        },
        timestamp: new Date().toISOString(),
        score: null, // Initially null, will be scored after 10 seconds
    };
    submissions.unshift(submission);

    // Auto-score after 10 seconds
    setTimeout(() => {
        const sub = submissions.find((s) => s.id === submission.id);
        if (sub) {
            sub.score = Math.floor(Math.random() * 31) + 70; // Random 70-100
            console.log(`[+] Submission ${submission.id} scored: ${sub.score}/100`);
        }
    }, 10000); // 10 seconds delay

    res.redirect(`/assignment/${assignmentId}`);
});

app.get("/submit-url", isAuthenticated, (req, res) => {
    const enrichedUser = getEnrichedUser(req.user);
    res.render("submit-url", { user: enrichedUser });
});

// Profile routes
app.get("/profile", isAuthenticated, (req, res) => {
    const enrichedUser = getEnrichedUser(req.user);
    res.render("profile", { user: enrichedUser, success: req.query.success });
});

app.post("/profile", isAuthenticated, (req, res) => {
    const { avatar, bio, displayName } = req.body;
    const userEmail = req.user.email;

    // Validate and sanitize inputs
    const profile = getUserProfile(userEmail, req.user.name);

    if (displayName && displayName.trim().length > 0) {
        profile.displayName = sanitizeHtml(displayName.trim(), {
            allowedTags: [],
            allowedAttributes: {},
        }).substring(0, 100);
    }

    if (bio !== undefined) {
        profile.bio = sanitizeHtml(bio.trim(), {
            allowedTags: [],
            allowedAttributes: {},
        }).substring(0, 500);
    }

    if (avatar !== undefined) {
        // Validate avatar URL
        const avatarUrl = avatar.trim();
        if (avatarUrl === "" || avatarUrl.match(/^https?:\/\/.+/)) {
            profile.avatar = avatarUrl || null;
        }
    }

    userProfiles[userEmail] = profile;
    res.redirect("/profile?success=true");
});

app.post("/submit-url", isAuthenticated, async (req, res) => {
    const { url } = req.body;
    if (!url) {
        return res.status(400).render("error", { message: "URL is required" });
    }

    try {
        // Send URL to bot service
        const response = await fetch("http://localhost:3001/visit-url", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ url }),
        });

        if (!response.ok) {
            throw new Error("Failed to submit URL to bot");
        }

        res.redirect("/submit-url?success=true");
    } catch (error) {
        console.error("Error submitting URL:", error);
        res.status(500).render("error", { message: "Failed to submit URL to bot" });
    }
});

app.get("/login", (req, res) => {
    res.render("login");
});

app.get("/auth", (req, res, next) => {
    const host = req.get("Host") || "edulearn.htb";
    const protocol = req.get("X-Forwarded-Proto") || "http";

    const portMatch = host.match(/:(\d+)$/);
    const port = portMatch ? portMatch[1] : "";
    const portSuffix = port ? `:${port}` : "";

    const ssoHost = `sso.edulearn.htb${portSuffix}`;
    const appHost = `edulearn.htb${portSuffix}`;

    const strategy = passport._strategies.oauth2;
    strategy._oauth2._authorizeUrl = `${protocol}://${ssoHost}/oauth/authorize`;
    strategy._callbackURL = `${protocol}://${appHost}/oauth/callback`;

    passport.authenticate("oauth2")(req, res, next);
});

app.get("/oauth/callback", passport.authenticate("oauth2", { failureRedirect: "/login" }), (req, res) => {
    res.redirect("/");
});

app.post("/assignment", isAuthenticated, isTeacher, (req, res) => {
    const { content, isPrivate } = req.body;
    if (content) {
        const sanitizedContent = sanitizeHtml(content, {
            allowedTags: ["img", "h3", "p", "strong", "em", "ul", "li", "br"],
            allowedAttributes: {
                img: ["src", "alt"],
            },
        });

        const profile = getUserProfile(req.user.email, req.user.name);
        assignments.unshift({
            id: Date.now(),
            content: sanitizedContent,
            author: {
                email: req.user.email,
                name: profile.displayName || req.user.name,
                avatar: profile.avatar,
            },
            timestamp: new Date().toISOString(),
            isPrivate: isPrivate === "on", // Convert checkbox value to boolean
        });
    }
    res.redirect("/");
});

app.get("/logout", (req, res) => {
    req.logout(() => {
        res.redirect("/login");
    });
});

// ===== API ROUTES =====

// Get reactions for an item (assignment or submission)
app.get("/api/reactions/:itemId", (req, res) => {
    const itemId = req.params.itemId;
    res.json(reactions[itemId] || {});
});

// Add reaction to an item
app.post("/api/reactions/:itemId", isAuthenticated, (req, res) => {
    const itemId = req.params.itemId;
    const { emoji } = req.body;

    const allowedEmojis = ["👍", "❤️", "🤔", "🎯", "🔥"];
    if (!emoji || !allowedEmojis.includes(emoji)) {
        return res.status(400).json({ error: "Invalid emoji" });
    }

    if (!reactions[itemId]) {
        reactions[itemId] = {};
    }

    reactions[itemId][emoji] = (reactions[itemId][emoji] || 0) + 1;
    res.json({ success: true, reactions: reactions[itemId] });
});

// Get user's bookmarks
app.get("/api/bookmarks", isAuthenticated, (req, res) => {
    const userEmail = req.user.email;
    res.json(bookmarks[userEmail] || []);
});

// Toggle bookmark
app.post("/api/bookmarks/:itemId", isAuthenticated, (req, res) => {
    const userEmail = req.user.email;
    const itemId = req.params.itemId;

    if (!bookmarks[userEmail]) {
        bookmarks[userEmail] = [];
    }

    const index = bookmarks[userEmail].indexOf(itemId);
    if (index > -1) {
        bookmarks[userEmail].splice(index, 1);
        res.json({ success: true, bookmarked: false });
    } else {
        bookmarks[userEmail].push(itemId);
        res.json({ success: true, bookmarked: true });
    }
});

// Track item view
app.post("/api/views/:itemId", isAuthenticated, (req, res) => {
    const itemId = req.params.itemId;
    itemViews[itemId] = (itemViews[itemId] || 0) + 1;
    res.json({ success: true, views: itemViews[itemId] });
});

// Get item statistics
app.get("/api/stats/:itemId", (req, res) => {
    const itemId = req.params.itemId;
    res.json({
        views: itemViews[itemId] || 0,
        reactions: reactions[itemId] || {},
        totalReactions: Object.values(reactions[itemId] || {}).reduce((a, b) => a + b, 0),
    });
});

// Get user statistics
app.get("/api/user/stats", isAuthenticated, (req, res) => {
    const userEmail = req.user.email;
    const userAssignments = assignments.filter((a) => a.author.email === userEmail);
    const userSubmissions = submissions.filter((s) => s.author.email === userEmail);

    let totalViews = 0;
    let totalReactions = 0;
    let totalScore = 0;
    let scoredSubmissions = 0;

    userAssignments.forEach((assignment) => {
        totalViews += itemViews[assignment.id] || 0;
        const assignmentReactions = reactions[assignment.id] || {};
        totalReactions += Object.values(assignmentReactions).reduce((a, b) => a + b, 0);
    });

    userSubmissions.forEach((submission) => {
        if (submission.score !== null) {
            totalScore += submission.score;
            scoredSubmissions++;
        }
    });

    res.json({
        assignments: userAssignments.length,
        submissions: userSubmissions.length,
        views: totalViews,
        reactions: totalReactions,
        bookmarks: (bookmarks[userEmail] || []).length,
        averageScore: scoredSubmissions > 0 ? Math.round(totalScore / scoredSubmissions) : 0,
    });
});

// Get trending assignments (most viewed/reacted)
app.get("/api/assignments/trending", isAuthenticated, (req, res) => {
    const visibleAssignments = assignments.filter(
        (assignment) => !assignment.isPrivate || assignment.author.email === req.user.email
    );

    const assignmentsWithScore = visibleAssignments.map((assignment) => {
        const views = itemViews[assignment.id] || 0;
        const assignmentReactions = reactions[assignment.id] || {};
        const totalReactions = Object.values(assignmentReactions).reduce((a, b) => a + b, 0);

        return {
            ...assignment,
            score: views + totalReactions * 2,
            views,
            totalReactions,
        };
    });

    assignmentsWithScore.sort((a, b) => b.score - a.score);
    res.json(assignmentsWithScore.slice(0, 5));
});

// Get user profile
app.get("/api/profile", isAuthenticated, (req, res) => {
    const enrichedUser = getEnrichedUser(req.user);
    res.json({
        email: enrichedUser.email,
        name: enrichedUser.name,
        displayName: enrichedUser.displayName,
        avatar: enrichedUser.avatar,
        bio: enrichedUser.bio,
    });
});

// Search assignments API
app.get("/api/assignments/search", isAuthenticated, (req, res) => {
    const query = (req.query.q || "").toLowerCase();
    const visibleAssignments = assignments.filter(
        (assignment) => !assignment.isPrivate || assignment.author.email === req.user.email
    );

    if (!query) {
        return res.json(visibleAssignments);
    }

    const filtered = visibleAssignments.filter((assignment) => {
        const content = assignment.content.toLowerCase();
        const author = assignment.author.name.toLowerCase();
        return content.includes(query) || author.includes(query);
    });

    res.json(filtered);
});

// Bot endpoint to score a submission
app.post("/api/score/:submissionId", isAuthenticated, (req, res) => {
    const { score } = req.body;
    const submissionId = parseInt(req.params.submissionId);

    const submission = submissions.find((s) => s.id === submissionId);
    if (!submission) {
        return res.status(404).json({ error: "Submission not found" });
    }

    submission.score = score;
    res.json({ success: true, score: submission.score });
});

app.listen(port, () => {
    console.log(`App listening at http://localhost:${port}`);
});
