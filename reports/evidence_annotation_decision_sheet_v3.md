# Evidence Annotation Decision Sheet v3 — Q001, Q005, Q009, Q012

**Decision basis:** Human-approved decisions for Milestone 2B.24R  
**Annotation status:** Proposal; all records remain pending user adjudication

This sheet records how the five approved decisions were applied to the
version-3 proposal. Approval of these revision criteria does not approve any
annotation as ground truth.

## Q001 — complaint-forwarding commitment

**Decision:** Treat direct text in each rank-1 chunk as answer evidence, not
mere page overlap.

The existing F1 remains: tell the customer how to take the complaint forward
if still dissatisfied. Both chunks contain the source-page-3 commitment:

- Fixed-size rank 1: `doc_001_fixed_size_00001_aee405d33739` — DIRECT, F1.
- Structure-aware rank 1: `doc_001_structure_aware_00001_ac782e3816d0` —
  DIRECT, F1.

**Old labels:** fixed-size incomplete; structure-aware incomplete.  
**V3 labels:** fixed-size complete; structure-aware complete.

## Q005 — penal-charge presentation

**Decision:** Late repayment and another borrower default are context supplied
by the question, not required answer facets. Retain the answer requirements:

- F3: The penal charge must be stated in bold.
- F4: The penal charge must be stated in the loan agreement.

Both use source doc_001, PDF page 4. F3 and F4 retain their v2 IDs; F1 and F2
were removed.

Top-10 evidence:

- Fixed-size rank 5: `doc_001_fixed_size_00004_785fedf70295`.
- Structure-aware rank 6: `doc_001_structure_aware_00004_288632361e39`.

Each cited doc_001 chunk fully supports F4 through its statement that penal
charge quantum and reasons are disclosed in the loan agreement. Neither
contains the bold requirement, so F3 is not covered; both strategy results
remain incomplete.

`covered_facets` lists only F4 because it is fully supported. The existing
`label: PARTIAL`, `supported_facet_ids`, and `justification` retain the
partial-evidence distinction; no schema extension was needed. Diagnostic
fixed-size rank 19 and structure-aware rank 17 contain both requirements but
are outside top 10 and do not affect top-10 completeness.

**Old labels:** both strategies incomplete, with a combined bold/location
facet represented as covered despite partial evidence.  
**V3 labels:** both strategies incomplete; only F4 is fully covered at
fixed-size r5 and structure-aware r6.

## Q009 — disadvantage trigger and customer option

**Decision:** The disadvantage trigger supplied by the question is context,
not a required answer facet. Retain:

- F2: Within 60 days and without notice, the customer may close the account
  or switch it.
- F3: Closing or switching must not require extra charges or interest.

Both facets use source doc_003, PDF page 5.

- Fixed-size rank 2: `doc_003_fixed_size_00006_8bf99111838c` — DIRECT, F2/F3.
- Structure-aware rank 4: `doc_003_structure_aware_00006_f9c845e0a416` —
  DIRECT, F2/F3.

**Old labels:** both strategies complete across three facets, including the
question's trigger.  
**V3 labels:** both strategies remain complete across the two answer facets.

## Q012 — separately assessable repossession safeguards

**Decision:** Split the two paired requirements while retaining stable IDs
where practical. All facets cite doc_016, PDF page 6:

| Facet | V3 requirement |
|---|---|
| F1 | Legally enforceable repossession clause in the contract/loan agreement. |
| F2 | Notice period before taking possession. |
| F6 | Circumstances in which the notice period may be waived. |
| F3 | Procedure for taking possession of the security. |
| F4 | Final chance to repay before sale/auction. |
| F5 | Procedure for returning possession to the borrower. |
| F7 | Procedure for sale or auction of the property. |

F6 and F7 are new, unique facet IDs. F2 and F5 retain their IDs for the
narrowed notice and return-of-possession facets.

- Fixed-size rank 4: `doc_016_fixed_size_00006_5707a2baee10` — DIRECT,
  F1–F7.
- Structure-aware rank 2: `doc_016_structure_aware_00007_3562949c7e7a` —
  DIRECT, F1–F7.

Both payloads contain the separately listed notice, waiver, possession,
repayment opportunity, return-possession, and sale/auction provisions.

**Old labels:** both strategies complete across five combined facets.  
**V3 labels:** both strategies remain complete across seven independently
assessed facets.

## Review boundary

The decisions above authorize a proposal revision. They do not adjudicate
the chunk labels as ground truth or remove
`pending_user_adjudication` from any record. Q020, Q021, and Q025 retain the
already approved evaluation criteria and their v2 evidence assessments.
