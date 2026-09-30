const assert = require("assert");
const { validateMerchant } = require("../app/validation.js");

const valid = {
  registeredName: "Synthetic Harbour Trading Limited",
  businessRegistrationNumber: "12345678",
  businessType: "Retail",
  country: "Hong Kong",
  contactName: "Test User",
  email: "tester@example.com",
  expectedMonthlyVolume: "50000",
  hasBusinessRegistration: true,
  hasOwnershipDeclaration: true,
  hasAuthorisationEvidence: true,
};

assert.equal(validateMerchant(valid).status, "READY_FOR_COMPLETENESS_REVIEW");
assert.equal(validateMerchant({ ...valid, email: "bad-email" }).status, "INCOMPLETE");
assert.deepEqual(validateMerchant({ ...valid, registeredName: "" }).missing, ["Registered name"]);
assert.ok(validateMerchant({ ...valid, businessRegistrationNumber: "ABC" }).errors.length === 1);
assert.ok(validateMerchant({ ...valid, expectedMonthlyVolume: "0" }).errors.length === 1);
assert.equal(validateMerchant({ ...valid, hasOwnershipDeclaration: false }).status, "DOCUMENTS_OUTSTANDING");
assert.deepEqual(validateMerchant({}).missing.length, 7);

console.log("7 validation rule tests passed");
