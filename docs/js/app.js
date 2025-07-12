// docs/js/app.js
document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("backtest-form");

  form.addEventListener("submit", async e => {
    e.preventDefault();

    // 1) Read the inputs
    const params = {
      posSd:        parseFloat(document.getElementById("posSd").value),
      negSd:        parseFloat(document.getElementById("negSd").value),
      holdDays:     parseInt  (document.getElementById("holdDays").value, 10),
      positionSize: parseFloat(document.getElementById("positionSize").value)
    };

    // 2) Optionally save locally
    localStorage.setItem("backtestParams", JSON.stringify(params));

    // 3) Push config.json update to GitHub
    //    You need to fill in USERNAME, REPO, and a PAT with repo:contents scope.
    const owner = "YOUR_USERNAME";
    const repo  = "YOUR_REPO";
    const path  = "config.json";
    const token = "YOUR_PERSONAL_ACCESS_TOKEN";

    // (a) First fetch the existing file to get its SHA
    const getRes = await fetch(
      `https://api.github.com/repos/${owner}/${repo}/contents/${path}`
    , {
      headers: {
        Authorization: `token ${token}`
      }
    });
    const { sha } = await getRes.json();

    // (b) Then PUT the updated config.json
    const putRes = await fetch(
      `https://api.github.com/repos/${owner}/${repo}/contents/${path}`
    , {
      method: "PUT",
      headers: {
        Authorization: `token ${token}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        message: "Update backtest config",
        content: btoa(JSON.stringify(params, null, 2)),
        sha
      })
    });

    if (!putRes.ok) {
      const err = await putRes.text();
      console.error("GitHub update failed:", err);
      return alert("Failed to save config. See console for details.");
    }

    alert("Parameters saved—please wait a minute and reload to see the results.");
  });
});
