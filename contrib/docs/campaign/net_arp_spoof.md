# ARP Spoof (`net_arp_spoof`)

[Índice da campanha](README.md)

Na campanha `experiments/60att_5runs_l0l1l2l3`, este documento consolida a execução do ataque `net_arp_spoof`. No catálogo local, o ataque é descrito como: Network gateway interception attack through ARP spoofing. A documentação abaixo usa apenas artefatos já presentes no repositório, principalmente as tabelas e figuras de `experiments/60att_5runs_l0l1l2l3/net_arp_spoof`.

## Metadados do ataque

| Campo | Valor |
| --- | --- |
| ID | `net_arp_spoof` |
| Categoria | 2) Network Interception and Exploitation |
| Subcategoria | 2.1 L2/L3 |
| Serviços alvo | local network |
| Imagem | `attack-arp-spoof:latest` |
| Container | `attack-arp-spoof` |
| Runtime máximo do catálogo | 10 s |
| Parâmetros de intensidade | n/d |
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0006/](https://attack.mitre.org/tactics/TA0006/)<br>[https://attack.mitre.org/tactics/TA0009/](https://attack.mitre.org/tactics/TA0009/)<br>[https://attack.mitre.org/techniques/T1557/](https://attack.mitre.org/techniques/T1557/)<br>[https://attack.mitre.org/techniques/T1557/002/](https://attack.mitre.org/techniques/T1557/002/) |

## Resumo estatístico por nível

| Nível | Serviço | Runs | Amostras attack | Sucesso médio | Falha média | Lat p50/p95 ms | PCAP total MB | Dataset médio (min-max) | Exec média s | Extratores ok/total | CPU média/máx | Mem MB média |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | http | 5 | 194 | 100% | 0% | 11,67 / 29,61 | 43,9 | 39.094 (38.436-39.714) | 47,98 | 3/3 | 0,84% / 1,04% | 108,7 |
| L1 | http | 5 | 200 | 100% | 0% | 5,86 / 11,84 | 46,43 | 41.578 (41.340-41.952) | 48,08 | 3/3 | 0,78% / 1% | 110,97 |
| L2 | http | 5 | 200 | 100% | 0% | 5,58 / 8,22 | 45,45 | 40.844 (40.754-41.194) | 48 | 3/3 | 0,84% / 1,04% | 113,1 |
| L3 | http | 5 | 200 | 100% | 0% | 5,53 / 7,83 | 45,94 | 41.214 (41.058-41.446) | 48,09 | 3/3 | 0,81% / 0,98% | 115,17 |

## Estabilidade entre reexecuções

| Nível | Métrica | Runs | Média | Desvio | CV | Min | Max |
| --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | CPU média na fase attack | 5 | 0,84 | 0,07 | 8,15% | 0,77 | 0,95 |
| L0 | Linhas do dataset | 5 | 39.093,6 | 504,09 | 1,29% | 38.436 | 39.714 |
| L0 | Tempo de execução | 5 | 47,98 | 0,33 | 0,68% | 47,75 | 48,55 |
| L0 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L0 | Latência p95 censurada | 5 | 29,61 | 7,9 | 26,66% | 22,42 | 43,07 |
| L1 | CPU média na fase attack | 5 | 0,78 | 0,09 | 12,13% | 0,62 | 0,87 |
| L1 | Linhas do dataset | 5 | 41.578 | 245,35 | 0,59% | 41.340 | 41.952 |
| L1 | Tempo de execução | 5 | 48,08 | 0,1 | 0,21% | 47,96 | 48,16 |
| L1 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L1 | Latência p95 censurada | 5 | 11,84 | 5,13 | 43,33% | 7,56 | 18,9 |
| L2 | CPU média na fase attack | 5 | 0,84 | 0,04 | 4,65% | 0,79 | 0,88 |
| L2 | Linhas do dataset | 5 | 40.844,4 | 195,45 | 0,48% | 40.754 | 41.194 |
| L2 | Tempo de execução | 5 | 48 | 0,04 | 0,09% | 47,93 | 48,05 |
| L2 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L2 | Latência p95 censurada | 5 | 8,22 | 1,04 | 12,64% | 7,15 | 9,67 |
| L3 | CPU média na fase attack | 5 | 0,81 | 0,02 | 2,91% | 0,79 | 0,84 |
| L3 | Linhas do dataset | 5 | 41.213,6 | 141,78 | 0,34% | 41.058 | 41.446 |
| L3 | Tempo de execução | 5 | 48,09 | 0,05 | 0,11% | 48,01 | 48,15 |
| L3 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L3 | Latência p95 censurada | 5 | 7,83 | 0,76 | 9,66% | 6,68 | 8,52 |

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
<td><img src="../../assets/campaign_doc/net_arp_spoof/F3_v1_timeseries_http_net_arp_spoof_L0_run01.png" alt="Série temporal L0 run01" width="420"><br><sub>Série temporal L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/net_arp_spoof/F3_v1_timeseries_http_net_arp_spoof_L1_run01.png" alt="Série temporal L1 run01" width="420"><br><sub>Série temporal L1 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/net_arp_spoof/F3_v1_timeseries_http_net_arp_spoof_L2_run01.png" alt="Série temporal L2 run01" width="420"><br><sub>Série temporal L2 run01</sub></td>
<td><img src="../../assets/campaign_doc/net_arp_spoof/F3_v1_timeseries_http_net_arp_spoof_L3_run01.png" alt="Série temporal L3 run01" width="420"><br><sub>Série temporal L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/net_arp_spoof/F5_resources_http_net_arp_spoof_L0_run01.png" alt="Recursos L0 run01" width="420"><br><sub>Recursos L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/net_arp_spoof/F5_resources_http_net_arp_spoof_L3_run01.png" alt="Recursos L3 run01" width="420"><br><sub>Recursos L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/net_arp_spoof/F4_v2_failrate_http_net_arp_spoof_L0.png" alt="Taxa de falha L0" width="420"><br><sub>Taxa de falha L0</sub></td>
<td><img src="../../assets/campaign_doc/net_arp_spoof/F4_v2_failrate_http_net_arp_spoof_L3.png" alt="Taxa de falha L3" width="420"><br><sub>Taxa de falha L3</sub></td>
</tr>
</table>

## Fontes utilizadas

- Catálogo do ataque: `docker/attackers/arp-spoof/attack.yaml`
- Artefatos da campanha: `experiments/60att_5runs_l0l1l2l3/net_arp_spoof`
