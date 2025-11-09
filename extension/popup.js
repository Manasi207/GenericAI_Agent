
/////////////////////////////////////////////////////////////////////////

// document.addEventListener("DOMContentLoaded", function () {
//   const form = document.getElementById("agent-form");
//   const queryInput = document.getElementById("query");
//   const responseDiv = document.getElementById("response");

//   form.addEventListener("submit", async function (e) {
//     e.preventDefault();
//     const userQuery = queryInput.value.trim();
//     if (!userQuery) return;

//     responseDiv.style.display = "block";
//     responseDiv.innerHTML = "<div class='loading'>⏳ Thinking...</div>";

//     try {
//       const res = await fetch("http://127.0.0.1:8000/agent", {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify({ prompt: userQuery }),
//       });

//       const data = await res.json();

//       // Handle direct navigation
//       if (data.redirect_url) {
//         const url = data.redirect_url;
//         window.open(url, "_blank"); // open site directly in a new tab
//         responseDiv.innerHTML = `🌐 Navigating to: <b>${url}</b>`;
//         return;
//       }

//       // Otherwise handle normal text responses
//       let text = data.response || data.detail || "⚠️ No response from agent";

//       // Convert any URLs in text into clickable anchors
//       const urlRegex = /(https?:\/\/[^\s]+)/g;
//       let html = text.replace(urlRegex, function (url) {
//         return `<a href="#" class="agent-link" data-url="${url}">${url}</a>`;
//       });

//       // Replace newlines with <br> for readability
//       responseDiv.innerHTML = html.replace(/\n/g, "<br>");

//       // Attach click handler to open links in new tab
//       responseDiv.querySelectorAll(".agent-link").forEach((a) => {
//         a.addEventListener("click", (ev) => {
//           ev.preventDefault();
//           const url = a.getAttribute("data-url");
//           window.open(url, "_blank");
//         });
//       });

//     } catch (err) {
//       responseDiv.innerHTML = "<div class='error'>❌ Failed to connect to backend</div>";
//       console.error("Agent error:", err);
//     }
//   });
// });
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

<<<<<<< HEAD
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
=======
    try {
      const res = await fetch("http://13.61.4.25:8000/agent", {
>>>>>>> 1a190c15c09dd3ab004bd05e82790fcc66e82eb0
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
