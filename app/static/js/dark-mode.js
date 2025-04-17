document.addEventListener("DOMContentLoaded", function () {
  // Check for saved theme preference or use preferred color scheme
  const savedTheme = localStorage.getItem("theme");
  const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;

  if (savedTheme === "dark" || (!savedTheme && prefersDark)) {
    document.body.classList.add("dark");
  }

  // Theme toggle button functionality
  const themeToggle = document.getElementById("theme-toggle");

  themeToggle.addEventListener("click", function () {
    document.body.classList.toggle("dark");

    // Save preference to localStorage
    if (document.body.classList.contains("dark")) {
      localStorage.setItem("theme", "dark");
    } else {
      localStorage.setItem("theme", "light");
    }
  });
});
