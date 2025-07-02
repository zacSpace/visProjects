document.addEventListener("DOMContentLoaded", () => {
    const checkbox = document.getElementById("yesNoSwitch");
    const label    = document.getElementById("switchLabel");
    label.textContent = checkbox.checked ? "Yes" : "No";
    checkbox.addEventListener("change", () => {
      label.textContent = checkbox.checked ? "Yes" : "No";
    });
  });
  