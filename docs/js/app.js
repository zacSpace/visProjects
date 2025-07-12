// docs/js/app.js
document.addEventListener("DOMContentLoaded", () => {
  // 0) Grab the existing config (injected at build time)
  const {
    posSd: initPosSd,
    negSd: initNegSd,
    holdDays: initHoldDays,
    positionSize: initSize,
    token: githubToken
  } = window.BACKTEST_CFG;

  // 1) Prefill the form fields
  document.getElementById("posSd").value        = initPosSd;
  document.getElementById("negSd").value        = initNegSd;
  document.getElementById("holdDays").value     = initHoldDays;
  document.getElementById("positionSize").value = initSize;

  const form = document.getElementById("backtest-form");
  form.addEventListener("submit", async e => {
    e.preventDefault();

    // 2) Collect the *new* parameters from the form
    const params = {
      posSd:        parseFloat(document.getElementById("posSd").value),
      negSd:        parseFloat(document.getElementById("negSd").value),
      holdDays:     parseInt(  document.getElementById("holdDays").value, 10),
      positionSize: parseFloat(document.getElementById("positionSize").value),
      token:        githubToken    // carry forward your PAT
    };

    // 3) GitHub repo info
    const owner = "zacSpace";
    const repo  = "visProjects";
    const path  = "config.json";

    // 4) Helper to call the GitHub API with your token
    const gh = (url, opts={}) =>
      fetch(url, {
        ...opts,
        headers: {
          "Authorization": `token ${githubToken}`,
          "Accept":        "application/vnd.github.v3+json",
          ...(opts.headers || {})
        }
      });

    // 5) Get existing file SHA (so we can update)
    let sha;
    const getRes = await gh(
      `https://api.github.com/repos/${owner}/${repo}/contents/${path}`
    );
    if (getRes.ok) {
      const data = await getRes.json();
      sha = data.sha;
    }

    // 6) PUT the new config.json
    const putRes = await gh(
      `https://api.github.com/repos/${owner}/${repo}/contents/${path}`,
      {
        method: "PUT",
        body: JSON.stringify({
          message: "Update backtest config",
          content: btoa(JSON.stringify(params, null, 2)),
          sha
        })
      }
    );

    if (!putRes.ok) {
      const err = await putRes.text();
      console.error("GitHub write failed:", err);
      alert("Failed to save config. See console for details.");
      return;
    }

    alert("Parameters saved—please wait a minute and reload to see the results.");
  });
});
