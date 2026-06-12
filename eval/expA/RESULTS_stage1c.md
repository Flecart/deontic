_(excluded 0 leak-flagged cases)_

## Verdict accuracy (share status) by arm x tier

| arm | tier 0 | tier 1 | tier 2 |
|---|---|---|---|
| ground_closed[deepseek-v4-flash] |  95.8% (23/24) |  83.3% (20/24) |  58.3% (14/24) |
| ground_closed[gpt-4.1] |  87.5% (21/24) |  83.3% (20/24) |  79.2% (19/24) |
| ground_open[deepseek-v4-flash] |  58.3% (14/24) |  58.3% (14/24) |  54.2% (13/24) |
| ground_open[gpt-4.1] |  75.0% (18/24) |  66.7% (16/24) |  62.5% (15/24) |
| holistic[deepseek-v4-flash] |  66.7% (16/24) |  70.8% (17/24) |  54.2% (13/24) |
| holistic[gpt-4.1] |  70.8% (17/24) |  66.7% (16/24) |  58.3% (14/24) |
| oracle | 100.0% (24/24) | 100.0% (24/24) | 100.0% (24/24) |
| program | 100.0% (24/24) |  33.3% (8/24) |  33.3% (8/24) |
| staged_closed[deepseek-v4-flash] |  87.5% (21/24) |  79.2% (19/24) |  50.0% (12/24) |
| staged_closed[gpt-4.1] |  91.7% (22/24) |  87.5% (21/24) |  58.3% (14/24) |
| staged_open[deepseek-v4-flash] |  62.5% (15/24) |  62.5% (15/24) |  45.8% (11/24) |
| staged_open[gpt-4.1] |  75.0% (18/24) |  66.7% (16/24) |  66.7% (16/24) |

## Atom-level grounding accuracy (regime x tier)

| regime[model] | tier 0 | tier 1 | tier 2 |
|---|---|---|---|
| ground_closed[deepseek-v4-flash] |  95.2% (160/168) |  73.8% (124/168) |  61.9% (104/168) |
| ground_closed[gpt-4.1] |  93.5% (157/168) |  78.6% (132/168) |  71.4% (120/168) |
| ground_open[deepseek-v4-flash] |  83.9% (141/168) |  83.9% (141/168) |  81.0% (136/168) |
| ground_open[gpt-4.1] |  88.7% (149/168) |  89.3% (150/168) |  86.3% (145/168) |
| staged_closed[deepseek-v4-flash] |  93.5% (157/168) |  72.0% (121/168) |  58.9% (99/168) |
| staged_closed[gpt-4.1] |  93.5% (157/168) |  77.4% (130/168) |  65.5% (110/168) |
| staged_open[deepseek-v4-flash] |  77.4% (130/168) |  83.9% (141/168) |  82.7% (139/168) |
| staged_open[gpt-4.1] |  84.5% (142/168) |  85.7% (144/168) |  88.1% (148/168) |

### True-atom recall per atom (regime, tier)

| arm | atom | tier 0 | tier 1 | tier 2 |
|---|---|---|---|---|
| ground_closed | anonymized |  75.0% (12/16) |  62.5% (10/16) |  18.8% (3/16) |
| ground_closed | certified | 100.0% (26/26) |   0.0% (0/26) |   0.0% (0/26) |
| ground_closed | commercial |  87.5% (21/24) |  12.5% (3/24) |  45.8% (11/24) |
| ground_closed | consent |  92.9% (26/28) |  64.3% (18/28) |  28.6% (8/28) |
| ground_closed | emergency | 100.0% (16/16) | 100.0% (16/16) |  68.8% (11/16) |
| ground_closed | personal_data |  94.7% (36/38) |  84.2% (32/38) |  28.9% (11/38) |
| ground_closed | revoked | 100.0% (18/18) |  72.2% (13/18) | 100.0% (18/18) |
| ground_open | anonymized |  12.5% (2/16) |  12.5% (2/16) |   0.0% (0/16) |
| ground_open | certified |  92.3% (24/26) |  57.7% (15/26) |  53.8% (14/26) |
| ground_open | commercial | 100.0% (24/24) | 100.0% (24/24) | 100.0% (24/24) |
| ground_open | consent |  57.1% (16/28) |  67.9% (19/28) |  78.6% (22/28) |
| ground_open | emergency |  68.8% (11/16) |  50.0% (8/16) |  43.8% (7/16) |
| ground_open | personal_data |  94.7% (36/38) | 100.0% (38/38) | 100.0% (38/38) |
| ground_open | revoked |  77.8% (14/18) | 100.0% (18/18) |  66.7% (12/18) |
| staged_closed | anonymized |  50.0% (8/16) |  43.8% (7/16) |   0.0% (0/16) |
| staged_closed | certified | 100.0% (26/26) |   0.0% (0/26) |   0.0% (0/26) |
| staged_closed | commercial | 100.0% (24/24) |  25.0% (6/24) |  58.3% (14/24) |
| staged_closed | consent |  92.9% (26/28) |  60.7% (17/28) |   0.0% (0/28) |
| staged_closed | emergency | 100.0% (16/16) | 100.0% (16/16) |  62.5% (10/16) |
| staged_closed | personal_data |  86.8% (33/38) |  86.8% (33/38) |  31.6% (12/38) |
| staged_closed | revoked |  88.9% (16/18) |  27.8% (5/18) |  61.1% (11/18) |
| staged_open | anonymized |   6.2% (1/16) |  18.8% (3/16) |   0.0% (0/16) |
| staged_open | certified |  53.8% (14/26) |  42.3% (11/26) |  57.7% (15/26) |
| staged_open | commercial | 100.0% (24/24) | 100.0% (24/24) | 100.0% (24/24) |
| staged_open | consent |  46.4% (13/28) |  67.9% (19/28) |  96.4% (27/28) |
| staged_open | emergency |  81.2% (13/16) |  37.5% (6/16) |  31.2% (5/16) |
| staged_open | personal_data |  94.7% (36/38) | 100.0% (38/38) |  97.4% (37/38) |
| staged_open | revoked |  66.7% (12/18) | 100.0% (18/18) |  83.3% (15/18) |

## Acted subset: violation + remedy detection

| arm | violation acc | notify acc | n |
|---|---|---|---|
| ground_closed[deepseek-v4-flash] |  83.3% (25/30) |  76.7% (23/30) | 30 |
| ground_closed[gpt-4.1] |  90.0% (27/30) |  86.7% (26/30) | 30 |
| ground_open[deepseek-v4-flash] |  70.0% (21/30) |  70.0% (21/30) | 30 |
| ground_open[gpt-4.1] |  86.7% (26/30) |  86.7% (26/30) | 30 |
| holistic[deepseek-v4-flash] |  73.3% (22/30) |  70.0% (21/30) | 30 |
| holistic[gpt-4.1] |  80.0% (24/30) |  80.0% (24/30) | 30 |
| oracle | 100.0% (30/30) | 100.0% (30/30) | 30 |
| program |  73.3% (22/30) |  73.3% (22/30) | 30 |
| staged_closed[deepseek-v4-flash] |  73.3% (22/30) |  63.3% (19/30) | 30 |
| staged_closed[gpt-4.1] |  83.3% (25/30) |  80.0% (24/30) | 30 |
| staged_open[deepseek-v4-flash] |  80.0% (24/30) |  76.7% (23/30) | 30 |
| staged_open[gpt-4.1] |  86.7% (26/30) |  86.7% (26/30) | 30 |

## Mean tokens per case (LLM arms)

| arm | mean tokens | n |
|---|---|---|
| ground_closed[deepseek-v4-flash] | 1822 | 72 |
| ground_closed[gpt-4.1] | 724 | 72 |
| ground_open[deepseek-v4-flash] | 1660 | 72 |
| ground_open[gpt-4.1] | 652 | 72 |
| holistic[deepseek-v4-flash] | 2045 | 72 |
| holistic[gpt-4.1] | 872 | 72 |
| staged_closed[deepseek-v4-flash] | 4387 | 72 |
| staged_closed[gpt-4.1] | 2977 | 72 |
| staged_open[deepseek-v4-flash] | 4275 | 72 |
| staged_open[gpt-4.1] | 2925 | 72 |
