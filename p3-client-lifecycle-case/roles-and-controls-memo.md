# P3 memo: operating boundary for a hypothetical corporate onboarding case

## Context

This is a public-material-based learning case for a fictional corporate customer. It does not use real people, companies, identity documents, accounts, transactions, or customer data.

## Business / operations team

The business or onboarding team can own intake, explain the purpose and intended nature of the relationship using the approved questionnaire, collect documents, check whether required fields are present, log gaps, manage SLA reminders, and route exceptions. They may describe evidence and process status; they must not make a regulated risk decision from this case.

## Compliance / authorised reviewer

An authorised compliance function must decide whether CDD requirements are satisfied, whether enhanced or simplified measures are appropriate, whether a relationship can be approved or must be rejected, and how ongoing monitoring or periodic review frequency should be set. Any suspicion assessment or suspicious transaction report is outside this project and belongs to the regulated firm and its authorised processes.

## Control design reflected in the tracker

The tracker separates `Documents outstanding`, `Completeness review`, `Compliance review`, `Activation pending`, and `Periodic review due`. Activation is gated on a recorded authorised decision. An SLA breach or non-standard ownership structure creates an escalation reason rather than an informal override.

## Source interpretation

The HKMA AML/CFT Guideline describes a risk-based approach, CDD measures such as identifying the customer, beneficial owner and acting person, understanding the purpose and intended nature of the relationship, completing CDD before establishing a relationship, and keeping records up to date through periodic review. HKMA's corporate CDD FAQ emphasises proportionate, non-one-size-fits-all treatment and reliable independent sources. JFIU states that a person who knows or suspects relevant criminal or terrorist property should report to an authorised officer as soon as practicable. Those principles inform the hand-offs here; this case does not apply them to a real customer.
