const form = document.querySelector(".announcement-form");
form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const formData = new FormData(form);
  await fetch("/api/announcements", {
    method: "POST",
    body: formData,
    credentials: "include",
  });
  form.reset();
  loadMessages();
});
