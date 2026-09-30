(function (root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  else root.MerchantValidation = api;
})(typeof globalThis !== "undefined" ? globalThis : this, function () {
  "use strict";

  const REQUIRED = [
    ["registeredName", "Registered name"],
    ["businessRegistrationNumber", "Business registration number"],
    ["businessType", "Business type"],
    ["country", "Country of registration"],
    ["contactName", "Contact name"],
    ["email", "Email"],
    ["expectedMonthlyVolume", "Expected monthly volume"],
  ];

  function validateMerchant(input) {
    const missing = REQUIRED.filter(([key]) => !String(input[key] || "").trim()).map(([, label]) => label);
    const errors = [];
    const email = String(input.email || "").trim();
    const brn = String(input.businessRegistrationNumber || "").trim();
    const volume = Number(input.expectedMonthlyVolume);

    if (email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) errors.push("Email format is invalid");
    if (brn && !/^\d{8}$/.test(brn)) errors.push("Business registration number must contain 8 digits");
    if (input.expectedMonthlyVolume && (!Number.isFinite(volume) || volume <= 0)) errors.push("Expected monthly volume must be greater than 0");

    const documents = [input.hasBusinessRegistration, input.hasOwnershipDeclaration, input.hasAuthorisationEvidence];
    const missingDocuments = ["Business registration copy", "Ownership declaration", "Authorisation evidence"]
      .filter((_, index) => !documents[index]);

    let status = "READY_FOR_COMPLETENESS_REVIEW";
    if (missing.length || errors.length) status = "INCOMPLETE";
    else if (missingDocuments.length) status = "DOCUMENTS_OUTSTANDING";

    return { status, missing, errors, missingDocuments };
  }

  return { validateMerchant, REQUIRED };
});
