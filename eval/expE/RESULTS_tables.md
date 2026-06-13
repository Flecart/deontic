_(excluded 6 leak-flagged cases)_

## Accept-verdict accuracy by arm x tier (majority baseline ~50%)

| arm | tier 0 | tier 1 | tier 2 |
|---|---|---|---|
| ground_closed[deepseek-v4-flash] |  91.4% (127/139) |  84.0% (121/144) |  90.2% (129/143) |
| ground_closed[gpt-4.1] |  90.6% (126/139) |  84.0% (121/144) |  90.2% (129/143) |
| ground_closed[qwen3.6-plus] |  91.4% (127/139) |  79.9% (115/144) |  91.6% (131/143) |
| ground_open[deepseek-v4-flash] |  89.9% (125/139) |  82.6% (119/144) |  88.8% (127/143) |
| ground_open[gpt-4.1] |  92.8% (129/139) |  78.5% (113/144) |  92.3% (132/143) |
| ground_open[qwen3.6-plus] |  88.5% (123/139) |  81.2% (117/144) |  88.1% (126/143) |
| holistic[deepseek-v4-flash] |  74.8% (104/139) |  66.7% (96/144) |  78.3% (112/143) |
| holistic[gpt-4.1] |  76.3% (106/139) |  63.2% (91/144) |  60.1% (86/143) |
| holistic[qwen3.6-plus] |  75.5% (105/139) |  61.1% (88/144) |  75.5% (108/143) |
| oracle | 100.0% (139/139) | 100.0% (144/144) | 100.0% (143/143) |
| program | 100.0% (139/139) |   1.4% (2/144) |   1.4% (2/143) |

## Atom-level grounding accuracy (regime x tier)

| regime[model] | tier 0 | tier 1 | tier 2 |
|---|---|---|---|
| ground_closed[deepseek-v4-flash] |  89.0% (1113/1251) |  86.3% (1118/1296) |  87.6% (1128/1287) |
| ground_closed[gpt-4.1] |  92.1% (1152/1251) |  89.5% (1160/1296) |  89.7% (1154/1287) |
| ground_closed[qwen3.6-plus] |  90.9% (1137/1251) |  88.6% (1148/1296) |  89.9% (1157/1287) |
| ground_open[deepseek-v4-flash] |  86.0% (1076/1251) |  86.2% (1117/1296) |  87.5% (1126/1287) |
| ground_open[gpt-4.1] |  88.5% (1107/1251) |  86.1% (1116/1296) |  89.9% (1157/1287) |
| ground_open[qwen3.6-plus] |  87.6% (1096/1251) |  87.6% (1135/1296) |  88.9% (1144/1287) |

### True-atom recall per atom (regime, tier)

| arm | atom | tier 0 | tier 1 | tier 2 |
|---|---|---|---|---|
| ground_closed | accepted_by_use |  95.4% (146/153) | 100.0% (162/162) |  93.2% (151/162) |
| ground_closed | as_is |  99.5% (209/210) |  98.6% (213/216) | 100.0% (216/216) |
| ground_closed | conforming |  26.9% (42/156) |   8.3% (13/156) |  32.1% (50/156) |
| ground_closed | cure_offered |  98.5% (195/198) |  98.1% (206/210) |  97.6% (202/207) |
| ground_closed | fitness_breached | 100.0% (195/195) |  98.5% (201/204) |  92.2% (188/204) |
| ground_closed | late_essential |  97.5% (117/120) |  49.2% (59/120) |  95.7% (112/117) |
| ground_closed | latent_defect |  97.4% (187/192) |  93.4% (185/198) |  91.4% (181/198) |
| ground_closed | material_defect | 100.0% (327/327) |  91.5% (313/342) |  95.0% (325/342) |
| ground_closed | merchantable |  37.3% (75/201) |  43.6% (89/204) |  17.9% (36/201) |
| ground_open | accepted_by_use |  88.9% (136/153) |  98.1% (159/162) |  90.7% (147/162) |
| ground_open | as_is |  75.7% (159/210) |  97.2% (210/216) | 100.0% (216/216) |
| ground_open | conforming |  29.5% (46/156) |  12.2% (19/156) |  34.0% (53/156) |
| ground_open | cure_offered |  99.5% (197/198) |  97.6% (205/210) |  97.1% (201/207) |
| ground_open | fitness_breached |  99.0% (193/195) |  78.4% (160/204) |  93.1% (190/204) |
| ground_open | late_essential |  90.8% (109/120) |  40.0% (48/120) |  94.9% (111/117) |
| ground_open | latent_defect |  91.1% (175/192) |  96.5% (191/198) |  90.9% (180/198) |
| ground_open | material_defect |  96.0% (314/327) |  90.1% (308/342) |  94.4% (323/342) |
| ground_open | merchantable |  34.8% (70/201) |  34.8% (71/204) |  32.8% (66/201) |

## Remedy detection: seller-cure-owed + refund-owed

| arm | cure-owed acc | refund-owed acc | n |
|---|---|---|---|
| ground_closed[deepseek-v4-flash] |  97.4% (415/426) |  89.9% (383/426) | 426 |
| ground_closed[gpt-4.1] |  94.1% (401/426) |  89.2% (380/426) | 426 |
| ground_closed[qwen3.6-plus] |  95.3% (406/426) |  89.0% (379/426) | 426 |
| ground_open[deepseek-v4-flash] |  90.6% (386/426) |  87.6% (373/426) | 426 |
| ground_open[gpt-4.1] |  89.2% (380/426) |  88.7% (378/426) | 426 |
| ground_open[qwen3.6-plus] |  91.3% (389/426) |  87.1% (371/426) | 426 |
| holistic[deepseek-v4-flash] |  89.4% (381/426) |  74.6% (318/426) | 426 |
| holistic[gpt-4.1] |  71.8% (306/426) |  69.2% (295/426) | 426 |
| holistic[qwen3.6-plus] |  59.2% (252/426) |  61.0% (260/426) | 426 |
| oracle | 100.0% (426/426) | 100.0% (426/426) | 426 |
| program |  46.5% (198/426) |  66.4% (283/426) | 426 |

## Paraphrase flip-rate (lower = more consistent)

| arm | flip-rate | groups |
|---|---|---|
| ground_closed[deepseek-v4-flash] |  13.3% (28/210) | 210 |
| ground_closed[gpt-4.1] |  12.9% (27/210) | 210 |
| ground_closed[qwen3.6-plus] |  11.9% (25/210) | 210 |
| ground_open[deepseek-v4-flash] |  12.9% (27/210) | 210 |
| ground_open[gpt-4.1] |  11.4% (24/210) | 210 |
| ground_open[qwen3.6-plus] |  13.3% (28/210) | 210 |
| holistic[deepseek-v4-flash] |  26.7% (56/210) | 210 |
| holistic[gpt-4.1] |  21.9% (46/210) | 210 |
| holistic[qwen3.6-plus] |  24.8% (52/210) | 210 |
| oracle |   0.0% (0/210) | 210 |
| program |   0.0% (0/210) | 210 |

## Mean tokens per case (LLM arms)

| arm | mean tokens | n |
|---|---|---|
| ground_closed[deepseek-v4-flash] | 975 | 426 |
| ground_closed[gpt-4.1] | 880 | 426 |
| ground_closed[qwen3.6-plus] | 917 | 426 |
| ground_open[deepseek-v4-flash] | 783 | 426 |
| ground_open[gpt-4.1] | 711 | 426 |
| ground_open[qwen3.6-plus] | 746 | 426 |
| holistic[deepseek-v4-flash] | 4707 | 426 |
| holistic[gpt-4.1] | 937 | 426 |
| holistic[qwen3.6-plus] | 965 | 426 |
