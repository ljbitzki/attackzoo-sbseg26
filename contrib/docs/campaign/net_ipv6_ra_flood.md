# IPv6 RA Flood (`net_ipv6_ra_flood`)

[Índice da campanha](README.md)

Na campanha `experiments/60att_5runs_l0l1l2l3`, este documento consolida a execução do ataque `net_ipv6_ra_flood`. No catálogo local, o ataque é descrito como: ICMPv6 Router Advertisement RA (134) flood on the local network. A documentação abaixo usa apenas artefatos já presentes no repositório, principalmente as tabelas e figuras de `experiments/60att_5runs_l0l1l2l3/net_ipv6_ra_flood`.

## Metadados do ataque

| Campo | Valor |
| --- | --- |
| ID | `net_ipv6_ra_flood` |
| Categoria | 2) Network Interception and Exploitation |
| Subcategoria | 2.2 IPv6 |
| Serviços alvo | local IPv6 network |
| Imagem | `attack-ipv6-ra-flood:latest` |
| Container | `attack-ipv6-ra-flood` |
| Runtime máximo do catálogo | 10 s |
| Parâmetros de intensidade | n/d |
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0006/](https://attack.mitre.org/tactics/TA0006/)<br>[https://attack.mitre.org/tactics/TA0009/](https://attack.mitre.org/tactics/TA0009/)<br>[https://attack.mitre.org/tactics/TA0040/](https://attack.mitre.org/tactics/TA0040/)<br>[https://attack.mitre.org/techniques/T1557/](https://attack.mitre.org/techniques/T1557/)<br>[https://attack.mitre.org/techniques/T1498/](https://attack.mitre.org/techniques/T1498/)<br>[https://attack.mitre.org/techniques/T1498/001/](https://attack.mitre.org/techniques/T1498/001/) |

## Resumo estatístico por nível

| Nível | Serviço | Runs | Amostras attack | Sucesso médio | Falha média | Lat p50/p95 ms | PCAP total MB | Dataset médio (min-max) | Exec média s | Extratores ok/total | CPU média/máx | Mem MB média |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | http | 5 | 200 | 100% | 0% | 4,2 / 4,97 | 5,05 | 9.601 (9.590-9.612) | 43,27 | 3/3 | 0,65% / 0,83% | 130,23 |
| L1 | http | 5 | 191 | 98,9% | 1,1% | 4,42 / 5,61 | 2.239,1 | 6.703.052 (5.264.982-7.208.904) | 964,9 | 3/3 | 0,65% / 0,79% | 133,08 |
| L2 | http | 5 | 200 | 100% | 0% | 4,17 / 5,49 | 2.075,81 | 6.213.737 (5.235.654-7.229.628) | 901,23 | 3/3 | 0,64% / 0,75% | 136,15 |
| L3 | http | 5 | 195 | 99,4% | 0,6% | 4,65 / 6,42 | 2.225,05 | 6.660.712 (5.878.524-7.124.444) | 962,3 | 3/3 | 0,7% / 0,88% | 138,2 |

## Estabilidade entre reexecuções

| Nível | Métrica | Runs | Média | Desvio | CV | Min | Max |
| --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | CPU média na fase attack | 5 | 0,65 | 0,07 | 10,28% | 0,6 | 0,76 |
| L0 | Linhas do dataset | 5 | 9.600,8 | 10,06 | 0,1% | 9.590 | 9.612 |
| L0 | Tempo de execução | 5 | 43,27 | 0,89 | 2,06% | 42,77 | 44,86 |
| L0 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L0 | Latência p95 censurada | 5 | 4,97 | 0,61 | 12,33% | 4,28 | 5,94 |
| L1 | CPU média na fase attack | 5 | 0,65 | 0,06 | 9,01% | 0,62 | 0,76 |
| L1 | Linhas do dataset | 5 | 6.703.051,6 | 814.069,02 | 12,14% | 5.264.982 | 7.208.904 |
| L1 | Tempo de execução | 5 | 964,9 | 110,58 | 11,46% | 768,77 | 1.029,91 |
| L1 | Falha na fase attack | 5 | 1,14 | 1,57 | 138,04% | 0 | 3,12 |
| L1 | Latência p95 censurada | 5 | 5,61 | 0,96 | 17,18% | 4,71 | 6,88 |
| L2 | CPU média na fase attack | 5 | 0,64 | 0,04 | 5,73% | 0,58 | 0,68 |
| L2 | Linhas do dataset | 5 | 6.213.736,8 | 925.420,2 | 14,89% | 5.235.654 | 7.229.628 |
| L2 | Tempo de execução | 5 | 901,23 | 128,99 | 14,31% | 764,94 | 1.040,79 |
| L2 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L2 | Latência p95 censurada | 5 | 5,49 | 0,78 | 14,13% | 4,61 | 6,64 |
| L3 | CPU média na fase attack | 5 | 0,7 | 0,1 | 14,03% | 0,56 | 0,8 |
| L3 | Linhas do dataset | 5 | 6.660.711,6 | 508.458,95 | 7,63% | 5.878.524 | 7.124.444 |
| L3 | Tempo de execução | 5 | 962,3 | 71,12 | 7,39% | 852,35 | 1.026,51 |
| L3 | Falha na fase attack | 5 | 0,57 | 1,28 | 223,61% | 0 | 2,86 |
| L3 | Latência p95 censurada | 5 | 6,42 | 1,01 | 15,74% | 5,07 | 7,59 |

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
<td><img src="../../assets/campaign_doc/net_ipv6_ra_flood/F3_v1_timeseries_http_net_ipv6_ra_flood_L0_run01.png" alt="Série temporal L0 run01" width="420"><br><sub>Série temporal L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/net_ipv6_ra_flood/F3_v1_timeseries_http_net_ipv6_ra_flood_L1_run01.png" alt="Série temporal L1 run01" width="420"><br><sub>Série temporal L1 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/net_ipv6_ra_flood/F3_v1_timeseries_http_net_ipv6_ra_flood_L2_run01.png" alt="Série temporal L2 run01" width="420"><br><sub>Série temporal L2 run01</sub></td>
<td><img src="../../assets/campaign_doc/net_ipv6_ra_flood/F3_v1_timeseries_http_net_ipv6_ra_flood_L3_run01.png" alt="Série temporal L3 run01" width="420"><br><sub>Série temporal L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/net_ipv6_ra_flood/F5_resources_http_net_ipv6_ra_flood_L0_run01.png" alt="Recursos L0 run01" width="420"><br><sub>Recursos L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/net_ipv6_ra_flood/F5_resources_http_net_ipv6_ra_flood_L3_run01.png" alt="Recursos L3 run01" width="420"><br><sub>Recursos L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/net_ipv6_ra_flood/F4_v2_failrate_http_net_ipv6_ra_flood_L0.png" alt="Taxa de falha L0" width="420"><br><sub>Taxa de falha L0</sub></td>
<td><img src="../../assets/campaign_doc/net_ipv6_ra_flood/F4_v2_failrate_http_net_ipv6_ra_flood_L3.png" alt="Taxa de falha L3" width="420"><br><sub>Taxa de falha L3</sub></td>
</tr>
</table>

## Fontes utilizadas

- Catálogo do ataque: `docker/attackers/ipv6-ra-flood/attack.yaml`
- Artefatos da campanha: `experiments/60att_5runs_l0l1l2l3/net_ipv6_ra_flood`
