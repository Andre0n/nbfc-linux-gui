const copyButton = document.querySelector("[data-copy]");

if (copyButton) {
  copyButton.addEventListener("click", async () => {
    try {
      await navigator.clipboard.writeText(copyButton.dataset.copy);
      copyButton.classList.add("copied");
      window.setTimeout(() => copyButton.classList.remove("copied"), 1200);
    } catch (_error) {
      copyButton.classList.remove("copied");
    }
  });
}
