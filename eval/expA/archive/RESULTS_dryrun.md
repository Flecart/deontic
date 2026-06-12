## Verdict accuracy (share status) by arm x tier

| arm | tier 0 | tier 1 | tier 2 |
|---|---|---|---|
| ground_closed[deepseek-v4-flash] |  83.3% (20/24) |  62.5% (15/24) |  50.0% (12/24) |
| ground_closed[gpt-4.1] |  83.3% (20/24) |  70.8% (17/24) |  54.2% (13/24) |
| ground_open[deepseek-v4-flash] |  45.8% (11/24) |  54.2% (13/24) |  45.8% (11/24) |
| ground_open[gpt-4.1] |  54.2% (13/24) |  58.3% (14/24) |  58.3% (14/24) |
| holistic[deepseek-v4-flash] |  45.8% (11/24) |  62.5% (15/24) |  54.2% (13/24) |
| holistic[gpt-4.1] |  50.0% (12/24) |  54.2% (13/24) |  54.2% (13/24) |
| oracle | 100.0% (24/24) | 100.0% (24/24) | 100.0% (24/24) |
| program | 100.0% (24/24) |  33.3% (8/24) |  33.3% (8/24) |

## Atom-level grounding accuracy (regime x tier)

| regime[model] | tier 0 | tier 1 | tier 2 |
|---|---|---|---|
| ground_closed[deepseek-v4-flash] |  90.5% (152/168) |  71.4% (120/168) |  56.5% (95/168) |
| ground_closed[gpt-4.1] |  92.3% (155/168) |  75.6% (127/168) |  64.9% (109/168) |
| ground_open[deepseek-v4-flash] |  78.6% (132/168) |  76.2% (128/168) |  75.6% (127/168) |
| ground_open[gpt-4.1] |  84.5% (142/168) |  86.3% (145/168) |  81.5% (137/168) |

### True-atom recall per atom (regime, tier)

| arm | atom | tier 0 | tier 1 | tier 2 |
|---|---|---|---|---|
| ground_closed | anonymized |  72.7% (16/22) |  90.9% (20/22) |  27.3% (6/22) |
| ground_closed | certified | 100.0% (28/28) |   0.0% (0/28) |   0.0% (0/28) |
| ground_closed | commercial |  92.9% (26/28) |  28.6% (8/28) |  39.3% (11/28) |
| ground_closed | consent |  90.0% (27/30) |  70.0% (21/30) |  16.7% (5/30) |
| ground_closed | emergency |  68.8% (11/16) |  43.8% (7/16) |  12.5% (2/16) |
| ground_closed | personal_data |  85.7% (24/28) |  78.6% (22/28) |  17.9% (5/28) |
| ground_closed | revoked |  95.0% (19/20) |  75.0% (15/20) |  90.0% (18/20) |
| ground_open | anonymized |  18.2% (4/22) |  63.6% (14/22) |  18.2% (4/22) |
| ground_open | certified |  85.7% (24/28) |  75.0% (21/28) |  50.0% (14/28) |
| ground_open | commercial | 100.0% (28/28) | 100.0% (28/28) | 100.0% (28/28) |
| ground_open | consent |  70.0% (21/30) |  53.3% (16/30) |  73.3% (22/30) |
| ground_open | emergency |  18.8% (3/16) |  12.5% (2/16) |   0.0% (0/16) |
| ground_open | personal_data |  89.3% (25/28) |  89.3% (25/28) |  96.4% (27/28) |
| ground_open | revoked |  85.0% (17/20) |  85.0% (17/20) |  95.0% (19/20) |

## Acted subset: violation + remedy detection

| arm | violation acc | notify acc | n |
|---|---|---|---|
| ground_closed[deepseek-v4-flash] |  73.3% (22/30) |  76.7% (23/30) | 30 |
| ground_closed[gpt-4.1] |  83.3% (25/30) |  86.7% (26/30) | 30 |
| ground_open[deepseek-v4-flash] |  56.7% (17/30) |  56.7% (17/30) | 30 |
| ground_open[gpt-4.1] |  66.7% (20/30) |  73.3% (22/30) | 30 |
| holistic[deepseek-v4-flash] |  66.7% (20/30) |  63.3% (19/30) | 30 |
| holistic[gpt-4.1] |  60.0% (18/30) |  56.7% (17/30) | 30 |
| oracle | 100.0% (30/30) | 100.0% (30/30) | 30 |
| program |  73.3% (22/30) |  80.0% (24/30) | 30 |

## Mean tokens per case (LLM arms)

| arm | mean tokens | n |
|---|---|---|
| ground_closed[deepseek-v4-flash] | 2002 | 72 |
| ground_closed[gpt-4.1] | 728 | 72 |
| ground_open[deepseek-v4-flash] | 1511 | 72 |
| ground_open[gpt-4.1] | 655 | 72 |
| holistic[deepseek-v4-flash] | 1926 | 72 |
| holistic[gpt-4.1] | 875 | 72 |
---
_Dry run on pre-coherence-fix cases (23/72 worlds flagged incoherent post-hoc; clean-case analysis in REPORT.md). Zero parse errors in 576 rows; oracle 100% throughout._
