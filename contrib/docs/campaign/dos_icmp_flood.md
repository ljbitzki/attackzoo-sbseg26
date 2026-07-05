# ICMP Flood (`dos_icmp_flood`)

[Índice da campanha](README.md)

Na campanha `experiments/60att_5runs_l0l1l2l3`, este documento consolida a execução do ataque `dos_icmp_flood`. No catálogo local, o ataque é descrito como: ICMP packet flood. A documentação abaixo usa apenas artefatos já presentes no repositório, principalmente as tabelas e figuras de `experiments/60att_5runs_l0l1l2l3/dos_icmp_flood`.

## Metadados do ataque

| Campo | Valor |
| --- | --- |
| ID | `dos_icmp_flood` |
| Categoria | 6) Denial of Service and Impact |
| Subcategoria | 6.1 Network/transport floods (ICMP/TCP/UDP) |
| Serviços alvo | target IP service |
| Imagem | `attack-icmp-flood:latest` |
| Container | `attack-icmp-flood` |
| Runtime máximo do catálogo | 10 s |
| Parâmetros de intensidade | duration_s, count, rate_pps, payload_size |
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0040/](https://attack.mitre.org/tactics/TA0040/)<br>[https://attack.mitre.org/techniques/T1498/](https://attack.mitre.org/techniques/T1498/)<br>[https://attack.mitre.org/techniques/T1498/001/](https://attack.mitre.org/techniques/T1498/001/) |

## Resumo estatístico por nível

| Nível | Serviço | Runs | Amostras attack | Sucesso médio | Falha média | Lat p50/p95 ms | PCAP total MB | Dataset médio (min-max) | Exec média s | Extratores ok/total | CPU média/máx | Mem MB média |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | http | 5 | 200 | 100% | 0% | 4,33 / 5,64 | 5,06 | 9.644 (9.604-9.742) | 43,16 | 3/3 | 0,79% / 0,96% | 240,96 |
| L1 | http | 5 | 198 | 100% | 0% | 4,55 / 6,3 | 26.075,71 | 8.660.581 (7.206.650-9.628.184) | 1.446,12 | 3/3 | 0,72% / 0,9% | 233,44 |
| L2 | http | 5 | 195 | 100% | 0% | 4,75 / 23,36 | 26.213,85 | 8.706.092 (8.219.550-9.305.436) | 1.454,17 | 3/3 | 0,75% / 0,9% | 152,38 |
| L3 | http | 5 | 181 | 100% | 0% | 12,82 / 249,46 | 25.600,02 | 8.501.922 (7.479.238-9.505.306) | 1.405,23 | 3/3 | 0,61% / 0,78% | 79,1 |

## Estabilidade entre reexecuções

| Nível | Métrica | Runs | Média | Desvio | CV | Min | Max |
| --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | CPU média na fase attack | 5 | 0,79 | 0,27 | 33,92% | 0,64 | 1,27 |
| L0 | Linhas do dataset | 5 | 9.643,6 | 56,45 | 0,59% | 9.604 | 9.742 |
| L0 | Tempo de execução | 5 | 43,16 | 0,44 | 1,01% | 42,93 | 43,93 |
| L0 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L0 | Latência p95 censurada | 5 | 5,64 | 0,99 | 17,54% | 4,85 | 7,31 |
| L1 | CPU média na fase attack | 5 | 0,72 | 0,04 | 5,43% | 0,67 | 0,78 |
| L1 | Linhas do dataset | 5 | 8.660.581,2 | 954.194,06 | 11,02% | 7.206.650 | 9.628.184 |
| L1 | Tempo de execução | 5 | 1.446,12 | 157,99 | 10,93% | 1.210,07 | 1.608,74 |
| L1 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L1 | Latência p95 censurada | 5 | 6,3 | 0,66 | 10,5% | 5,66 | 7 |
| L2 | CPU média na fase attack | 5 | 0,75 | 0,08 | 11,31% | 0,63 | 0,87 |
| L2 | Linhas do dataset | 5 | 8.706.092 | 489.785,49 | 5,63% | 8.219.550 | 9.305.436 |
| L2 | Tempo de execução | 5 | 1.454,17 | 78,95 | 5,43% | 1.377,43 | 1.554,02 |
| L2 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L2 | Latência p95 censurada | 5 | 23,36 | 6,4 | 27,42% | 13,12 | 29,52 |
| L3 | CPU média na fase attack | 5 | 0,61 | 0,05 | 7,53% | 0,57 | 0,66 |
| L3 | Linhas do dataset | 5 | 8.501.922 | 786.973,95 | 9,26% | 7.479.238 | 9.505.306 |
| L3 | Tempo de execução | 5 | 1.405,23 | 133,37 | 9,49% | 1.230,82 | 1.576,02 |
| L3 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L3 | Latência p95 censurada | 5 | 249,46 | 194,86 | 78,11% | 20,85 | 510,26 |

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
<td><img src="../../assets/campaign_doc/dos_icmp_flood/F3_v1_timeseries_http_dos_icmp_flood_L0_run01.png" alt="Série temporal L0 run01" width="420"><br><sub>Série temporal L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/dos_icmp_flood/F3_v1_timeseries_http_dos_icmp_flood_L1_run01.png" alt="Série temporal L1 run01" width="420"><br><sub>Série temporal L1 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/dos_icmp_flood/F3_v1_timeseries_http_dos_icmp_flood_L2_run01.png" alt="Série temporal L2 run01" width="420"><br><sub>Série temporal L2 run01</sub></td>
<td><img src="../../assets/campaign_doc/dos_icmp_flood/F3_v1_timeseries_http_dos_icmp_flood_L3_run01.png" alt="Série temporal L3 run01" width="420"><br><sub>Série temporal L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/dos_icmp_flood/F5_resources_http_dos_icmp_flood_L0_run01.png" alt="Recursos L0 run01" width="420"><br><sub>Recursos L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/dos_icmp_flood/F5_resources_http_dos_icmp_flood_L3_run01.png" alt="Recursos L3 run01" width="420"><br><sub>Recursos L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/dos_icmp_flood/F4_v2_failrate_http_dos_icmp_flood_L0.png" alt="Taxa de falha L0" width="420"><br><sub>Taxa de falha L0</sub></td>
<td><img src="../../assets/campaign_doc/dos_icmp_flood/F4_v2_failrate_http_dos_icmp_flood_L3.png" alt="Taxa de falha L3" width="420"><br><sub>Taxa de falha L3</sub></td>
</tr>
</table>

## Fontes utilizadas

- Catálogo do ataque: `docker/attackers/icmp-flood/attack.yaml`
- Artefatos da campanha: `experiments/60att_5runs_l0l1l2l3/dos_icmp_flood`
