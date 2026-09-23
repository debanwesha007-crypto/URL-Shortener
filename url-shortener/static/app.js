const form = document.getElementById("shorten-form");
const urlInput = document.getElementById("url-input");
const customCodeInput = document.getElementById("custom-code-input");
const resultBox = document.getElementById("result");
const shortUrlText = document.getElementById("short-url-text");
const errorText = document.getElementById("error-text");
const copyBtn = document.getElementById("copy-btn");
const urlsBody = document.getElementById("urls-body");

async function loadUrls() {
  const res = await fetch("/api/urls");
  const urls = await res.json();
  urlsBody.innerHTML = "";
  urls.forEach((u) => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td><a href="/${u.short_code}" target="_blank">/${u.short_code}</a></td>
      <td class="original" title="${u.original_url}">${u.original_url}</td>
      <td>${u.clicks}</td>
      <td><button data-code="${u.short_code}" class="delete-btn">✕</button></td>
    `;
    urlsBody.appendChild(tr);
  });

  document.querySelectorAll(".delete-btn").forEach((btn) => {
    btn.addEventListener("click", async () => {
      await fetch(`/api/urls/${btn.dataset.code}`, { method: "DELETE" });
      loadUrls();
    });
  });
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  errorText.classList.add("hidden");
  resultBox.classList.add("hidden");

  const payload = {
    url: urlInput.value,
    custom_code: customCodeInput.value,
  };

  try {
    const res = await fetch("/api/shorten", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const data = await res.json();

    if (!res.ok) {
      errorText.textContent = data.error || "Something went wrong.";
      errorText.classList.remove("hidden");
      return;
    }

    shortUrlText.textContent = data.short_url;
    resultBox.classList.remove("hidden");
    urlInput.value = "";
    customCodeInput.value = "";
    loadUrls();
  } catch (err) {
    errorText.textContent = "Could not reach the server.";
    errorText.classList.remove("hidden");
  }
});

copyBtn.addEventListener("click", () => {
  navigator.clipboard.writeText(shortUrlText.textContent);
  copyBtn.textContent = "Copied!";
  setTimeout(() => (copyBtn.textContent = "Copy"), 1500);
});

loadUrls();
