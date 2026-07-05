# Port Scanner OS (`recon_port_scanner_os`)

[Índice da campanha](README.md)

Na campanha `experiments/60att_5runs_l0l1l2l3`, este documento consolida a execução do ataque `recon_port_scanner_os`. No catálogo local, o ataque é descrito como: Target operating system detection (fingerprinting). A documentação abaixo usa apenas artefatos já presentes no repositório, principalmente as tabelas e figuras de `experiments/60att_5runs_l0l1l2l3/recon_port_scanner_os`.

## Metadados do ataque

| Campo | Valor |
| --- | --- |
| ID | `recon_port_scanner_os` |
| Categoria | 1) Reconnaissance and Discovery |
| Subcategoria | 1.2 Port, service, OS, and vulnerability scanning |
| Serviços alvo | target IP service |
| Imagem | `attack-port-scanner-os:latest` |
| Container | `attack-port-scanner-os` |
| Runtime máximo do catálogo | 120 s |
| Parâmetros de intensidade | n/d |
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0043/](https://attack.mitre.org/tactics/TA0043/)<br>[https://attack.mitre.org/tactics/TA0007/](https://attack.mitre.org/tactics/TA0007/)<br>[https://attack.mitre.org/techniques/T1592/](https://attack.mitre.org/techniques/T1592/)<br>[https://attack.mitre.org/techniques/T1595/](https://attack.mitre.org/techniques/T1595/)<br>[https://attack.mitre.org/techniques/T1595/001/](https://attack.mitre.org/techniques/T1595/001/)<br>[https://attack.mitre.org/techniques/T1046/](https://attack.mitre.org/techniques/T1046/) |

## Resumo estatístico por nível

| Nível | Serviço | Runs | Amostras attack | Sucesso médio | Falha média | Lat p50/p95 ms | PCAP total MB | Dataset médio (min-max) | Exec média s | Extratores ok/total | CPU média/máx | Mem MB média |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | http | 5 | 200 | 100% | 0% | 4,34 / 5,4 | 5,06 | 9.620 (9.590-9.706) | 43,12 | 3/3 | 0,7% / 0,81% | 728,41 |
| L1 | http | 5 | 200 | 100% | 0% | 4,52 / 6 | 7,15 | 19.381 (19.292-19.434) | 44,12 | 3/3 | 0,75% / 1,09% | 730,81 |
| L2 | http | 5 | 200 | 100% | 0% | 4,36 / 5,16 | 7,16 | 19.401 (19.330-19.426) | 44,13 | 3/3 | 0,68% / 0,8% | 733,43 |
| L3 | http | 5 | 200 | 100% | 0% | 5,27 / 6,72 | 7,16 | 19.399 (19.310-19.430) | 44,18 | 3/3 | 0,84% / 1,05% | 737,59 |

## Estabilidade entre reexecuções

| Nível | Métrica | Runs | Média | Desvio | CV | Min | Max |
| --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | CPU média na fase attack | 5 | 0,7 | 0,04 | 6,15% | 0,65 | 0,77 |
| L0 | Linhas do dataset | 5 | 9.619,6 | 48,53 | 0,5% | 9.590 | 9.706 |
| L0 | Tempo de execução | 5 | 43,12 | 0,43 | 1% | 42,87 | 43,89 |
| L0 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L0 | Latência p95 censurada | 5 | 5,4 | 0,75 | 13,89% | 4,77 | 6,3 |
| L1 | CPU média na fase attack | 5 | 0,75 | 0,08 | 10,17% | 0,68 | 0,88 |
| L1 | Linhas do dataset | 5 | 19.381,2 | 64,2 | 0,33% | 19.292 | 19.434 |
| L1 | Tempo de execução | 5 | 44,12 | 0,03 | 0,07% | 44,1 | 44,17 |
| L1 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L1 | Latência p95 censurada | 5 | 6 | 1,2 | 20,01% | 4,9 | 8 |
| L2 | CPU média na fase attack | 5 | 0,68 | 0,04 | 5,18% | 0,65 | 0,74 |
| L2 | Linhas do dataset | 5 | 19.401,2 | 40,16 | 0,21% | 19.330 | 19.426 |
| L2 | Tempo de execução | 5 | 44,13 | 0,09 | 0,2% | 43,99 | 44,22 |
| L2 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L2 | Latência p95 censurada | 5 | 5,16 | 0,63 | 12,23% | 4,55 | 6,01 |
| L3 | CPU média na fase attack | 5 | 0,84 | 0,11 | 13,3% | 0,71 | 0,97 |
| L3 | Linhas do dataset | 5 | 19.398,8 | 49,93 | 0,26% | 19.310 | 19.430 |
| L3 | Tempo de execução | 5 | 44,18 | 0,08 | 0,18% | 44,09 | 44,29 |
| L3 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L3 | Latência p95 censurada | 5 | 6,72 | 0,96 | 14,34% | 5,29 | 7,61 |

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
<td><img src="../../assets/campaign_doc/recon_port_scanner_os/F3_v1_timeseries_http_recon_port_scanner_os_L0_run01.png" alt="Série temporal L0 run01" width="420"><br><sub>Série temporal L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/recon_port_scanner_os/F3_v1_timeseries_http_recon_port_scanner_os_L1_run01.png" alt="Série temporal L1 run01" width="420"><br><sub>Série temporal L1 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/recon_port_scanner_os/F3_v1_timeseries_http_recon_port_scanner_os_L2_run01.png" alt="Série temporal L2 run01" width="420"><br><sub>Série temporal L2 run01</sub></td>
<td><img src="../../assets/campaign_doc/recon_port_scanner_os/F3_v1_timeseries_http_recon_port_scanner_os_L3_run01.png" alt="Série temporal L3 run01" width="420"><br><sub>Série temporal L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/recon_port_scanner_os/F5_resources_http_recon_port_scanner_os_L0_run01.png" alt="Recursos L0 run01" width="420"><br><sub>Recursos L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/recon_port_scanner_os/F5_resources_http_recon_port_scanner_os_L3_run01.png" alt="Recursos L3 run01" width="420"><br><sub>Recursos L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/recon_port_scanner_os/F4_v2_failrate_http_recon_port_scanner_os_L0.png" alt="Taxa de falha L0" width="420"><br><sub>Taxa de falha L0</sub></td>
<td><img src="../../assets/campaign_doc/recon_port_scanner_os/F4_v2_failrate_http_recon_port_scanner_os_L3.png" alt="Taxa de falha L3" width="420"><br><sub>Taxa de falha L3</sub></td>
</tr>
</table>

## Fontes utilizadas

- Catálogo do ataque: `docker/attackers/port-scanner-os/attack.yaml`
- Artefatos da campanha: `experiments/60att_5runs_l0l1l2l3/recon_port_scanner_os`
