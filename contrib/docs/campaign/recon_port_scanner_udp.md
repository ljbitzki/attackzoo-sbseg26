# Port Scanner UDP (`recon_port_scanner_udp`)

[Índice da campanha](README.md)

Na campanha `experiments/60att_5runs_l0l1l2l3`, este documento consolida a execução do ataque `recon_port_scanner_udp`. No catálogo local, o ataque é descrito como: UDP port scan of the target. A documentação abaixo usa apenas artefatos já presentes no repositório, principalmente as tabelas e figuras de `experiments/60att_5runs_l0l1l2l3/recon_port_scanner_udp`.

## Metadados do ataque

| Campo | Valor |
| --- | --- |
| ID | `recon_port_scanner_udp` |
| Categoria | 1) Reconnaissance and Discovery |
| Subcategoria | 1.2 Port, service, OS, and vulnerability scanning |
| Serviços alvo | target IP service |
| Imagem | `attack-port-scanner-udp:latest` |
| Container | `attack-port-scanner-udp` |
| Runtime máximo do catálogo | 300 s |
| Parâmetros de intensidade | n/d |
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0043/](https://attack.mitre.org/tactics/TA0043/)<br>[https://attack.mitre.org/tactics/TA0007/](https://attack.mitre.org/tactics/TA0007/)<br>[https://attack.mitre.org/techniques/T1590/](https://attack.mitre.org/techniques/T1590/)<br>[https://attack.mitre.org/techniques/T1595/](https://attack.mitre.org/techniques/T1595/)<br>[https://attack.mitre.org/techniques/T1595/001/](https://attack.mitre.org/techniques/T1595/001/)<br>[https://attack.mitre.org/techniques/T1046/](https://attack.mitre.org/techniques/T1046/) |

## Resumo estatístico por nível

| Nível | Serviço | Runs | Amostras attack | Sucesso médio | Falha média | Lat p50/p95 ms | PCAP total MB | Dataset médio (min-max) | Exec média s | Extratores ok/total | CPU média/máx | Mem MB média |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | http | 5 | 200 | 100% | 0% | 5,06 / 6,59 | 5,05 | 9.606 (9.540-9.716) | 43,16 | 3/3 | 0,78% / 0,94% | 748,35 |
| L1 | http | 5 | 200 | 100% | 0% | 4,17 / 4,97 | 5,26 | 10.673 (10.378-11.112) | 43,11 | 3/3 | 0,65% / 0,73% | 750,34 |
| L2 | http | 5 | 200 | 100% | 0% | 5,08 / 6,54 | 5,23 | 10.525 (10.360-11.038) | 43,23 | 3/3 | 0,78% / 0,87% | 752,4 |
| L3 | http | 5 | 200 | 100% | 0% | 5,14 / 6,4 | 5,22 | 10.494 (10.370-10.954) | 43,15 | 3/3 | 0,81% / 0,94% | 754,68 |

## Estabilidade entre reexecuções

| Nível | Métrica | Runs | Média | Desvio | CV | Min | Max |
| --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | CPU média na fase attack | 5 | 0,78 | 0,11 | 13,88% | 0,67 | 0,96 |
| L0 | Linhas do dataset | 5 | 9.605,6 | 66,73 | 0,69% | 9.540 | 9.716 |
| L0 | Tempo de execução | 5 | 43,16 | 0,37 | 0,86% | 42,95 | 43,82 |
| L0 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L0 | Latência p95 censurada | 5 | 6,59 | 1,02 | 15,45% | 5,53 | 8,06 |
| L1 | CPU média na fase attack | 5 | 0,65 | 0,04 | 5,8% | 0,61 | 0,71 |
| L1 | Linhas do dataset | 5 | 10.672,8 | 379,57 | 3,56% | 10.378 | 11.112 |
| L1 | Tempo de execução | 5 | 43,11 | 0,14 | 0,33% | 42,96 | 43,26 |
| L1 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L1 | Latência p95 censurada | 5 | 4,97 | 0,65 | 13,1% | 4,46 | 6,06 |
| L2 | CPU média na fase attack | 5 | 0,78 | 0,03 | 3,88% | 0,73 | 0,8 |
| L2 | Linhas do dataset | 5 | 10.525,2 | 290,88 | 2,76% | 10.360 | 11.038 |
| L2 | Tempo de execução | 5 | 43,23 | 0,1 | 0,22% | 43,11 | 43,38 |
| L2 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L2 | Latência p95 censurada | 5 | 6,54 | 0,19 | 2,88% | 6,27 | 6,75 |
| L3 | CPU média na fase attack | 5 | 0,81 | 0,11 | 13,99% | 0,66 | 0,94 |
| L3 | Linhas do dataset | 5 | 10.494,4 | 257,06 | 2,45% | 10.370 | 10.954 |
| L3 | Tempo de execução | 5 | 43,15 | 0,1 | 0,22% | 43,03 | 43,26 |
| L3 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L3 | Latência p95 censurada | 5 | 6,4 | 1,21 | 18,88% | 4,73 | 7,89 |

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
<td><img src="../../assets/campaign_doc/recon_port_scanner_udp/F3_v1_timeseries_http_recon_port_scanner_udp_L0_run01.png" alt="Série temporal L0 run01" width="420"><br><sub>Série temporal L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/recon_port_scanner_udp/F3_v1_timeseries_http_recon_port_scanner_udp_L1_run01.png" alt="Série temporal L1 run01" width="420"><br><sub>Série temporal L1 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/recon_port_scanner_udp/F3_v1_timeseries_http_recon_port_scanner_udp_L2_run01.png" alt="Série temporal L2 run01" width="420"><br><sub>Série temporal L2 run01</sub></td>
<td><img src="../../assets/campaign_doc/recon_port_scanner_udp/F3_v1_timeseries_http_recon_port_scanner_udp_L3_run01.png" alt="Série temporal L3 run01" width="420"><br><sub>Série temporal L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/recon_port_scanner_udp/F5_resources_http_recon_port_scanner_udp_L0_run01.png" alt="Recursos L0 run01" width="420"><br><sub>Recursos L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/recon_port_scanner_udp/F5_resources_http_recon_port_scanner_udp_L3_run01.png" alt="Recursos L3 run01" width="420"><br><sub>Recursos L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/recon_port_scanner_udp/F4_v2_failrate_http_recon_port_scanner_udp_L0.png" alt="Taxa de falha L0" width="420"><br><sub>Taxa de falha L0</sub></td>
<td><img src="../../assets/campaign_doc/recon_port_scanner_udp/F4_v2_failrate_http_recon_port_scanner_udp_L3.png" alt="Taxa de falha L3" width="420"><br><sub>Taxa de falha L3</sub></td>
</tr>
</table>

## Fontes utilizadas

- Catálogo do ataque: `docker/attackers/port-scanner-udp/attack.yaml`
- Artefatos da campanha: `experiments/60att_5runs_l0l1l2l3/recon_port_scanner_udp`
