# ARP Scan (`recon_arp_scan`)

[Índice da campanha](README.md)

Na campanha `experiments/60att_5runs_l0l1l2l3`, este documento consolida a execução do ataque `recon_arp_scan`. No catálogo local, o ataque é descrito como: Host enumeration through ARP on the target network. A documentação abaixo usa apenas artefatos já presentes no repositório, principalmente as tabelas e figuras de `experiments/60att_5runs_l0l1l2l3/recon_arp_scan`.

## Metadados do ataque

| Campo | Valor |
| --- | --- |
| ID | `recon_arp_scan` |
| Categoria | 1) Reconnaissance and Discovery |
| Subcategoria | 1.1 Network-level host discovery |
| Serviços alvo | local network |
| Imagem | `attack-arp-scan:latest` |
| Container | `attack-arp-scan` |
| Runtime máximo do catálogo | 10 s |
| Parâmetros de intensidade | n/d |
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0043/](https://attack.mitre.org/tactics/TA0043/)<br>[https://attack.mitre.org/tactics/TA0007/](https://attack.mitre.org/tactics/TA0007/)<br>[https://attack.mitre.org/techniques/T1590/](https://attack.mitre.org/techniques/T1590/)<br>[https://attack.mitre.org/techniques/T1595/](https://attack.mitre.org/techniques/T1595/)<br>[https://attack.mitre.org/techniques/T1595/001/](https://attack.mitre.org/techniques/T1595/001/)<br>[https://attack.mitre.org/techniques/T1018/](https://attack.mitre.org/techniques/T1018/) |

## Resumo estatístico por nível

| Nível | Serviço | Runs | Amostras attack | Sucesso médio | Falha média | Lat p50/p95 ms | PCAP total MB | Dataset médio (min-max) | Exec média s | Extratores ok/total | CPU média/máx | Mem MB média |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | http | 5 | 200 | 100% | 0% | 4,36 / 5,63 | 5,06 | 9.620 (9.590-9.718) | 43,13 | 3/3 | 0,73% / 0,89% | 701,9 |
| L1 | http | 5 | 200 | 100% | 0% | 4,36 / 5,54 | 40,04 | 238.923 (234.084-243.542) | 60,85 | 3/3 | 0,67% / 0,78% | 703,89 |
| L2 | http | 5 | 200 | 100% | 0% | 4,38 / 5,82 | 40,73 | 243.436 (242.890-243.946) | 61,15 | 3/3 | 0,71% / 0,89% | 706,09 |
| L3 | http | 5 | 200 | 100% | 0% | 5,16 / 6,94 | 40,72 | 243.358 (242.742-243.654) | 61,15 | 3/3 | 0,79% / 0,96% | 708,21 |

## Estabilidade entre reexecuções

| Nível | Métrica | Runs | Média | Desvio | CV | Min | Max |
| --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | CPU média na fase attack | 5 | 0,73 | 0,08 | 11,2% | 0,62 | 0,85 |
| L0 | Linhas do dataset | 5 | 9.620,4 | 54,89 | 0,57% | 9.590 | 9.718 |
| L0 | Tempo de execução | 5 | 43,13 | 0,33 | 0,77% | 42,87 | 43,69 |
| L0 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L0 | Latência p95 censurada | 5 | 5,63 | 0,9 | 15,91% | 4,46 | 6,53 |
| L1 | CPU média na fase attack | 5 | 0,67 | 0,04 | 6,16% | 0,63 | 0,73 |
| L1 | Linhas do dataset | 5 | 238.922,8 | 4.484,55 | 1,88% | 234.084 | 243.542 |
| L1 | Tempo de execução | 5 | 60,85 | 0,29 | 0,47% | 60,4 | 61,18 |
| L1 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L1 | Latência p95 censurada | 5 | 5,54 | 1,19 | 21,38% | 4,58 | 7,58 |
| L2 | CPU média na fase attack | 5 | 0,71 | 0,07 | 9,96% | 0,6 | 0,79 |
| L2 | Linhas do dataset | 5 | 243.436,4 | 404,42 | 0,17% | 242.890 | 243.946 |
| L2 | Tempo de execução | 5 | 61,15 | 0,19 | 0,31% | 60,93 | 61,35 |
| L2 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L2 | Latência p95 censurada | 5 | 5,82 | 0,86 | 14,74% | 4,42 | 6,52 |
| L3 | CPU média na fase attack | 5 | 0,79 | 0,06 | 7,79% | 0,7 | 0,86 |
| L3 | Linhas do dataset | 5 | 243.358 | 364,9 | 0,15% | 242.742 | 243.654 |
| L3 | Tempo de execução | 5 | 61,15 | 0,14 | 0,23% | 60,93 | 61,31 |
| L3 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L3 | Latência p95 censurada | 5 | 6,94 | 0,8 | 11,58% | 5,94 | 8 |

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
<td><img src="../../assets/campaign_doc/recon_arp_scan/F3_v1_timeseries_http_recon_arp_scan_L0_run01.png" alt="Série temporal L0 run01" width="420"><br><sub>Série temporal L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/recon_arp_scan/F3_v1_timeseries_http_recon_arp_scan_L1_run01.png" alt="Série temporal L1 run01" width="420"><br><sub>Série temporal L1 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/recon_arp_scan/F3_v1_timeseries_http_recon_arp_scan_L2_run01.png" alt="Série temporal L2 run01" width="420"><br><sub>Série temporal L2 run01</sub></td>
<td><img src="../../assets/campaign_doc/recon_arp_scan/F3_v1_timeseries_http_recon_arp_scan_L3_run01.png" alt="Série temporal L3 run01" width="420"><br><sub>Série temporal L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/recon_arp_scan/F5_resources_http_recon_arp_scan_L0_run01.png" alt="Recursos L0 run01" width="420"><br><sub>Recursos L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/recon_arp_scan/F5_resources_http_recon_arp_scan_L3_run01.png" alt="Recursos L3 run01" width="420"><br><sub>Recursos L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/recon_arp_scan/F4_v2_failrate_http_recon_arp_scan_L0.png" alt="Taxa de falha L0" width="420"><br><sub>Taxa de falha L0</sub></td>
<td><img src="../../assets/campaign_doc/recon_arp_scan/F4_v2_failrate_http_recon_arp_scan_L3.png" alt="Taxa de falha L3" width="420"><br><sub>Taxa de falha L3</sub></td>
</tr>
</table>

## Fontes utilizadas

- Catálogo do ataque: `docker/attackers/arp-scan/attack.yaml`
- Artefatos da campanha: `experiments/60att_5runs_l0l1l2l3/recon_arp_scan`
