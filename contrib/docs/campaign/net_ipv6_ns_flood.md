# IPv6 NS Flood (`net_ipv6_ns_flood`)

[Índice da campanha](README.md)

Na campanha `experiments/60att_5runs_l0l1l2l3`, este documento consolida a execução do ataque `net_ipv6_ns_flood`. No catálogo local, o ataque é descrito como: ICMPv6 Neighbor Solicitation NS (135) flood on the local network. A documentação abaixo usa apenas artefatos já presentes no repositório, principalmente as tabelas e figuras de `experiments/60att_5runs_l0l1l2l3/net_ipv6_ns_flood`.

## Metadados do ataque

| Campo | Valor |
| --- | --- |
| ID | `net_ipv6_ns_flood` |
| Categoria | 2) Network Interception and Exploitation |
| Subcategoria | 2.2 IPv6 |
| Serviços alvo | local IPv6 network |
| Imagem | `attack-ipv6-ns-flood:latest` |
| Container | `attack-ipv6-ns-flood` |
| Runtime máximo do catálogo | 10 s |
| Parâmetros de intensidade | n/d |
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0040/](https://attack.mitre.org/tactics/TA0040/)<br>[https://attack.mitre.org/techniques/T1498/](https://attack.mitre.org/techniques/T1498/)<br>[https://attack.mitre.org/techniques/T1498/001/](https://attack.mitre.org/techniques/T1498/001/) |

## Resumo estatístico por nível

| Nível | Serviço | Runs | Amostras attack | Sucesso médio | Falha média | Lat p50/p95 ms | PCAP total MB | Dataset médio (min-max) | Exec média s | Extratores ok/total | CPU média/máx | Mem MB média |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | http | 5 | 199 | 100% | 0% | 4,68 / 6,31 | 5,19 | 9.920 (9.594-11.182) | 43,6 | 3/3 | 0,74% / 0,91% | 118,14 |
| L1 | http | 5 | 200 | 100% | 0% | 4,44 / 6 | 3.970,47 | 15.410.129 (13.709.440-16.443.054) | 1.562,22 | 3/3 | 0,72% / 0,95% | 123,2 |
| L2 | http | 5 | 199 | 100% | 0% | 4,65 / 6,07 | 4.153,5 | 16.120.792 (15.801.490-16.369.384) | 1.627,37 | 3/3 | 0,7% / 0,87% | 126,02 |
| L3 | http | 5 | 200 | 100% | 0% | 4,28 / 5,98 | 3.909,94 | 15.175.026 (12.540.022-16.408.888) | 1.529,62 | 3/3 | 0,66% / 0,86% | 128,12 |

## Estabilidade entre reexecuções

| Nível | Métrica | Runs | Média | Desvio | CV | Min | Max |
| --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | CPU média na fase attack | 5 | 0,74 | 0,09 | 12,78% | 0,62 | 0,86 |
| L0 | Linhas do dataset | 5 | 9.920 | 705,63 | 7,11% | 9.594 | 11.182 |
| L0 | Tempo de execução | 5 | 43,6 | 1,29 | 2,96% | 42,91 | 45,91 |
| L0 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L0 | Latência p95 censurada | 5 | 6,31 | 1,2 | 19,1% | 4,89 | 7,71 |
| L1 | CPU média na fase attack | 5 | 0,72 | 0,07 | 9,81% | 0,62 | 0,8 |
| L1 | Linhas do dataset | 5 | 15.410.128,8 | 1.015.598,34 | 6,59% | 13.709.440 | 16.443.054 |
| L1 | Tempo de execução | 5 | 1.562,22 | 98,67 | 6,32% | 1.398,26 | 1.664,52 |
| L1 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L1 | Latência p95 censurada | 5 | 6 | 0,79 | 13,22% | 5,26 | 7,22 |
| L2 | CPU média na fase attack | 5 | 0,7 | 0,09 | 12,4% | 0,6 | 0,78 |
| L2 | Linhas do dataset | 5 | 16.120.792 | 220.354,08 | 1,37% | 15.801.490 | 16.369.384 |
| L2 | Tempo de execução | 5 | 1.627,37 | 24 | 1,47% | 1.591,54 | 1.652,76 |
| L2 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L2 | Latência p95 censurada | 5 | 6,07 | 1,18 | 19,52% | 4,65 | 7,4 |
| L3 | CPU média na fase attack | 5 | 0,66 | 0,06 | 8,79% | 0,6 | 0,74 |
| L3 | Linhas do dataset | 5 | 15.175.026 | 1.532.495,18 | 10,1% | 12.540.022 | 16.408.888 |
| L3 | Tempo de execução | 5 | 1.529,62 | 146,01 | 9,55% | 1.277,3 | 1.640,92 |
| L3 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L3 | Latência p95 censurada | 5 | 5,98 | 0,97 | 16,16% | 4,89 | 7,13 |

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
<td><img src="../../assets/campaign_doc/net_ipv6_ns_flood/F3_v1_timeseries_http_net_ipv6_ns_flood_L0_run01.png" alt="Série temporal L0 run01" width="420"><br><sub>Série temporal L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/net_ipv6_ns_flood/F3_v1_timeseries_http_net_ipv6_ns_flood_L1_run01.png" alt="Série temporal L1 run01" width="420"><br><sub>Série temporal L1 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/net_ipv6_ns_flood/F3_v1_timeseries_http_net_ipv6_ns_flood_L2_run01.png" alt="Série temporal L2 run01" width="420"><br><sub>Série temporal L2 run01</sub></td>
<td><img src="../../assets/campaign_doc/net_ipv6_ns_flood/F3_v1_timeseries_http_net_ipv6_ns_flood_L3_run01.png" alt="Série temporal L3 run01" width="420"><br><sub>Série temporal L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/net_ipv6_ns_flood/F5_resources_http_net_ipv6_ns_flood_L0_run01.png" alt="Recursos L0 run01" width="420"><br><sub>Recursos L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/net_ipv6_ns_flood/F5_resources_http_net_ipv6_ns_flood_L3_run01.png" alt="Recursos L3 run01" width="420"><br><sub>Recursos L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/net_ipv6_ns_flood/F4_v2_failrate_http_net_ipv6_ns_flood_L0.png" alt="Taxa de falha L0" width="420"><br><sub>Taxa de falha L0</sub></td>
<td><img src="../../assets/campaign_doc/net_ipv6_ns_flood/F4_v2_failrate_http_net_ipv6_ns_flood_L3.png" alt="Taxa de falha L3" width="420"><br><sub>Taxa de falha L3</sub></td>
</tr>
</table>

## Fontes utilizadas

- Catálogo do ataque: `docker/attackers/ipv6-ns-flood/attack.yaml`
- Artefatos da campanha: `experiments/60att_5runs_l0l1l2l3/net_ipv6_ns_flood`
