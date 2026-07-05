# Web Wide Scanner (`web_wide_scanner`)

[Índice da campanha](README.md)

Na campanha `experiments/60att_5runs_l0l1l2l3`, este documento consolida a execução do ataque `web_wide_scanner`. No catálogo local, o ataque é descrito como: Broad scanner for known web vulnerabilities. A documentação abaixo usa apenas artefatos já presentes no repositório, principalmente as tabelas e figuras de `experiments/60att_5runs_l0l1l2l3/web_wide_scanner`.

## Metadados do ataque

| Campo | Valor |
| --- | --- |
| ID | `web_wide_scanner` |
| Categoria | 3) Web Application Attacks |
| Subcategoria | 3.1 General Web |
| Serviços alvo | http-server |
| Imagem | `attack-web-wide-scanner:latest` |
| Container | `attack-web-wide-scanner` |
| Runtime máximo do catálogo | 10 s |
| Parâmetros de intensidade | n/d |
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0043/](https://attack.mitre.org/tactics/TA0043/)<br>[https://attack.mitre.org/techniques/T1590/](https://attack.mitre.org/techniques/T1590/)<br>[https://attack.mitre.org/techniques/T1592/](https://attack.mitre.org/techniques/T1592/)<br>[https://attack.mitre.org/techniques/T1595/](https://attack.mitre.org/techniques/T1595/)<br>[https://attack.mitre.org/techniques/T1595/002/](https://attack.mitre.org/techniques/T1595/002/) |

## Resumo estatístico por nível

| Nível | Serviço | Runs | Amostras attack | Sucesso médio | Falha média | Lat p50/p95 ms | PCAP total MB | Dataset médio (min-max) | Exec média s | Extratores ok/total | CPU média/máx | Mem MB média |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | http | 5 | 200 | 100% | 0% | 4,82 / 5,68 | 1,67 | 3.160 (3.120-3.200) | 42,25 | 3/3 | 0,7% / 0,77% | 881,73 |
| L1 | http | 5 | 200 | 100% | 0% | 5,16 / 6,71 | 1,66 | 3.136 (3.120-3.160) | 42,2 | 3/3 | 0,79% / 0,94% | 872,76 |
| L2 | http | 5 | 200 | 100% | 0% | 4,65 / 5,93 | 1,67 | 3.160 (3.160-3.162) | 42,09 | 3/3 | 0,73% / 0,87% | 873,32 |
| L3 | http | 5 | 200 | 100% | 0% | 5,11 / 6,66 | 1,66 | 3.144 (3.120-3.160) | 42,19 | 3/3 | 0,78% / 0,94% | 875,56 |

## Estabilidade entre reexecuções

| Nível | Métrica | Runs | Média | Desvio | CV | Min | Max |
| --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | CPU média na fase attack | 5 | 0,7 | 0,04 | 5,15% | 0,67 | 0,76 |
| L0 | Linhas do dataset | 5 | 3.160,4 | 28,3 | 0,9% | 3.120 | 3.200 |
| L0 | Tempo de execução | 5 | 42,25 | 0,32 | 0,75% | 42,04 | 42,81 |
| L0 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L0 | Latência p95 censurada | 5 | 5,68 | 0,63 | 11,16% | 5,17 | 6,78 |
| L1 | CPU média na fase attack | 5 | 0,79 | 0,07 | 8,84% | 0,67 | 0,84 |
| L1 | Linhas do dataset | 5 | 3.136 | 21,91 | 0,7% | 3.120 | 3.160 |
| L1 | Tempo de execução | 5 | 42,2 | 0,08 | 0,18% | 42,12 | 42,29 |
| L1 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L1 | Latência p95 censurada | 5 | 6,71 | 0,92 | 13,78% | 5,33 | 7,89 |
| L2 | CPU média na fase attack | 5 | 0,73 | 0,08 | 11,35% | 0,66 | 0,84 |
| L2 | Linhas do dataset | 5 | 3.160,4 | 0,89 | 0,03% | 3.160 | 3.162 |
| L2 | Tempo de execução | 5 | 42,09 | 0,04 | 0,09% | 42,04 | 42,14 |
| L2 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L2 | Latência p95 censurada | 5 | 5,93 | 0,92 | 15,55% | 5,09 | 7,39 |
| L3 | CPU média na fase attack | 5 | 0,78 | 0,09 | 11,49% | 0,67 | 0,91 |
| L3 | Linhas do dataset | 5 | 3.144 | 21,91 | 0,7% | 3.120 | 3.160 |
| L3 | Tempo de execução | 5 | 42,19 | 0,07 | 0,16% | 42,13 | 42,27 |
| L3 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L3 | Latência p95 censurada | 5 | 6,66 | 0,86 | 12,86% | 5,39 | 7,6 |

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
<td><img src="../../assets/campaign_doc/web_wide_scanner/F3_v1_timeseries_http_web_wide_scanner_L0_run01.png" alt="Série temporal L0 run01" width="420"><br><sub>Série temporal L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/web_wide_scanner/F3_v1_timeseries_http_web_wide_scanner_L1_run01.png" alt="Série temporal L1 run01" width="420"><br><sub>Série temporal L1 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/web_wide_scanner/F3_v1_timeseries_http_web_wide_scanner_L2_run01.png" alt="Série temporal L2 run01" width="420"><br><sub>Série temporal L2 run01</sub></td>
<td><img src="../../assets/campaign_doc/web_wide_scanner/F3_v1_timeseries_http_web_wide_scanner_L3_run01.png" alt="Série temporal L3 run01" width="420"><br><sub>Série temporal L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/web_wide_scanner/F5_resources_http_web_wide_scanner_L0_run01.png" alt="Recursos L0 run01" width="420"><br><sub>Recursos L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/web_wide_scanner/F5_resources_http_web_wide_scanner_L3_run01.png" alt="Recursos L3 run01" width="420"><br><sub>Recursos L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/web_wide_scanner/F4_v2_failrate_http_web_wide_scanner_L0.png" alt="Taxa de falha L0" width="420"><br><sub>Taxa de falha L0</sub></td>
<td><img src="../../assets/campaign_doc/web_wide_scanner/F4_v2_failrate_http_web_wide_scanner_L3.png" alt="Taxa de falha L3" width="420"><br><sub>Taxa de falha L3</sub></td>
</tr>
</table>

## Fontes utilizadas

- Catálogo do ataque: `docker/attackers/web-wide-scanner/attack.yaml`
- Artefatos da campanha: `experiments/60att_5runs_l0l1l2l3/web_wide_scanner`
