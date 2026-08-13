// Dark Mode Toggle (UI preference - client-side only)
function initDarkMode() {
    const isDark = localStorage.getItem("darkMode") === "true";
    if (isDark) {
        document.body.classList.add("dark-mode");
        updateDarkModeButton(true);
    }
}

function toggleDarkMode() {
    const isDark = document.body.classList.toggle("dark-mode");
    localStorage.setItem("darkMode", isDark);
    updateDarkModeButton(isDark);
    showToast(isDark ? "🌙 Dark mode enabled" : "☀️ Light mode enabled");
}

function updateDarkModeButton(isDark) {
    const btn = document.getElementById("darkModeBtn");
    if (btn) {
        btn.innerHTML = isDark
            ? '<span class="iconify h-5 w-5" data-icon="ph:sun-bold"></span>'
            : '<span class="iconify h-5 w-5" data-icon="ph:moon-bold"></span>';
    }
}

// Item Reactions (Server-side with API) - works for both assignments and submissions
async function initReactions() {
    const assignmentCards = document.querySelectorAll("[data-assignment-id]");
    const submissionCards = document.querySelectorAll("[data-submission-id]");

    for (const card of assignmentCards) {
        const itemId = card.getAttribute("data-assignment-id");
        if (itemId) {
            await loadReactions(itemId);
        }
    }

    for (const card of submissionCards) {
        const itemId = card.getAttribute("data-submission-id");
        if (itemId) {
            await loadReactions(itemId);
        }
    }
}

async function loadReactions(itemId) {
    try {
        const response = await fetch(`/api/reactions/${itemId}`);
        const reactions = await response.json();
        updateReactionDisplay(itemId, reactions);
    } catch (error) {
        console.error("Failed to load reactions:", error);
    }
}

async function addReaction(itemId, emoji) {
    try {
        const response = await fetch(`/api/reactions/${itemId}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ emoji }),
        });

        const data = await response.json();
        if (data.success) {
            updateReactionDisplay(itemId, data.reactions);
            showToast(`Reacted with ${emoji}`);
        }
    } catch (error) {
        console.error("Failed to add reaction:", error);
        showToast("❌ Failed to add reaction");
    }
}

function updateReactionDisplay(itemId, reactions) {
    const container = document.getElementById(`reactions-${itemId}`);
    if (container) {
        let html = "";
        Object.entries(reactions).forEach(([emoji, count]) => {
            html += `<span class="reaction-badge">${emoji} ${count}</span>`;
        });
        container.innerHTML = html;
    }
}

// Search Assignments (Server-side API)
let searchTimeout;
async function searchAssignments(query) {
    clearTimeout(searchTimeout);

    // Debounce search
    searchTimeout = setTimeout(async () => {
        try {
            const response = await fetch(`/api/assignments/search?q=${encodeURIComponent(query)}`);
            const filteredAssignments = await response.json();

            // Update UI with filtered results
            const assignments = document.querySelectorAll(".assignment-card");
            let visibleCount = 0;

            assignments.forEach((assignment) => {
                const assignmentId = assignment
                    .querySelector("[data-assignment-id]")
                    ?.getAttribute("data-assignment-id");
                const isVisible = filteredAssignments.some((a) => a.id.toString() === assignmentId);

                if (query === "" || isVisible) {
                    assignment.style.display = "";
                    assignment.style.animation = "fadeIn 0.3s ease-out";
                    visibleCount++;
                } else {
                    assignment.style.display = "none";
                }
            });

            const noResults = document.getElementById("no-search-results");
            if (noResults) {
                noResults.style.display = visibleCount === 0 && query !== "" ? "block" : "none";
            }
        } catch (error) {
            console.error("Search failed:", error);
        }
    }, 300);
}

// View Mode Toggle (Grid/List)
function toggleViewMode() {
    const container = document.querySelector(".assignments-container");
    if (!container) return;

    const currentMode = localStorage.getItem("viewMode") || "list";
    const newMode = currentMode === "list" ? "grid" : "list";

    container.className = `assignments-container view-${newMode}`;
    localStorage.setItem("viewMode", newMode);

    const btn = document.getElementById("viewModeBtn");
    if (btn) {
        btn.innerHTML =
            newMode === "grid"
                ? '<span class="iconify h-5 w-5" data-icon="ph:list-bold"></span>'
                : '<span class="iconify h-5 w-5" data-icon="ph:grid-four-bold"></span>';
    }

    showToast(newMode === "grid" ? "📱 Grid view" : "📋 List view");
}

function initViewMode() {
    const mode = localStorage.getItem("viewMode") || "list";
    const container = document.querySelector(".assignments-container");
    if (container) {
        container.className = `assignments-container view-${mode}`;
    }
}

// Statistics Counter Animation
function animateStats() {
    const stats = document.querySelectorAll(".stat-number");
    stats.forEach((stat) => {
        const target = parseInt(stat.getAttribute("data-value") || stat.textContent);
        let current = 0;
        const increment = target / 50;
        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                stat.textContent = target;
                clearInterval(timer);
            } else {
                stat.textContent = Math.floor(current);
            }
        }, 20);
    });
}

// Toast Notifications
function showToast(message, duration = 3000) {
    const toast = document.createElement("div");
    toast.className = "toast-notification";
    toast.textContent = message;
    document.body.appendChild(toast);

    setTimeout(() => toast.classList.add("show"), 100);

    setTimeout(() => {
        toast.classList.remove("show");
        setTimeout(() => toast.remove(), 300);
    }, duration);
}

// Reading Time Estimator
function estimateReadingTime() {
    document.querySelectorAll(".assignment-content, .submission-content").forEach((content) => {
        const text = content.textContent;
        const words = text.trim().split(/\s+/).length;
        const minutes = Math.ceil(words / 200); // Average reading speed

        const container = content.closest(".assignment-card, .submission-card");
        if (container) {
            const badge = document.createElement("span");
            badge.className = "reading-time-badge";
            badge.innerHTML = `<span class="iconify h-3 w-3" data-icon="ph:book-open-bold"></span> ${minutes} min read`;

            const existingBadge = container.querySelector(".reading-time-badge");
            if (!existingBadge) {
                const metaContainer = container.querySelector(".assignment-meta, .submission-meta");
                if (metaContainer) {
                    metaContainer.appendChild(badge);
                }
            }
        }
    });
}

// Character Counter for New Post
function initCharCounter() {
    const textarea = document.querySelector('textarea[name="content"]');
    if (!textarea) return;

    const counter = document.createElement("div");
    counter.className = "char-counter";
    counter.innerHTML = '<span class="current">0</span> / <span class="max">5000</span> characters';
    textarea.parentNode.insertBefore(counter, textarea.nextSibling);

    textarea.addEventListener("input", function () {
        const current = this.value.length;
        counter.querySelector(".current").textContent = current;
        counter.className = current > 4500 ? "char-counter warning" : "char-counter";
    });
}

// Item Bookmarks (Server-side with API)
async function toggleBookmark(itemId) {
    try {
        const response = await fetch(`/api/bookmarks/${itemId}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
        });

        const data = await response.json();
        if (data.success) {
            showToast(data.bookmarked ? "📌 Bookmarked!" : "📌 Bookmark removed");
            await updateBookmarkButtons();
        }
    } catch (error) {
        console.error("Failed to toggle bookmark:", error);
        showToast("❌ Failed to update bookmark");
    }
}

async function updateBookmarkButtons() {
    try {
        const response = await fetch("/api/bookmarks");
        const bookmarks = await response.json();

        document.querySelectorAll(".bookmark-btn").forEach((btn) => {
            const itemId = btn.getAttribute("data-item-id");
            const isBookmarked = bookmarks.includes(itemId);
            btn.innerHTML = isBookmarked
                ? '<span class="iconify h-4 w-4 text-amber-500" data-icon="ph:bookmark-simple-fill"></span>'
                : '<span class="iconify h-4 w-4" data-icon="ph:bookmark-simple-bold"></span>';
        });
    } catch (error) {
        console.error("Failed to load bookmarks:", error);
    }
}

// Activity Tracker (Server-side)
async function trackActivity() {
    try {
        const response = await fetch("/api/user/stats");
        const stats = await response.json();
        updateStatsDisplay(stats);
    } catch (error) {
        console.error("Failed to load stats:", error);
    }
}

function updateStatsDisplay(stats) {
    const statsEl = document.getElementById("user-stats");
    if (statsEl) {
        statsEl.innerHTML = `
            <div class="stat-item">
                <span class="iconify h-5 w-5" data-icon="ph:book-bold"></span>
                <div class="flex-1">
                    <span class="stat-number">${stats.assignments || 0}</span>
                    <span class="ml-1">assignments</span>
                </div>
            </div>
            <div class="stat-item">
                <span class="iconify h-5 w-5" data-icon="ph:file-text-bold"></span>
                <div class="flex-1">
                    <span class="stat-number">${stats.submissions || 0}</span>
                    <span class="ml-1">submissions</span>
                </div>
            </div>
            <div class="stat-item">
                <span class="iconify h-5 w-5" data-icon="ph:medal-bold"></span>
                <div class="flex-1">
                    <span class="stat-number">${stats.averageScore || 0}</span>
                    <span class="ml-1">avg score</span>
                </div>
            </div>
            <div class="stat-item">
                <span class="iconify h-5 w-5" data-icon="ph:bookmark-simple-bold"></span>
                <div class="flex-1">
                    <span class="stat-number">${stats.bookmarks || 0}</span>
                    <span class="ml-1">bookmarks</span>
                </div>
            </div>
        `;
    }
}

// Track post view
async function trackPostView(postId) {
    try {
        await fetch(`/api/views/${postId}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
        });
    } catch (error) {
        console.error("Failed to track view:", error);
    }
}

// Smooth Scroll
function smoothScrollTo(element) {
    element.scrollIntoView({ behavior: "smooth", block: "start" });
}

// Copy Link to Clipboard
function copyAssignmentLink(assignmentId) {
    const url = `${window.location.origin}/assignment/${assignmentId}`;
    navigator.clipboard
        .writeText(url)
        .then(() => {
            showToast("🔗 Link copied to clipboard!");
        })
        .catch(() => {
            showToast("❌ Failed to copy link");
        });
}

function copySubmissionLink(submissionId) {
    const url = `${window.location.origin}/submission/${submissionId}`;
    navigator.clipboard
        .writeText(url)
        .then(() => {
            showToast("🔗 Link copied to clipboard!");
        })
        .catch(() => {
            showToast("❌ Failed to copy link");
        });
}

// Initialize all features
document.addEventListener("DOMContentLoaded", async function () {
    initDarkMode();
    await initReactions();
    initViewMode();
    initCharCounter();
    await updateBookmarkButtons();
    await trackActivity();
    estimateReadingTime();

    // Track view for assignment or submission detail page
    const assignmentIdMeta = document.querySelector('meta[name="assignment-id"]');
    if (assignmentIdMeta) {
        await trackPostView(assignmentIdMeta.content);
    }

    // Add event listeners for search
    const searchInput = document.getElementById("searchAssignments");
    if (searchInput) {
        searchInput.addEventListener("input", (e) => searchAssignments(e.target.value));
    }

    console.log("✨ Interactive features loaded with server-side support!");
});
