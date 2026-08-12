const chatBox = document.getElementById("chatMessages");
const form = document.getElementById("chatForm");

const senderColors = {};
const senderAlertClasses = {};

const textColors = [
  "#8be9fd", // cyan
  "#50fa7b", // green
  "#ff79c6", // pink
  "#f1fa8c", // yellow
  "#bd93f9", // purple
  "#ff5555", // red
  "#f8f8f2", // white
];

const alertVariants = [
  "terminal-alert",
  "terminal-alert-primary",
  "terminal-alert-error",
];

String.prototype.hashCode = function () {
  let hash = 0;
  for (let i = 0; i < this.length; i++) {
    hash = this.charCodeAt(i) + ((hash << 5) - hash);
  }
  return hash;
};

function getColorForSender(sender) {
  if (!senderColors[sender]) {
    const color = textColors[Math.abs(sender.hashCode()) % textColors.length];
    senderColors[sender] = color;
  }
  return senderColors[sender];
}

function getAlertClassForSender(sender) {
  if (!senderAlertClasses[sender]) {
    const alert =
      alertVariants[Math.abs(sender.hashCode()) % alertVariants.length];
    senderAlertClasses[sender] = alert;
  }
  return senderAlertClasses[sender];
}

async function loadMessages() {
  const res = await fetch("/api/chat-messages", { credentials: "include" });
  if (!res.ok) return;
  const data = await res.json();
  if (!data.success) return;

  chatBox.innerHTML = "";

  data.messages.forEach((msg) => {
    const timestamp = msg[0];
    const content = msg[1];
    const sender = msg[2];
    const attachment = msg[3];

    const line = document.createElement("div");
    line.className = getAlertClassForSender(sender);
    line.style.display = "flex";
    line.style.justifyContent = "space-between";
    line.style.alignItems = "center";
    line.style.marginBottom = "0.5rem";
    line.style.padding = "0.5rem 1rem";

    const left = document.createElement("div");
    left.className = "message-left";
    left.style.flex = "1";
    left.style.whiteSpace = "pre-wrap";
    left.style.wordBreak = "break-word";

    const senderSpan = document.createElement("span");
    senderSpan.className = "sender";
    senderSpan.textContent = `[${sender}] `;
    senderSpan.style.color = getColorForSender(sender);
    senderSpan.style.fontWeight = "bold";

    const contentSpan = document.createElement("span");
    contentSpan.textContent = content || "";

    left.appendChild(senderSpan);
    left.appendChild(contentSpan);

    if (attachment && !attachment.endsWith("/uploads/")) {
      const link = document.createElement("a");
      link.href = attachment;
      link.textContent = " (attachment)";
      link.target = "_blank";
      link.className = "terminal-link";
      left.appendChild(link);
    }

    const timeSpan = document.createElement("span");
    timeSpan.className = "timestamp";
    timeSpan.textContent = timestamp;
    timeSpan.style.color = "var(--secondary-color)";
    timeSpan.style.opacity = "0.6";
    timeSpan.style.fontSize = "0.85em";
    timeSpan.style.whiteSpace = "nowrap";
    timeSpan.style.marginLeft = "1rem";

    line.appendChild(left);
    line.appendChild(timeSpan);

    chatBox.appendChild(line);
  });

  chatBox.scrollTop = chatBox.scrollHeight;
}

// Refresh messages every 2 seconds
setInterval(loadMessages, 2000);
loadMessages();

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const formData = new FormData(form);
  await fetch("/api/chat-messages", {
    method: "POST",
    body: formData,
    credentials: "include",
  });
  form.reset();
  loadMessages();
});
