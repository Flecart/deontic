_(excluded 0 leak-flagged cases)_

## Act-verdict accuracy by arm x tier (3-class, baseline ~33-50%)

| arm | tier 0 | tier 1 | tier 2 |
|---|---|---|---|
| ground_closed[deepseek-v4-flash] |  86.8% (125/144) |  75.0% (108/144) |  84.0% (121/144) |
| ground_closed[gpt-4.1] |  87.5% (126/144) |  83.3% (120/144) |  81.9% (118/144) |
| ground_closed[qwen3.6-plus] |  86.8% (125/144) |  77.1% (111/144) |  86.1% (124/144) |
| ground_open[deepseek-v4-flash] |  46.5% (67/144) |  58.3% (84/144) |  50.7% (73/144) |
| ground_open[gpt-4.1] |  67.4% (97/144) |  77.1% (111/144) |  59.7% (86/144) |
| ground_open[qwen3.6-plus] |  79.9% (115/144) |  84.7% (122/144) |  72.9% (105/144) |
| holistic[deepseek-v4-flash] |  54.9% (79/144) |  60.4% (87/144) |  56.2% (81/144) |
| holistic[gpt-4.1] |  62.5% (90/144) |  70.1% (101/144) |  58.3% (84/144) |
| holistic[qwen3.6-plus] |  63.2% (91/144) |  71.5% (103/144) |  56.2% (81/144) |
| oracle | 100.0% (144/144) | 100.0% (144/144) | 100.0% (144/144) |
| program | 100.0% (144/144) |  33.3% (48/144) |  33.3% (48/144) |

## Atom-level grounding accuracy (regime x tier)

| regime[model] | tier 0 | tier 1 | tier 2 |
|---|---|---|---|
| ground_closed[deepseek-v4-flash] |  87.6% (1261/1440) |  84.7% (1219/1440) |  82.0% (1181/1440) |
| ground_closed[gpt-4.1] |  89.1% (1283/1440) |  86.0% (1238/1440) |  84.2% (1213/1440) |
| ground_closed[qwen3.6-plus] |  87.3% (1257/1440) |  83.3% (1199/1440) |  83.8% (1206/1440) |
| ground_open[deepseek-v4-flash] |  71.6% (1031/1440) |  75.6% (1088/1440) |  72.8% (1048/1440) |
| ground_open[gpt-4.1] |  79.2% (1141/1440) |  83.2% (1198/1440) |  81.5% (1174/1440) |
| ground_open[qwen3.6-plus] |  80.2% (1155/1440) |  80.3% (1156/1440) |  79.4% (1143/1440) |

### True-atom recall per atom (regime, tier)

| arm | atom | tier 0 | tier 1 | tier 2 |
|---|---|---|---|---|
| ground_closed | affects_third_parties | 100.0% (234/234) |  99.1% (232/234) | 100.0% (234/234) |
| ground_closed | averting_harm |  97.9% (141/144) |  79.9% (115/144) |  91.0% (131/144) |
| ground_closed | confirmed |  94.9% (148/156) |  77.6% (121/156) |  94.9% (148/156) |
| ground_closed | consequential |  99.7% (299/300) |  93.7% (281/300) |  96.3% (289/300) |
| ground_closed | contained |  50.0% (51/102) |  41.2% (42/102) |  66.7% (68/102) |
| ground_closed | dry_run_clean |  99.0% (190/192) |  99.5% (191/192) |  81.8% (157/192) |
| ground_closed | irreversible |  77.5% (172/222) |  74.3% (165/222) |  70.3% (156/222) |
| ground_closed | reversible_window |  93.7% (208/222) |  90.5% (201/222) |  94.6% (210/222) |
| ground_closed | runtime_certified | 100.0% (204/204) |  71.6% (146/204) |  51.5% (105/204) |
| ground_closed | within_authority |  74.1% (120/162) |  85.2% (138/162) |  84.0% (136/162) |
| ground_open | affects_third_parties |  99.6% (233/234) | 100.0% (234/234) | 100.0% (234/234) |
| ground_open | averting_harm |  48.6% (70/144) |  50.7% (73/144) |  47.9% (69/144) |
| ground_open | confirmed |  69.9% (109/156) | 100.0% (156/156) |  24.4% (38/156) |
| ground_open | consequential |  90.3% (271/300) |  85.3% (256/300) |  88.3% (265/300) |
| ground_open | contained |  35.3% (36/102) |  54.9% (56/102) |  56.9% (58/102) |
| ground_open | dry_run_clean |  72.9% (140/192) |  86.5% (166/192) |  56.8% (109/192) |
| ground_open | irreversible |  51.4% (114/222) |  40.1% (89/222) |  60.8% (135/222) |
| ground_open | reversible_window |  61.3% (136/222) |  73.0% (162/222) |  84.2% (187/222) |
| ground_open | runtime_certified |  47.1% (96/204) |  35.3% (72/204) |  72.5% (148/204) |
| ground_open | within_authority |  48.1% (78/162) |  79.0% (128/162) |  96.3% (156/162) |

## Remedy detection: rollback-owed + disclose-owed

| arm | rollback-owed acc | disclose-owed acc | n |
|---|---|---|---|
| ground_closed[deepseek-v4-flash] |  83.6% (361/432) |  83.6% (361/432) | 432 |
| ground_closed[gpt-4.1] |  85.6% (370/432) |  85.6% (370/432) | 432 |
| ground_closed[qwen3.6-plus] |  85.6% (370/432) |  85.6% (370/432) | 432 |
| ground_open[deepseek-v4-flash] |  65.3% (282/432) |  65.3% (282/432) | 432 |
| ground_open[gpt-4.1] |  75.9% (328/432) |  75.9% (328/432) | 432 |
| ground_open[qwen3.6-plus] |  81.0% (350/432) |  81.0% (350/432) | 432 |
| holistic[deepseek-v4-flash] |  69.0% (298/432) |  69.0% (298/432) | 432 |
| holistic[gpt-4.1] |  74.3% (321/432) |  74.3% (321/432) | 432 |
| holistic[qwen3.6-plus] |  75.2% (325/432) |  75.0% (324/432) | 432 |
| oracle | 100.0% (432/432) | 100.0% (432/432) | 432 |
| program |  77.8% (336/432) |  77.8% (336/432) | 432 |

## Paraphrase flip-rate (lower = more consistent)

| arm | flip-rate | groups |
|---|---|---|
| ground_closed[deepseek-v4-flash] |  14.8% (32/216) | 216 |
| ground_closed[gpt-4.1] |  15.7% (34/216) | 216 |
| ground_closed[qwen3.6-plus] |  17.1% (37/216) | 216 |
| ground_open[deepseek-v4-flash] |  37.5% (81/216) | 216 |
| ground_open[gpt-4.1] |  28.7% (62/216) | 216 |
| ground_open[qwen3.6-plus] |  19.4% (42/216) | 216 |
| holistic[deepseek-v4-flash] |  38.4% (83/216) | 216 |
| holistic[gpt-4.1] |  43.1% (93/216) | 216 |
| holistic[qwen3.6-plus] |  43.5% (94/216) | 216 |
| oracle |   0.0% (0/216) | 216 |
| program |   0.0% (0/216) | 216 |

## Mean tokens per case (LLM arms)

| arm | mean tokens | n |
|---|---|---|
| ground_closed[deepseek-v4-flash] | 1205 | 432 |
| ground_closed[gpt-4.1] | 877 | 432 |
| ground_closed[qwen3.6-plus] | 919 | 432 |
| ground_open[deepseek-v4-flash] | 2070 | 432 |
| ground_open[gpt-4.1] | 679 | 432 |
| ground_open[qwen3.6-plus] | 718 | 432 |
| holistic[deepseek-v4-flash] | 1006 | 432 |
| holistic[gpt-4.1] | 903 | 432 |
| holistic[qwen3.6-plus] | 966 | 432 |
