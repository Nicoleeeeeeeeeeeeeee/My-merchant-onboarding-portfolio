"use strict";

const form = document.querySelector("#merchant-form");
const resultPanel = document.querySelector("#result");
const statusHeading = document.querySelector("#status");
const detail = document.querySelector("#result-detail");

function values() {
  return {
    registeredName: document.querySelector("#registeredName").value,
    businessRegistrationNumber: document.querySelector("#businessRegistrationNumber").value,
    businessType: document.querySelector("#businessType").value,
    country: document.querySelector("#country").value,
    contactName: document.querySelector("#contactName").value,
    email: document.querySelector("#email").value,
    expectedMonthlyVolume: document.querySelector("#expectedMonthlyVolume").value,
    hasBusinessRegistration: document.querySelector("#hasBusinessRegistration").checked,
    hasOwnershipDeclaration: document.querySelector("#hasOwnershipDeclaration").checked,
    hasAuthorisationEvidence: document.querySelector("#hasAuthorisationEvidence").checked,
  };
}

function list(title, items) {
  if (!items.length) return "";
  return `<h3>${title}</h3><ul>${items.map((item) => `<li>${item}</li>`).join("")}</ul>`;
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  const output = MerchantValidation.validateMerchant(values());
  resultPanel.dataset.status = output.status;
  statusHeading.textContent = output.status.replaceAll("_", " ");
  detail.innerHTML =
    list("Missing required fields", output.missing) +
    list("Validation errors", output.errors) +
    list("Documents outstanding", output.missingDocuments) +
    (!output.missing.length && !output.errors.length && !output.missingDocuments.length
      ? "<p>Required information and checklist items are complete. Route to an authorised reviewer; this tool does not approve the merchant.</p>"
      : "");
});

form.addEventListener("reset", () => {
  window.setTimeout(() => {
    resultPanel.dataset.status = "idle";
    statusHeading.textContent = "Awaiting validation";
    detail.innerHTML = "<p>Enter merchant details and run validation.</p>";
  }, 0);
});
