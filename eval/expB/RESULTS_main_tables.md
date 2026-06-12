_(excluded 0 leak-flagged cases)_

## Verdict accuracy (draw status) by arm x tier

| arm | tier 0 | tier 1 | tier 2 |
|---|---|---|---|
| ground_closed[deepseek-v4-flash] |  90.6% (87/96) |  61.5% (59/96) |  38.5% (37/96) |
| ground_closed[gpt-4.1] |  97.9% (94/96) |  76.0% (73/96) |  49.0% (47/96) |
| ground_closed[gpt-5.4] |  96.9% (93/96) |  84.4% (81/96) |  51.0% (49/96) |
| ground_closed[qwen3.6-plus] |  99.0% (95/96) |  89.6% (86/96) |  54.2% (52/96) |
| ground_open[deepseek-v4-flash] |  62.5% (60/96) |  61.5% (59/96) |  65.6% (63/96) |
| ground_open[gpt-4.1] |  79.2% (76/96) |  76.0% (73/96) |  81.2% (78/96) |
| ground_open[gpt-5.4] |  69.8% (67/96) |  64.6% (62/96) |  66.7% (64/96) |
| ground_open[qwen3.6-plus] |  90.6% (87/96) |  88.5% (85/96) |  81.2% (78/96) |
| holistic[deepseek-v4-flash] |  61.5% (59/96) |  60.4% (58/96) |  69.8% (67/96) |
| holistic[gpt-4.1] |  67.7% (65/96) |  58.3% (56/96) |  65.6% (63/96) |
| holistic[gpt-5.4] |  90.6% (87/96) |  80.2% (77/96) |  80.2% (77/96) |
| holistic[qwen3.6-plus] |  86.5% (83/96) |  81.2% (78/96) |  76.0% (73/96) |
| oracle | 100.0% (96/96) | 100.0% (96/96) | 100.0% (96/96) |
| program | 100.0% (96/96) |  35.4% (34/96) |  35.4% (34/96) |

## Atom-level grounding accuracy (regime x tier)

| regime[model] | tier 0 | tier 1 | tier 2 |
|---|---|---|---|
| ground_closed[deepseek-v4-flash] |  96.6% (649/672) |  79.3% (533/672) |  58.5% (393/672) |
| ground_closed[gpt-4.1] |  98.2% (660/672) |  88.2% (593/672) |  78.3% (526/672) |
| ground_closed[gpt-5.4] |  98.4% (661/672) |  84.2% (566/672) |  64.4% (433/672) |
| ground_closed[qwen3.6-plus] |  97.0% (652/672) |  87.2% (586/672) |  79.9% (537/672) |
| ground_open[deepseek-v4-flash] |  79.3% (533/672) |  75.1% (505/672) |  74.1% (498/672) |
| ground_open[gpt-4.1] |  87.9% (591/672) |  86.5% (581/672) |  89.6% (602/672) |
| ground_open[gpt-5.4] |  87.8% (590/672) |  82.7% (556/672) |  82.6% (555/672) |
| ground_open[qwen3.6-plus] |  85.7% (576/672) |  81.7% (549/672) |  85.4% (574/672) |

### True-atom recall per atom (regime, tier)

| arm | atom | tier 0 | tier 1 | tier 2 |
|---|---|---|---|---|
| ground_closed | allocation_granted |  95.4% (229/240) |  73.3% (176/240) |  38.3% (92/240) |
| ground_closed | contention | 100.0% (184/184) |  64.7% (119/184) |  38.0% (70/184) |
| ground_closed | essential_workload |  91.2% (146/160) |  68.1% (109/160) |  28.8% (46/160) |
| ground_closed | grant_suspended |  97.7% (125/128) |  64.8% (83/128) |  72.7% (93/128) |
| ground_closed | offset_posted |  98.1% (157/160) |  96.9% (155/160) |  23.1% (37/160) |
| ground_closed | over_quota |  98.2% (330/336) |  79.8% (268/336) |  46.1% (155/336) |
| ground_closed | priority_certified |  99.5% (183/184) |  55.4% (102/184) |  62.0% (114/184) |
| ground_open | allocation_granted |  82.1% (197/240) |  73.3% (176/240) |  67.9% (163/240) |
| ground_open | contention |  76.1% (140/184) |  51.1% (94/184) |  42.9% (79/184) |
| ground_open | essential_workload |  63.1% (101/160) |  56.2% (90/160) |  72.5% (116/160) |
| ground_open | grant_suspended |  76.6% (98/128) |  92.2% (118/128) |  85.9% (110/128) |
| ground_open | offset_posted |  58.8% (94/160) |  83.8% (134/160) |  55.6% (89/160) |
| ground_open | over_quota |  89.0% (299/336) |  73.2% (246/336) |  76.2% (256/336) |
| ground_open | priority_certified |  71.7% (132/184) |  52.7% (97/184) |  87.0% (160/184) |

## Acted subset: violation + remedy detection

| arm | violation acc | report acc | n |
|---|---|---|---|
| ground_closed[deepseek-v4-flash] |  69.3% (79/114) |  78.9% (90/114) | 114 |
| ground_closed[gpt-4.1] |  85.1% (97/114) |  87.7% (100/114) | 114 |
| ground_closed[gpt-5.4] |  80.7% (92/114) |  82.5% (94/114) | 114 |
| ground_closed[qwen3.6-plus] |  85.1% (97/114) |  86.8% (99/114) | 114 |
| ground_open[deepseek-v4-flash] |  68.4% (78/114) |  71.9% (82/114) | 114 |
| ground_open[gpt-4.1] |  81.6% (93/114) |  85.1% (97/114) | 114 |
| ground_open[gpt-5.4] |  78.1% (89/114) |  81.6% (93/114) | 114 |
| ground_open[qwen3.6-plus] |  80.7% (92/114) |  82.5% (94/114) | 114 |
| holistic[deepseek-v4-flash] |  75.4% (86/114) |  75.4% (86/114) | 114 |
| holistic[gpt-4.1] |  76.3% (87/114) |  78.9% (90/114) | 114 |
| holistic[gpt-5.4] |  83.3% (95/114) |  85.1% (97/114) | 114 |
| holistic[qwen3.6-plus] |  73.7% (84/114) |  78.9% (90/114) | 114 |
| oracle | 100.0% (114/114) | 100.0% (114/114) | 114 |
| program |  75.4% (86/114) |  78.9% (90/114) | 114 |

## Paraphrase flip-rate (lower = more consistent)

| arm | flip-rate | groups |
|---|---|---|
| ground_closed[deepseek-v4-flash] |  31.2% (45/144) | 144 |
| ground_closed[gpt-4.1] |  21.5% (31/144) | 144 |
| ground_closed[gpt-5.4] |  26.4% (38/144) | 144 |
| ground_closed[qwen3.6-plus] |  18.8% (27/144) | 144 |
| ground_open[deepseek-v4-flash] |  47.2% (68/144) | 144 |
| ground_open[gpt-4.1] |  32.6% (47/144) | 144 |
| ground_open[gpt-5.4] |  34.0% (49/144) | 144 |
| ground_open[qwen3.6-plus] |  20.1% (29/144) | 144 |
| holistic[deepseek-v4-flash] |  31.2% (45/144) | 144 |
| holistic[gpt-4.1] |  31.9% (46/144) | 144 |
| holistic[gpt-5.4] |  20.8% (30/144) | 144 |
| holistic[qwen3.6-plus] |  20.8% (30/144) | 144 |
| oracle |   0.0% (0/144) | 144 |
| program |   0.0% (0/144) | 144 |

## Mean tokens per case (LLM arms)

| arm | mean tokens | n |
|---|---|---|
| ground_closed[deepseek-v4-flash] | 1954 | 288 |
| ground_closed[gpt-4.1] | 737 | 288 |
| ground_closed[gpt-5.4] | 726 | 288 |
| ground_closed[qwen3.6-plus] | 776 | 288 |
| ground_open[deepseek-v4-flash] | 2271 | 288 |
| ground_open[gpt-4.1] | 659 | 288 |
| ground_open[gpt-5.4] | 647 | 288 |
| ground_open[qwen3.6-plus] | 697 | 288 |
| holistic[deepseek-v4-flash] | 996 | 288 |
| holistic[gpt-4.1] | 881 | 288 |
| holistic[gpt-5.4] | 874 | 288 |
| holistic[qwen3.6-plus] | 920 | 288 |
