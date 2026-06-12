_(excluded 0 leak-flagged cases)_

## Verdict accuracy (share status) by arm x tier

| arm | tier 0 | tier 1 | tier 2 |
|---|---|---|---|
| ground_closed[deepseek-v4-flash] |  83.3% (20/24) |  66.7% (16/24) |  50.0% (12/24) |
| ground_closed[gpt-4.1] |  87.5% (21/24) |  66.7% (16/24) |  54.2% (13/24) |
| ground_open[deepseek-v4-flash] |  41.7% (10/24) |  58.3% (14/24) |  45.8% (11/24) |
| ground_open[gpt-4.1] |  62.5% (15/24) |  62.5% (15/24) |  54.2% (13/24) |
| holistic[deepseek-v4-flash] |  62.5% (15/24) |  50.0% (12/24) |  50.0% (12/24) |
| holistic[gpt-4.1] |  62.5% (15/24) |  54.2% (13/24) |  50.0% (12/24) |
| oracle | 100.0% (24/24) | 100.0% (24/24) | 100.0% (24/24) |
| program | 100.0% (24/24) |  33.3% (8/24) |  33.3% (8/24) |
| staged_closed[deepseek-v4-flash] |  83.3% (20/24) |  75.0% (18/24) |  50.0% (12/24) |
| staged_closed[gpt-4.1] |  87.5% (21/24) |  79.2% (19/24) |  50.0% (12/24) |
| staged_open[deepseek-v4-flash] |  54.2% (13/24) |  54.2% (13/24) |  50.0% (12/24) |
| staged_open[gpt-4.1] |  58.3% (14/24) |  54.2% (13/24) |  54.2% (13/24) |

## Atom-level grounding accuracy (regime x tier)

| regime[model] | tier 0 | tier 1 | tier 2 |
|---|---|---|---|
| ground_closed[deepseek-v4-flash] |  92.3% (155/168) |  76.8% (129/168) |  64.3% (108/168) |
| ground_closed[gpt-4.1] |  92.3% (155/168) |  77.4% (130/168) |  72.6% (122/168) |
| ground_open[deepseek-v4-flash] |  77.4% (130/168) |  79.2% (133/168) |  79.2% (133/168) |
| ground_open[gpt-4.1] |  86.3% (145/168) |  83.9% (141/168) |  85.7% (144/168) |
| staged_closed[deepseek-v4-flash] |  92.3% (155/168) |  76.8% (129/168) |  64.9% (109/168) |
| staged_closed[gpt-4.1] |  92.9% (156/168) |  79.2% (133/168) |  70.2% (118/168) |
| staged_open[deepseek-v4-flash] |  78.0% (131/168) |  83.3% (140/168) |  79.2% (133/168) |
| staged_open[gpt-4.1] |  81.0% (136/168) |  79.2% (133/168) |  81.5% (137/168) |

### True-atom recall per atom (regime, tier)

| arm | atom | tier 0 | tier 1 | tier 2 |
|---|---|---|---|---|
| ground_closed | anonymized | 100.0% (10/10) |  70.0% (7/10) |  50.0% (5/10) |
| ground_closed | certified | 100.0% (20/20) |   5.0% (1/20) |   0.0% (0/20) |
| ground_closed | commercial |  95.0% (19/20) |  25.0% (5/20) |  70.0% (14/20) |
| ground_closed | consent |  96.4% (27/28) |  71.4% (20/28) |  17.9% (5/28) |
| ground_closed | emergency |  62.5% (10/16) |  56.2% (9/16) |   6.2% (1/16) |
| ground_closed | personal_data |  93.3% (28/30) |  66.7% (20/30) |  13.3% (4/30) |
| ground_closed | revoked | 100.0% (12/12) |  91.7% (11/12) | 100.0% (12/12) |
| ground_open | anonymized |  10.0% (1/10) |  60.0% (6/10) |  10.0% (1/10) |
| ground_open | certified |  80.0% (16/20) |  55.0% (11/20) |  65.0% (13/20) |
| ground_open | commercial | 100.0% (20/20) | 100.0% (20/20) | 100.0% (20/20) |
| ground_open | consent |  67.9% (19/28) |  60.7% (17/28) |  60.7% (17/28) |
| ground_open | emergency |  18.8% (3/16) |  12.5% (2/16) |   0.0% (0/16) |
| ground_open | personal_data |  90.0% (27/30) |  83.3% (25/30) |  93.3% (28/30) |
| ground_open | revoked |  58.3% (7/12) |  91.7% (11/12) |  91.7% (11/12) |
| staged_closed | anonymized | 100.0% (10/10) |  90.0% (9/10) |  10.0% (1/10) |
| staged_closed | certified | 100.0% (20/20) |   0.0% (0/20) |   0.0% (0/20) |
| staged_closed | commercial |  95.0% (19/20) |  20.0% (4/20) |  80.0% (16/20) |
| staged_closed | consent |  89.3% (25/28) |  75.0% (21/28) |  10.7% (3/28) |
| staged_closed | emergency |  68.8% (11/16) |  62.5% (10/16) |  12.5% (2/16) |
| staged_closed | personal_data |  93.3% (28/30) |  63.3% (19/30) |  13.3% (4/30) |
| staged_closed | revoked | 100.0% (12/12) |  66.7% (8/12) |  50.0% (6/12) |
| staged_open | anonymized |  20.0% (2/10) |  60.0% (6/10) |  20.0% (2/10) |
| staged_open | certified |  65.0% (13/20) |  60.0% (12/20) |  45.0% (9/20) |
| staged_open | commercial | 100.0% (20/20) | 100.0% (20/20) | 100.0% (20/20) |
| staged_open | consent |  53.6% (15/28) |  71.4% (20/28) |  64.3% (18/28) |
| staged_open | emergency |  25.0% (4/16) |   0.0% (0/16) |   0.0% (0/16) |
| staged_open | personal_data |  90.0% (27/30) |  76.7% (23/30) |  93.3% (28/30) |
| staged_open | revoked |  50.0% (6/12) | 100.0% (12/12) |  58.3% (7/12) |

## Acted subset: violation + remedy detection

| arm | violation acc | notify acc | n |
|---|---|---|---|
| ground_closed[deepseek-v4-flash] |  55.6% (10/18) |  77.8% (14/18) | 18 |
| ground_closed[gpt-4.1] |  61.1% (11/18) |  83.3% (15/18) | 18 |
| ground_open[deepseek-v4-flash] |  55.6% (10/18) |  44.4% (8/18) | 18 |
| ground_open[gpt-4.1] |  66.7% (12/18) |  50.0% (9/18) | 18 |
| holistic[deepseek-v4-flash] |  55.6% (10/18) |  44.4% (8/18) | 18 |
| holistic[gpt-4.1] |  61.1% (11/18) |  44.4% (8/18) | 18 |
| oracle | 100.0% (18/18) | 100.0% (18/18) | 18 |
| program |  77.8% (14/18) |  88.9% (16/18) | 18 |
| staged_closed[deepseek-v4-flash] |  66.7% (12/18) |  72.2% (13/18) | 18 |
| staged_closed[gpt-4.1] |  72.2% (13/18) |  83.3% (15/18) | 18 |
| staged_open[deepseek-v4-flash] |  61.1% (11/18) |  44.4% (8/18) | 18 |
| staged_open[gpt-4.1] |  61.1% (11/18) |  44.4% (8/18) | 18 |

## Mean tokens per case (LLM arms)

| arm | mean tokens | n |
|---|---|---|
| ground_closed[deepseek-v4-flash] | 1756 | 72 |
| ground_closed[gpt-4.1] | 719 | 72 |
| ground_open[deepseek-v4-flash] | 1590 | 72 |
| ground_open[gpt-4.1] | 646 | 72 |
| holistic[deepseek-v4-flash] | 1951 | 72 |
| holistic[gpt-4.1] | 867 | 72 |
| staged_closed[deepseek-v4-flash] | 4278 | 72 |
| staged_closed[gpt-4.1] | 2927 | 72 |
| staged_open[deepseek-v4-flash] | 4099 | 72 |
| staged_open[gpt-4.1] | 2863 | 72 |
