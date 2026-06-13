_(excluded 8 leak-flagged cases)_

## Honor-verdict accuracy by arm x tier

_majority-class baseline: t0 49.5%, t1 50.5%, t2 50.0%_

| arm | tier 0 | tier 1 | tier 2 |
|---|---|---|---|
| ground_closed[deepseek-v4-flash] |  93.5% (87/93) |  80.0% (76/95) |  78.3% (72/92) |
| ground_closed[gpt-4.1] |  94.6% (88/93) |  74.7% (71/95) |  66.3% (61/92) |
| ground_closed[gpt-5.4] |  95.7% (89/93) |  74.7% (71/95) |  59.8% (55/92) |
| ground_closed[qwen3.6-plus] |  94.6% (88/93) |  77.9% (74/95) |  69.6% (64/92) |
| ground_open[deepseek-v4-flash] |  72.0% (67/93) |  66.3% (63/95) |  78.3% (72/92) |
| ground_open[gpt-4.1] |  75.3% (70/93) |  66.3% (63/95) |  69.6% (64/92) |
| ground_open[gpt-5.4] |  76.3% (71/93) |  58.9% (56/95) |  62.0% (57/92) |
| ground_open[qwen3.6-plus] |  80.6% (75/93) |  78.9% (75/95) |  80.4% (74/92) |
| holistic[deepseek-v4-flash] |  72.0% (67/93) |  65.3% (62/95) |  76.1% (70/92) |
| holistic[gpt-4.1] |  64.5% (60/93) |  64.2% (61/95) |  66.3% (61/92) |
| holistic[gpt-5.4] |  82.8% (77/93) |  71.6% (68/95) |  80.4% (74/92) |
| holistic[qwen3.6-plus] |  59.1% (55/93) |  41.1% (39/95) |  48.9% (45/92) |
| oracle | 100.0% (93/93) | 100.0% (95/95) | 100.0% (92/92) |
| program | 100.0% (93/93) |   2.1% (2/95) |   2.2% (2/92) |

## Atom-level grounding accuracy (regime x tier)

| regime[model] | tier 0 | tier 1 | tier 2 |
|---|---|---|---|
| ground_closed[deepseek-v4-flash] |  90.5% (673/744) |  84.1% (639/760) |  79.9% (588/736) |
| ground_closed[gpt-4.1] |  94.8% (705/744) |  84.1% (639/760) |  78.1% (575/736) |
| ground_closed[gpt-5.4] |  93.8% (698/744) |  81.3% (618/760) |  75.7% (557/736) |
| ground_closed[qwen3.6-plus] |  94.0% (699/744) |  86.6% (658/760) |  80.7% (594/736) |
| ground_open[deepseek-v4-flash] |  80.6% (600/744) |  78.2% (594/760) |  83.7% (616/736) |
| ground_open[gpt-4.1] |  78.6% (585/744) |  77.0% (585/760) |  78.8% (580/736) |
| ground_open[gpt-5.4] |  80.5% (599/744) |  79.3% (603/760) |  81.1% (597/736) |
| ground_open[qwen3.6-plus] |  84.4% (628/744) |  83.0% (631/760) |  84.9% (625/736) |

### True-atom recall per atom (regime, tier)

| arm | atom | tier 0 | tier 1 | tier 2 |
|---|---|---|---|---|
| ground_closed | authority_manifested | 100.0% (168/168) |  60.2% (106/176) |  89.9% (151/168) |
| ground_closed | counterparty_good_faith |  91.3% (179/196) |  83.0% (166/200) |  57.3% (110/192) |
| ground_closed | mandate_revoked |  99.7% (299/300) |  92.9% (286/308) |  95.4% (290/304) |
| ground_closed | ratified |  88.6% (124/140) |  49.3% (69/140) |  44.3% (62/140) |
| ground_closed | revocation_published |  97.9% (141/144) |  81.8% (121/148) |  37.2% (55/148) |
| ground_closed | self_dealing | 100.0% (180/180) |  92.8% (167/180) |  79.4% (143/180) |
| ground_closed | urgent_necessity |  88.5% (46/52) |  80.4% (45/56) |  42.3% (22/52) |
| ground_closed | within_scope |  61.0% (122/200) |  29.3% (61/208) |   7.5% (15/200) |
| ground_open | authority_manifested |  92.9% (156/168) |  86.9% (153/176) |  92.3% (155/168) |
| ground_open | counterparty_good_faith |  67.3% (132/196) |  57.0% (114/200) |  70.8% (136/192) |
| ground_open | mandate_revoked |  92.3% (277/300) |  96.1% (296/308) |  97.0% (295/304) |
| ground_open | ratified |  34.3% (48/140) |   9.3% (13/140) |  38.6% (54/140) |
| ground_open | revocation_published |  84.0% (121/144) |  85.1% (126/148) |  96.6% (143/148) |
| ground_open | self_dealing | 100.0% (180/180) |  98.3% (177/180) |  81.7% (147/180) |
| ground_open | urgent_necessity |  71.2% (37/52) |  57.1% (32/56) |  57.7% (30/52) |
| ground_open | within_scope |  51.5% (103/200) |  54.3% (113/208) |  63.0% (126/200) |

## Acted subset (company already refused): violation + notice duty

| arm | wrongful-refusal acc | notice-duty acc | n |
|---|---|---|---|
| ground_closed[deepseek-v4-flash] |  82.1% (124/151) |  68.2% (103/151) | 151 |
| ground_closed[gpt-4.1] |  77.5% (117/151) |  67.5% (102/151) | 151 |
| ground_closed[gpt-5.4] |  78.8% (119/151) |  68.9% (104/151) | 151 |
| ground_closed[qwen3.6-plus] |  78.1% (118/151) |  69.5% (105/151) | 151 |
| ground_open[deepseek-v4-flash] |  67.5% (102/151) |  61.6% (93/151) | 151 |
| ground_open[gpt-4.1] |  67.5% (102/151) |  68.2% (103/151) | 151 |
| ground_open[gpt-5.4] |  63.6% (96/151) |  66.2% (100/151) | 151 |
| ground_open[qwen3.6-plus] |  78.1% (118/151) |  74.8% (113/151) | 151 |
| holistic[deepseek-v4-flash] |  55.6% (84/151) |  58.9% (89/151) | 151 |
| holistic[gpt-4.1] |  61.6% (93/151) |  58.9% (89/151) | 151 |
| holistic[gpt-5.4] |  77.5% (117/151) |  72.8% (110/151) | 151 |
| holistic[qwen3.6-plus] |  72.2% (109/151) |  64.2% (97/151) | 151 |
| oracle | 100.0% (151/151) | 100.0% (151/151) | 151 |
| program |  64.2% (97/151) |  69.5% (105/151) | 151 |

## Sub-agent conduct-duty breach detection (engine-mediated arms)

| arm | breach acc | n |
|---|---|---|
| ground_closed[deepseek-v4-flash] |  93.9% (263/280) | 280 |
| ground_closed[gpt-4.1] |  91.1% (255/280) | 280 |
| ground_closed[gpt-5.4] |  88.2% (247/280) | 280 |
| ground_closed[qwen3.6-plus] |  94.6% (265/280) | 280 |
| ground_open[deepseek-v4-flash] |  93.2% (261/280) | 280 |
| ground_open[gpt-4.1] |  91.8% (257/280) | 280 |
| ground_open[gpt-5.4] |  86.4% (242/280) | 280 |
| ground_open[qwen3.6-plus] |  95.7% (268/280) | 280 |
| oracle | 100.0% (280/280) | 280 |
| program |  48.2% (135/280) | 280 |

## Paraphrase flip-rate (honor verdict)

| arm | flip-rate | groups |
|---|---|---|
| ground_closed[deepseek-v4-flash] |  22.8% (31/136) | 136 |
| ground_closed[gpt-4.1] |  25.0% (34/136) | 136 |
| ground_closed[gpt-5.4] |  22.8% (31/136) | 136 |
| ground_closed[qwen3.6-plus] |  20.6% (28/136) | 136 |
| ground_open[deepseek-v4-flash] |  26.5% (36/136) | 136 |
| ground_open[gpt-4.1] |  24.3% (33/136) | 136 |
| ground_open[gpt-5.4] |  30.1% (41/136) | 136 |
| ground_open[qwen3.6-plus] |  25.0% (34/136) | 136 |
| holistic[deepseek-v4-flash] |  23.5% (32/136) | 136 |
| holistic[gpt-4.1] |  22.1% (30/136) | 136 |
| holistic[gpt-5.4] |  30.1% (41/136) | 136 |
| holistic[qwen3.6-plus] |  31.6% (43/136) | 136 |
| oracle |   0.0% (0/136) | 136 |
| program |   0.0% (0/136) | 136 |
