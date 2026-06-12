_(excluded 1 leak-flagged cases)_

## Verdict accuracy (share status) by arm x tier

| arm | tier 0 | tier 1 | tier 2 |
|---|---|---|---|
| ground_closed[deepseek-v4-flash] |  90.6% (87/96) |  90.5% (86/95) |  59.4% (57/96) |
| ground_closed[gpt-4.1] |  88.5% (85/96) |  78.9% (75/95) |  70.8% (68/96) |
| ground_closed[gpt-5.4] |  92.7% (89/96) |  56.8% (54/95) |  42.7% (41/96) |
| ground_closed[qwen3.6-plus] |  94.8% (91/96) |  66.3% (63/95) |  69.8% (67/96) |
| ground_open[deepseek-v4-flash] |  61.5% (59/96) |  46.3% (44/95) |  50.0% (48/96) |
| ground_open[gpt-4.1] |  77.1% (74/96) |  65.3% (62/95) |  66.7% (64/96) |
| ground_open[gpt-5.4] |  41.7% (40/96) |  37.9% (36/95) |  43.8% (42/96) |
| ground_open[qwen3.6-plus] |  72.9% (70/96) |  64.2% (61/95) |  69.8% (67/96) |
| holistic[deepseek-v4-flash] |  78.1% (75/96) |  63.2% (60/95) |  54.2% (52/96) |
| holistic[gpt-4.1] |  72.9% (70/96) |  55.8% (53/95) |  56.2% (54/96) |
| holistic[gpt-5.4] |  83.3% (80/96) |  72.6% (69/95) |  75.0% (72/96) |
| holistic[qwen3.6-plus] |  86.5% (83/96) |  71.6% (68/95) |  78.1% (75/96) |
| oracle | 100.0% (96/96) | 100.0% (95/95) | 100.0% (96/96) |
| program | 100.0% (96/96) |  34.7% (33/95) |  35.4% (34/96) |

## Atom-level grounding accuracy (regime x tier)

| regime[model] | tier 0 | tier 1 | tier 2 |
|---|---|---|---|
| ground_closed[deepseek-v4-flash] |  93.8% (630/672) |  78.2% (520/665) |  61.3% (412/672) |
| ground_closed[gpt-4.1] |  91.7% (616/672) |  75.8% (504/665) |  67.9% (456/672) |
| ground_closed[gpt-5.4] |  95.2% (640/672) |  67.8% (451/665) |  55.4% (372/672) |
| ground_closed[qwen3.6-plus] |  92.6% (622/672) |  77.4% (515/665) |  70.5% (474/672) |
| ground_open[deepseek-v4-flash] |  77.8% (523/672) |  76.8% (511/665) |  76.2% (512/672) |
| ground_open[gpt-4.1] |  86.3% (580/672) |  85.4% (568/665) |  84.2% (566/672) |
| ground_open[gpt-5.4] |  80.7% (542/672) |  76.5% (509/665) |  80.1% (538/672) |
| ground_open[qwen3.6-plus] |  84.1% (565/672) |  81.8% (544/665) |  83.6% (562/672) |

### True-atom recall per atom (regime, tier)

| arm | atom | tier 0 | tier 1 | tier 2 |
|---|---|---|---|---|
| ground_closed | anonymized |  91.9% (147/160) |  95.0% (152/160) |  45.0% (72/160) |
| ground_closed | certified | 100.0% (200/200) |   1.5% (3/200) |   1.0% (2/200) |
| ground_closed | commercial |  94.0% (173/184) |  25.0% (46/184) |  38.0% (70/184) |
| ground_closed | consent |  91.8% (191/208) |  58.3% (119/204) |  22.6% (47/208) |
| ground_closed | emergency |  93.1% (149/160) |  63.8% (102/160) |  50.0% (80/160) |
| ground_closed | personal_data |  74.1% (237/320) |  60.1% (190/316) |  17.2% (55/320) |
| ground_closed | revoked |  99.1% (111/112) |  70.5% (79/112) |  75.0% (84/112) |
| ground_open | anonymized |  45.0% (72/160) |  55.0% (88/160) |  38.8% (62/160) |
| ground_open | certified |  82.0% (164/200) |  69.0% (138/200) |  59.5% (119/200) |
| ground_open | commercial | 100.0% (184/184) | 100.0% (184/184) |  99.5% (183/184) |
| ground_open | consent |  65.9% (137/208) |  63.7% (130/204) |  85.6% (178/208) |
| ground_open | emergency |  47.5% (76/160) |  16.2% (26/160) |  38.1% (61/160) |
| ground_open | personal_data |  61.2% (196/320) |  62.3% (197/316) |  67.8% (217/320) |
| ground_open | revoked |  84.8% (95/112) |  91.1% (102/112) |  69.6% (78/112) |

## Acted subset: violation + remedy detection

| arm | violation acc | notify acc | n |
|---|---|---|---|
| ground_closed[deepseek-v4-flash] |  87.5% (105/120) |  93.3% (112/120) | 120 |
| ground_closed[gpt-4.1] |  90.8% (109/120) |  92.5% (111/120) | 120 |
| ground_closed[gpt-5.4] |  80.0% (96/120) |  86.7% (104/120) | 120 |
| ground_closed[qwen3.6-plus] |  88.3% (106/120) |  90.8% (109/120) | 120 |
| ground_open[deepseek-v4-flash] |  60.0% (72/120) |  74.2% (89/120) | 120 |
| ground_open[gpt-4.1] |  85.0% (102/120) |  82.5% (99/120) | 120 |
| ground_open[gpt-5.4] |  45.8% (55/120) |  55.0% (66/120) | 120 |
| ground_open[qwen3.6-plus] |  77.5% (93/120) |  74.2% (89/120) | 120 |
| holistic[deepseek-v4-flash] |  70.8% (85/120) |  69.2% (83/120) | 120 |
| holistic[gpt-4.1] |  72.5% (87/120) |  67.5% (81/120) | 120 |
| holistic[gpt-5.4] |  80.0% (96/120) |  77.5% (93/120) | 120 |
| holistic[qwen3.6-plus] |  83.3% (100/120) |  78.3% (94/120) | 120 |
| oracle | 100.0% (120/120) | 100.0% (120/120) | 120 |
| program |  86.7% (104/120) |  90.0% (108/120) | 120 |

## Paraphrase flip-rate (lower = more consistent)

| arm | flip-rate | groups |
|---|---|---|
| ground_closed[deepseek-v4-flash] |  21.0% (30/143) | 143 |
| ground_closed[gpt-4.1] |  25.2% (36/143) | 143 |
| ground_closed[gpt-5.4] |  35.0% (50/143) | 143 |
| ground_closed[qwen3.6-plus] |  24.5% (35/143) | 143 |
| ground_open[deepseek-v4-flash] |  34.3% (49/143) | 143 |
| ground_open[gpt-4.1] |  26.6% (38/143) | 143 |
| ground_open[gpt-5.4] |  24.5% (35/143) | 143 |
| ground_open[qwen3.6-plus] |  27.3% (39/143) | 143 |
| holistic[deepseek-v4-flash] |  33.6% (48/143) | 143 |
| holistic[gpt-4.1] |  29.4% (42/143) | 143 |
| holistic[gpt-5.4] |  28.7% (41/143) | 143 |
| holistic[qwen3.6-plus] |  25.9% (37/143) | 143 |
| oracle |   0.0% (0/143) | 143 |
| program |   0.0% (0/143) | 143 |

## Mean tokens per case (LLM arms)

| arm | mean tokens | n |
|---|---|---|
| ground_closed[deepseek-v4-flash] | 1400 | 287 |
| ground_closed[gpt-4.1] | 727 | 287 |
| ground_closed[gpt-5.4] | 716 | 287 |
| ground_closed[qwen3.6-plus] | 774 | 287 |
| ground_open[deepseek-v4-flash] | 1883 | 287 |
| ground_open[gpt-4.1] | 655 | 287 |
| ground_open[gpt-5.4] | 643 | 287 |
| ground_open[qwen3.6-plus] | 693 | 287 |
| holistic[deepseek-v4-flash] | 2266 | 287 |
| holistic[gpt-4.1] | 875 | 287 |
| holistic[gpt-5.4] | 870 | 287 |
| holistic[qwen3.6-plus] | 918 | 287 |
