# Reference notes

The case references contain legal authorities, propositions and constraints from
the original evaluation dataset. They support the scoring protocol and are not
unique model answers. They have not been independently validated as a complete
legal reference database.

## Nursing fee references: RV025 and RV026

| Record | Issue | Reading guidance |
| --- | --- | --- |
| RV025 | The cited Article 32 uses older numbering without specifying the edition. | Check the applicable edition; the corresponding rule is Article 19 in the 2022 text. |
| RV026 | Article 23 does not state the nursing fee calculation rule. The cited Article 32 also uses older numbering. | The calculation rule is Article 21 in the older text and Article 8 in the 2022 text. |

The [older judicial interpretation](https://dxjjjc.bjdx.gov.cn/jjjcw/xxgk/qtgk/djfg01/1464943/index.html)
sets out nursing fee calculation in Article 21 and continued payments in Article 32;
Article 23 concerns inpatient meal allowances. The
[2022 interpretation](https://zjyuyao.zjjcy.gov.cn/art/2022/7/28/art_1229661300_339.html)
places the nursing and continuation rules in Articles 8 and 19. Its Article 23
concerns compensation for mental distress. The applicable edition depends on the
case and the interpretation's temporal rules.

The released reference fields retain their original wording, with the issue
recorded in `reference_status` and `reference_note`. Prompt text and published
scores are unchanged. The effect on scoring has not been measured. Evaluations
using corrected references should identify their reference version and report
new scores separately from the paper's results.
