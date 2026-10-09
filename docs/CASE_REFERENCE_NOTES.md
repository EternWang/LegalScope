# Reference notes

The case references contain legal authorities, propositions and constraints from
the original evaluation dataset. They support the scoring protocol and are not
unique model answers. They have not been independently validated as a complete
legal reference database.

## Nursing fee references: RV025 and RV026

| Record | Issue | Reading guidance |
| --- | --- | --- |
| RV025 | The reference uses Article 32 without an edition, while the supplied judgment cites the 2020 revision. | The continuation rule is Article 19 in the 2020 revision. |
| RV026 | Article 23 does not state the nursing fee calculation rule. Article 32 also uses older numbering. | The 2020 revision places the calculation and continuation rules in Articles 8 and 19. |

The [older judicial interpretation](https://dxjjjc.bjdx.gov.cn/jjjcw/xxgk/qtgk/djfg01/1464943/index.html)
sets out nursing fee calculation in Article 21 and continued payments in Article 32;
Article 23 concerns inpatient meal allowances. The
[2020 revision, effective January 1, 2021](https://www.court.gov.cn/zixun/xiangqing/282621.html),
places nursing calculation and continuation in Articles 8 and 19; Article 23
concerns compensation for mental distress. The supplied judgment explicitly
identifies the 2020 revision in its statement of the first instance legal basis.
It also reproduces an appellant's argument using older numbering. These passages
must be distinguished when interpreting the reference. The
[2022 text](https://www.court.gov.cn/fabu/xiangqing/357071.html) retains Articles 8
and 19, but is not the edition named in that passage of the source judgment.

## Procedural defects: RV271 and RV272

The proposition in these records concerns a minor procedural violation without
an actual adverse effect on the applicant's rights. Two citations identify a
different provision:

| Historical citation | Provision corresponding to the stated rule |
| --- | --- |
| Administrative Litigation Law, Article 74(1)(1) | Article 74(1)(2) |
| Administrative Reconsideration Law, Article 65(2)(2) | Article 65(1)(2), in the 2023 revision effective January 1, 2024 |

Article 74(1)(1) concerns serious harm to national or public interests if an act
is revoked. Article 65(2)(2) concerns an authority changing the challenged act
while the applicant continues to request review. See the official texts of the
[Administrative Litigation Law](https://www.samr.gov.cn/zw/zfxxgk/fdzdgknr/bgt/art/2025/art_ba3b20d736d14aeeb1ace665f0f51a21.html)
and [Administrative Reconsideration Law](https://xz.spb.gov.cn/xzyzglj/c100065/c100066/202312/7f4c4135a419497ea449cdc9e46fa385.shtml).
These mismatches are also present in the supplied source text; they were not
introduced by the public export. The observation concerns the correspondence
between a citation and the stated rule, not a new assessment of the case outcome.

## References requiring clarification

RV189 and RV190 cite Article 20 of the 2003 personal injury interpretation,
which addresses lost income; the stated proposition discusses medical expenses,
for which Article 19 is directly relevant. Article 20 may also be relevant by
cross-reference when a caregiver has income. Whether to supplement or replace
the citation requires a substantive review, so no replacement is applied.

RV201 and RV202 use the generic English label “Rules for Reviewing and Determining
Forensic Psychiatric Appraisal Opinions” without identifying an issuing authority,
edition or provision. The exact intended authority has not been established.
RV205 and RV206 state a procedural principle without a specific provision.
These references should not be treated as precise bibliographic citations.

Unflagged records are not a certification of legal correctness. Citation
existence, the law applicable at the relevant time, and support for the particular
proposition are separate checks. Older laws may be appropriate for older events.

## Version handling

The released reference fields retain their original wording, with known issues
recorded in `reference_status` and `reference_note`. Prompt text and published
scores are unchanged. The effect on scoring has not been measured. Evaluations
using corrected references should identify their reference version and report
new scores separately from the paper's results.

An [offline comparison utility](REFERENCE_REVIEW.md) prepares responses and
validates result coverage for a new evaluation. It does not supply a corrected
gold answer set or implement the historical evaluator.
