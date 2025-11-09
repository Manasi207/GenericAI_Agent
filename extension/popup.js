
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// New code starts here popup.js
const sendBtn = document.getElementById("sendBtn");
const promptInput = document.getElementById("prompt");
const responseDiv = document.getElementById("response");
const imageInput = document.getElementById("imageInput");

const API_URL = "http://127.0.0.1:8000";

sendBtn.addEventListener("click", async () => {
  const prompt = promptInput.value.trim();
  if (!prompt) {
    responseDiv.innerText = "⚠️ Please enter a prompt.";
    return;
  }

  responseDiv.innerText = "⏳ Processing...";


  const file = imageInput.files[0];
  try {
    let res;
    if (file) {
      const formData = new FormData();
      formData.append("prompt", prompt);
      formData.append("file", file);
      res = await fetch(`${API_URL}/agent/image`, {
        method: "POST",
        body: formData,
      });
    } else {
      res = await fetch(`${API_URL}/agent`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt }),
      });
    }

    const data = await res.json();
    const responseText = data.response || "⚠️ No response.";
    responseDiv.innerText = responseText;

    // ✅ Automatically open a new tab for browse: commands
    if (responseText.includes("🌐 I will open")) {
      const match = responseText.match(/open\s+([^\s]+)\s+/i);
      if (match && match[1]) {
        let url = match[1];
        if (!url.startsWith("http")) {
          url = "https://" + url;
        }
        chrome.tabs.create({ url });
      }
    }
  } catch (err) {
    responseDiv.innerText = "❌ Error: " + err.message;
  }
});
