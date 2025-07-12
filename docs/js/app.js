// docs/js/app.js
document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("backtest-form");

  form.addEventListener("submit", e => {
    e.preventDefault();
    const params = {
      posSd:        parseFloat(document.getElementById("posSd").value),
      negSd:        parseFloat(document.getElementById("negSd").value),
      holdDays:     parseInt(document.getElementById("holdDays").value, 10),
      positionSize: parseFloat(document.getElementById("positionSize").value)
    };
    // Save for later or send to your backend/CI:
    localStorage.setItem("backtestParams", JSON.stringify(params));

    // If you plan to reload the page and have your build pipeline pick up a config file:
    // location.search = new URLSearchParams(params).toString();

    // For now just confirm:
    alert("Parameters saved: " + JSON.stringify(params));
  });
}); 
