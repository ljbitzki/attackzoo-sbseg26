# RST Flood (`dos_rst_flood`)

[Índice da campanha](README.md)

Na campanha `experiments/60att_5runs_l0l1l2l3`, este documento consolida a execução do ataque `dos_rst_flood`. No catálogo local, o ataque é descrito como: TCP packet flood with the RST flag set. A documentação abaixo usa apenas artefatos já presentes no repositório, principalmente as tabelas e figuras de `experiments/60att_5runs_l0l1l2l3/dos_rst_flood`.

## Metadados do ataque

| Campo | Valor |
| --- | --- |
| ID | `dos_rst_flood` |
| Categoria | 6) Denial of Service and Impact |
| Subcategoria | 6.1 Network/transport floods (ICMP/TCP/UDP) |
| Serviços alvo | target IP service |
| Imagem | `attack-rst-flood:latest` |
| Container | `attack-rst-flood` |
| Runtime máximo do catálogo | 10 s |
| Parâmetros de intensidade | duration_s, count, rate_pps, payload_size |
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0040/](https://attack.mitre.org/tactics/TA0040/)<br>[https://attack.mitre.org/techniques/T1498/](https://attack.mitre.org/techniques/T1498/)<br>[https://attack.mitre.org/techniques/T1498/001/](https://attack.mitre.org/techniques/T1498/001/) |

## Resumo estatístico por nível

| Nível | Serviço | Runs | Amostras attack | Sucesso médio | Falha média | Lat p50/p95 ms | PCAP total MB | Dataset médio (min-max) | Exec média s | Extratores ok/total | CPU média/máx | Mem MB média |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | http | 5 | 199 | 100% | 0% | 4,07 / 20,47 | 1,66 | 3.136 (3.120-3.162) | 42,37 | 3/3 | 0,61% / 0,7% | 79,84 |
| L1 | http | 5 | 199 | 100% | 0% | 4,52 / 15,8 | 860,41 | 4.742.488 (4.561.396-4.850.748) | 598,24 | 3/3 | 0,71% / 0,93% | 81,94 |
| L2 | http | 5 | 196 | 100% | 0% | 4,37 / 40,5 | 837,06 | 4.613.701 (3.977.122-4.903.038) | 580,78 | 3/3 | 0,7% / 1,16% | 86,26 |
| L3 | http | 5 | 200 | 100% | 0% | 4 / 8,76 | 838,25 | 4.620.094 (3.875.808-4.913.302) | 581,89 | 3/3 | 0,61% / 0,75% | 101,84 |

## Estabilidade entre reexecuções

| Nível | Métrica | Runs | Média | Desvio | CV | Min | Max |
| --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | CPU média na fase attack | 5 | 0,61 | 0,04 | 7,26% | 0,53 | 0,64 |
| L0 | Linhas do dataset | 5 | 3.136,4 | 22,47 | 0,72% | 3.120 | 3.162 |
| L0 | Tempo de execução | 5 | 42,37 | 0,63 | 1,48% | 42,03 | 43,47 |
| L0 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L0 | Latência p95 censurada | 5 | 20,47 | 2,45 | 11,97% | 18,19 | 24,03 |
| L1 | CPU média na fase attack | 5 | 0,71 | 0,09 | 12,1% | 0,58 | 0,8 |
| L1 | Linhas do dataset | 5 | 4.742.487,6 | 109.806,47 | 2,32% | 4.561.396 | 4.850.748 |
| L1 | Tempo de execução | 5 | 598,24 | 12,35 | 2,06% | 577,61 | 609,4 |
| L1 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L1 | Latência p95 censurada | 5 | 15,8 | 6,61 | 41,85% | 4,83 | 20,48 |
| L2 | CPU média na fase attack | 5 | 0,7 | 0,1 | 14,9% | 0,63 | 0,88 |
| L2 | Linhas do dataset | 5 | 4.613.701,2 | 364.149,29 | 7,89% | 3.977.122 | 4.903.038 |
| L2 | Tempo de execução | 5 | 580,78 | 42,07 | 7,24% | 507,25 | 614,26 |
| L2 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L2 | Latência p95 censurada | 5 | 40,5 | 47,15 | 116,43% | 14,46 | 124,67 |
| L3 | CPU média na fase attack | 5 | 0,61 | 0,06 | 9,26% | 0,53 | 0,67 |
| L3 | Linhas do dataset | 5 | 4.620.093,6 | 420.807,39 | 9,11% | 3.875.808 | 4.913.302 |
| L3 | Tempo de execução | 5 | 581,89 | 49,38 | 8,49% | 494,41 | 614,74 |
| L3 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L3 | Latência p95 censurada | 5 | 8,76 | 5,35 | 61,05% | 4,36 | 16,09 |

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
<td><img src="../../assets/campaign_doc/dos_rst_flood/F3_v1_timeseries_http_dos_rst_flood_L0_run01.png" alt="Série temporal L0 run01" width="420"><br><sub>Série temporal L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/dos_rst_flood/F3_v1_timeseries_http_dos_rst_flood_L1_run01.png" alt="Série temporal L1 run01" width="420"><br><sub>Série temporal L1 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/dos_rst_flood/F3_v1_timeseries_http_dos_rst_flood_L2_run01.png" alt="Série temporal L2 run01" width="420"><br><sub>Série temporal L2 run01</sub></td>
<td><img src="../../assets/campaign_doc/dos_rst_flood/F3_v1_timeseries_http_dos_rst_flood_L3_run01.png" alt="Série temporal L3 run01" width="420"><br><sub>Série temporal L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/dos_rst_flood/F5_resources_http_dos_rst_flood_L0_run01.png" alt="Recursos L0 run01" width="420"><br><sub>Recursos L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/dos_rst_flood/F5_resources_http_dos_rst_flood_L3_run01.png" alt="Recursos L3 run01" width="420"><br><sub>Recursos L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/dos_rst_flood/F4_v2_failrate_http_dos_rst_flood_L0.png" alt="Taxa de falha L0" width="420"><br><sub>Taxa de falha L0</sub></td>
<td><img src="../../assets/campaign_doc/dos_rst_flood/F4_v2_failrate_http_dos_rst_flood_L3.png" alt="Taxa de falha L3" width="420"><br><sub>Taxa de falha L3</sub></td>
</tr>
</table>

## Fontes utilizadas

- Catálogo do ataque: `docker/attackers/rst-flood/attack.yaml`
- Artefatos da campanha: `experiments/60att_5runs_l0l1l2l3/dos_rst_flood`
