# STP Config Flood (`net_stp_conf_flood`)

[Índice da campanha](README.md)

Na campanha `experiments/60att_5runs_l0l1l2l3`, este documento consolida a execução do ataque `net_stp_conf_flood`. No catálogo local, o ataque é descrito como: BPDU (Bridge Protocol Data Unit) packet flood with STP topology reconfiguration information and random MAC addresses. A documentação abaixo usa apenas artefatos já presentes no repositório, principalmente as tabelas e figuras de `experiments/60att_5runs_l0l1l2l3/net_stp_conf_flood`.

## Metadados do ataque

| Campo | Valor |
| --- | --- |
| ID | `net_stp_conf_flood` |
| Categoria | 2) Network Interception and Exploitation |
| Subcategoria | 2.1 L2/L3 |
| Serviços alvo | local network |
| Imagem | `attack-stp-conf-flood:latest` |
| Container | `attack-stp-conf-flood` |
| Runtime máximo do catálogo | 10 s |
| Parâmetros de intensidade | n/d |
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0040/](https://attack.mitre.org/tactics/TA0040/)<br>[https://attack.mitre.org/techniques/T1498/](https://attack.mitre.org/techniques/T1498/)<br>[https://attack.mitre.org/techniques/T1498/001/](https://attack.mitre.org/techniques/T1498/001/)<br>[https://attack.mitre.org/techniques/T1565/](https://attack.mitre.org/techniques/T1565/)<br>[https://attack.mitre.org/techniques/T1565/002/](https://attack.mitre.org/techniques/T1565/002/) |

## Resumo estatístico por nível

| Nível | Serviço | Runs | Amostras attack | Sucesso médio | Falha média | Lat p50/p95 ms | PCAP total MB | Dataset médio (min-max) | Exec média s | Extratores ok/total | CPU média/máx | Mem MB média |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | http | 5 | 199 | 100% | 0% | 4,1 / 4,61 | 5,05 | 9.599 (9.592-9.606) | 43,29 | 3/3 | 0,62% / 0,69% | 140,26 |
| L1 | http | 5 | 200 | 100% | 0% | 4,62 / 6,61 | 49,39 | 260.994 (134.940-404.352) | 57,29 | 3/3 | 0,73% / 0,91% | 142,42 |
| L2 | http | 5 | 200 | 100% | 0% | 5,42 / 7,14 | 41,73 | 217.553 (78.536-420.104) | 55,07 | 3/3 | 0,83% / 1,04% | 144,51 |
| L3 | http | 5 | 200 | 100% | 0% | 5,45 / 7,32 | 36,45 | 187.698 (94.272-321.442) | 53,33 | 3/3 | 0,86% / 1,09% | 146,61 |

## Estabilidade entre reexecuções

| Nível | Métrica | Runs | Média | Desvio | CV | Min | Max |
| --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | CPU média na fase attack | 5 | 0,62 | 0,04 | 6,06% | 0,59 | 0,68 |
| L0 | Linhas do dataset | 5 | 9.599,2 | 6,72 | 0,07% | 9.592 | 9.606 |
| L0 | Tempo de execução | 5 | 43,29 | 0,97 | 2,23% | 42,84 | 45,02 |
| L0 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L0 | Latência p95 censurada | 5 | 4,61 | 0,3 | 6,55% | 4,38 | 5,13 |
| L1 | CPU média na fase attack | 5 | 0,73 | 0,08 | 10,9% | 0,66 | 0,85 |
| L1 | Linhas do dataset | 5 | 260.994,4 | 110.048,17 | 42,16% | 134.940 | 404.352 |
| L1 | Tempo de execução | 5 | 57,29 | 6,31 | 11,01% | 50,14 | 65,54 |
| L1 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L1 | Latência p95 censurada | 5 | 6,61 | 1,22 | 18,43% | 5,17 | 8,07 |
| L2 | CPU média na fase attack | 5 | 0,83 | 0,05 | 6,26% | 0,78 | 0,92 |
| L2 | Linhas do dataset | 5 | 217.552,8 | 160.975,85 | 73,99% | 78.536 | 420.104 |
| L2 | Tempo de execução | 5 | 55,07 | 9,16 | 16,63% | 47 | 66,46 |
| L2 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L2 | Latência p95 censurada | 5 | 7,14 | 0,39 | 5,48% | 6,61 | 7,69 |
| L3 | CPU média na fase attack | 5 | 0,86 | 0,07 | 8,59% | 0,79 | 0,98 |
| L3 | Linhas do dataset | 5 | 187.697,6 | 95.071,1 | 50,65% | 94.272 | 321.442 |
| L3 | Tempo de execução | 5 | 53,33 | 5,5 | 10,32% | 47,85 | 60,91 |
| L3 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L3 | Latência p95 censurada | 5 | 7,32 | 0,77 | 10,46% | 6,63 | 8,22 |

## Validação de artefatos

| Nível | Runs | Captura | Probe | Features | Dataset | Recursos | Server stats | Aceite |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | 5 | 5/5 | 5/5 | 5/5 | 5/5 | 5/5 | 5/5 | 5/5 |
| L1 | 5 | 5/5 | 5/5 | 5/5 | 5/5 | 5/5 | 5/5 | 5/5 |
| L2 | 5 | 5/5 | 5/5 | 5/5 | 5/5 | 5/5 | 5/5 | 5/5 |
| L3 | 5 | 5/5 | 5/5 | 5/5 | 5/5 | 5/5 | 5/5 | 5/5 |

## Figuras selecionadas

<table>
<tr>
<td><img src="../../assets/campaign_doc/net_stp_conf_flood/F3_v1_timeseries_http_net_stp_conf_flood_L0_run01.png" alt="Série temporal L0 run01" width="420"><br><sub>Série temporal L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/net_stp_conf_flood/F3_v1_timeseries_http_net_stp_conf_flood_L1_run01.png" alt="Série temporal L1 run01" width="420"><br><sub>Série temporal L1 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/net_stp_conf_flood/F3_v1_timeseries_http_net_stp_conf_flood_L2_run01.png" alt="Série temporal L2 run01" width="420"><br><sub>Série temporal L2 run01</sub></td>
<td><img src="../../assets/campaign_doc/net_stp_conf_flood/F3_v1_timeseries_http_net_stp_conf_flood_L3_run01.png" alt="Série temporal L3 run01" width="420"><br><sub>Série temporal L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/net_stp_conf_flood/F5_resources_http_net_stp_conf_flood_L0_run01.png" alt="Recursos L0 run01" width="420"><br><sub>Recursos L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/net_stp_conf_flood/F5_resources_http_net_stp_conf_flood_L3_run01.png" alt="Recursos L3 run01" width="420"><br><sub>Recursos L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/net_stp_conf_flood/F4_v2_failrate_http_net_stp_conf_flood_L0.png" alt="Taxa de falha L0" width="420"><br><sub>Taxa de falha L0</sub></td>
<td><img src="../../assets/campaign_doc/net_stp_conf_flood/F4_v2_failrate_http_net_stp_conf_flood_L3.png" alt="Taxa de falha L3" width="420"><br><sub>Taxa de falha L3</sub></td>
</tr>
</table>

## Fontes utilizadas

- Catálogo do ataque: `docker/attackers/stp-conf-flood/attack.yaml`
- Artefatos da campanha: `experiments/60att_5runs_l0l1l2l3/net_stp_conf_flood`
