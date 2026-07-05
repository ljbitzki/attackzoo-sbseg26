# XSS Scanner (`web_xss_scanner`)

[Índice da campanha](README.md)

Na campanha `experiments/60att_5runs_l0l1l2l3`, este documento consolida a execução do ataque `web_xss_scanner`. No catálogo local, o ataque é descrito como: Automated scan and analysis of parameter flaws susceptible to XSS. A documentação abaixo usa apenas artefatos já presentes no repositório, principalmente as tabelas e figuras de `experiments/60att_5runs_l0l1l2l3/web_xss_scanner`.

## Metadados do ataque

| Campo | Valor |
| --- | --- |
| ID | `web_xss_scanner` |
| Categoria | 3) Web Application Attacks |
| Subcategoria | 3.1 General Web |
| Serviços alvo | http-server |
| Imagem | `attack-xss-scanner:latest` |
| Container | `attack-xss-scanner` |
| Runtime máximo do catálogo | 10 s |
| Parâmetros de intensidade | n/d |
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0043/](https://attack.mitre.org/tactics/TA0043/)<br>[https://attack.mitre.org/tactics/TA0001/](https://attack.mitre.org/tactics/TA0001/)<br>[https://attack.mitre.org/techniques/T1595/](https://attack.mitre.org/techniques/T1595/)<br>[https://attack.mitre.org/techniques/T1595/002/](https://attack.mitre.org/techniques/T1595/002/)<br>[https://attack.mitre.org/techniques/T1190/](https://attack.mitre.org/techniques/T1190/) |

## Resumo estatístico por nível

| Nível | Serviço | Runs | Amostras attack | Sucesso médio | Falha média | Lat p50/p95 ms | PCAP total MB | Dataset médio (min-max) | Exec média s | Extratores ok/total | CPU média/máx | Mem MB média |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | http | 5 | 200 | 100% | 0% | 4,55 / 5,68 | 1,67 | 3.160 (3.160-3.162) | 42,32 | 3/3 | 0,72% / 0,82% | 877,84 |
| L1 | http | 5 | 162 | 95% | 5% | 5,94 / 778,94 | 3 | 4.462 (4.402-4.536) | 42,35 | 3/3 | 4,79% / 27,82% | 935,33 |
| L2 | http | 5 | 160 | 95% | 5% | 5,26 / 781,78 | 3 | 4.470 (4.344-4.584) | 42,37 | 3/3 | 4,65% / 28,12% | 936,21 |
| L3 | http | 5 | 162 | 95% | 5% | 5,61 / 830,31 | 3,01 | 4.487 (4.380-4.626) | 42,36 | 3/3 | 4,63% / 28,92% | 949,55 |

## Estabilidade entre reexecuções

| Nível | Métrica | Runs | Média | Desvio | CV | Min | Max |
| --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | CPU média na fase attack | 5 | 0,72 | 0,07 | 9,4% | 0,65 | 0,83 |
| L0 | Linhas do dataset | 5 | 3.160,4 | 0,89 | 0,03% | 3.160 | 3.162 |
| L0 | Tempo de execução | 5 | 42,32 | 0,48 | 1,14% | 42,03 | 43,17 |
| L0 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L0 | Latência p95 censurada | 5 | 5,68 | 0,86 | 15,23% | 4,81 | 6,77 |
| L1 | CPU média na fase attack | 5 | 4,79 | 1,14 | 23,86% | 2,77 | 5,47 |
| L1 | Linhas do dataset | 5 | 4.462 | 67,01 | 1,5% | 4.402 | 4.536 |
| L1 | Tempo de execução | 5 | 42,35 | 0,09 | 0,22% | 42,24 | 42,43 |
| L1 | Falha na fase attack | 5 | 4,98 | 1,83 | 36,65% | 2,94 | 6,45 |
| L1 | Latência p95 censurada | 5 | 778,94 | 314,75 | 40,41% | 429,8 | 1.169,58 |
| L2 | CPU média na fase attack | 5 | 4,65 | 0,38 | 8,19% | 4,05 | 5,01 |
| L2 | Linhas do dataset | 5 | 4.470,4 | 106,78 | 2,39% | 4.344 | 4.584 |
| L2 | Tempo de execução | 5 | 42,37 | 0,06 | 0,14% | 42,27 | 42,42 |
| L2 | Falha na fase attack | 5 | 5,03 | 1,77 | 35,29% | 2,86 | 6,45 |
| L2 | Latência p95 censurada | 5 | 781,78 | 371,87 | 47,57% | 139,59 | 1.106,24 |
| L3 | CPU média na fase attack | 5 | 4,63 | 1,29 | 27,97% | 2,78 | 6,26 |
| L3 | Linhas do dataset | 5 | 4.487,2 | 100,13 | 2,23% | 4.380 | 4.626 |
| L3 | Tempo de execução | 5 | 42,36 | 0,09 | 0,22% | 42,27 | 42,5 |
| L3 | Falha na fase attack | 5 | 4,99 | 1,83 | 36,62% | 2,86 | 6,45 |
| L3 | Latência p95 censurada | 5 | 830,31 | 403,9 | 48,64% | 182,74 | 1.300,69 |

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
<td><img src="../../assets/campaign_doc/web_xss_scanner/F3_v1_timeseries_http_web_xss_scanner_L0_run01.png" alt="Série temporal L0 run01" width="420"><br><sub>Série temporal L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/web_xss_scanner/F3_v1_timeseries_http_web_xss_scanner_L1_run01.png" alt="Série temporal L1 run01" width="420"><br><sub>Série temporal L1 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/web_xss_scanner/F3_v1_timeseries_http_web_xss_scanner_L2_run01.png" alt="Série temporal L2 run01" width="420"><br><sub>Série temporal L2 run01</sub></td>
<td><img src="../../assets/campaign_doc/web_xss_scanner/F3_v1_timeseries_http_web_xss_scanner_L3_run01.png" alt="Série temporal L3 run01" width="420"><br><sub>Série temporal L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/web_xss_scanner/F5_resources_http_web_xss_scanner_L0_run01.png" alt="Recursos L0 run01" width="420"><br><sub>Recursos L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/web_xss_scanner/F5_resources_http_web_xss_scanner_L3_run01.png" alt="Recursos L3 run01" width="420"><br><sub>Recursos L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/web_xss_scanner/F4_v2_failrate_http_web_xss_scanner_L0.png" alt="Taxa de falha L0" width="420"><br><sub>Taxa de falha L0</sub></td>
<td><img src="../../assets/campaign_doc/web_xss_scanner/F4_v2_failrate_http_web_xss_scanner_L3.png" alt="Taxa de falha L3" width="420"><br><sub>Taxa de falha L3</sub></td>
</tr>
</table>

## Fontes utilizadas

- Catálogo do ataque: `docker/attackers/xss-scanner/attack.yaml`
- Artefatos da campanha: `experiments/60att_5runs_l0l1l2l3/web_xss_scanner`
