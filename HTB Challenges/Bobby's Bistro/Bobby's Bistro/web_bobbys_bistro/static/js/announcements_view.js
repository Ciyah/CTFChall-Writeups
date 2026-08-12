document.addEventListener("click", function (e) {
  const link = e.target.closest("a[data-announcement]");
  if (!link) return;

  e.preventDefault();

  const content = link.getAttribute("data-announcement");
  const encoded = encodeURIComponent(content);

  window.location.href = `/announcements/view?q=${encoded}`;
});
