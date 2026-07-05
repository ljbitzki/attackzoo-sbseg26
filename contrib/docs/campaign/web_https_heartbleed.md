# HTTPS Heartbleed (`web_https_heartbleed`)

[Índice da campanha](README.md)

Na campanha `experiments/60att_5runs_l0l1l2l3`, este documento consolida a execução do ataque `web_https_heartbleed`. No catálogo local, o ataque é descrito como: Heartbleed scanner/exploitation against a vulnerable HTTPS server. A documentação abaixo usa apenas artefatos já presentes no repositório, principalmente as tabelas e figuras de `experiments/60att_5runs_l0l1l2l3/web_https_heartbleed`.

## Metadados do ataque

| Campo | Valor |
| --- | --- |
| ID | `web_https_heartbleed` |
| Categoria | 3) Web Application Attacks |
| Subcategoria | 3.1 General Web |
| Serviços alvo | http-server |
| Imagem | `attack-web-https-heartbleed:latest` |
| Container | `attack-web-https-heartbleed` |
| Runtime máximo do catálogo | 10 s |
| Parâmetros de intensidade | n/d |
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0043/](https://attack.mitre.org/tactics/TA0043/)<br>[https://attack.mitre.org/tactics/TA0001/](https://attack.mitre.org/tactics/TA0001/)<br>[https://attack.mitre.org/tactics/TA0009/](https://attack.mitre.org/tactics/TA0009/)<br>[https://attack.mitre.org/techniques/T1595/](https://attack.mitre.org/techniques/T1595/)<br>[https://attack.mitre.org/techniques/T1595/002/](https://attack.mitre.org/techniques/T1595/002/)<br>[https://attack.mitre.org/techniques/T1190/](https://attack.mitre.org/techniques/T1190/)<br>[https://attack.mitre.org/techniques/T1005/](https://attack.mitre.org/techniques/T1005/) |

## Resumo estatístico por nível

| Nível | Serviço | Runs | Amostras attack | Sucesso médio | Falha média | Lat p50/p95 ms | PCAP total MB | Dataset médio (min-max) | Exec média s | Extratores ok/total | CPU média/máx | Mem MB média |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | https | 5 | 199 | 100% | 0% | 5,59 / 6,77 | 1,49 | 2.198 (2.184-2.224) | 42,39 | 3/3 | 0,46% / 0,53% | 24,26 |
| L1 | https | 5 | 200 | 100% | 0% | 4,93 / 6,26 | 47,67 | 8.257 (8.222-8.286) | 42,94 | 3/3 | 2,15% / 4,52% | 24,55 |
| L2 | https | 5 | 200 | 100% | 0% | 4,84 / 6,13 | 47,95 | 8.223 (8.206-8.248) | 42,99 | 3/3 | 2,2% / 4,4% | 24,53 |
| L3 | https | 5 | 200 | 100% | 0% | 4,47 / 5,37 | 47,32 | 8.260 (8.242-8.286) | 42,91 | 3/3 | 2,15% / 4,42% | 24,53 |

## Estabilidade entre reexecuções

| Nível | Métrica | Runs | Média | Desvio | CV | Min | Max |
| --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | CPU média na fase attack | 5 | 0,46 | 0,02 | 4,92% | 0,42 | 0,48 |
| L0 | Linhas do dataset | 5 | 2.198 | 18,11 | 0,82% | 2.184 | 2.224 |
| L0 | Tempo de execução | 5 | 42,39 | 0,55 | 1,3% | 42,11 | 43,37 |
| L0 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L0 | Latência p95 censurada | 5 | 6,77 | 0,44 | 6,52% | 6,24 | 7,27 |
| L1 | CPU média na fase attack | 5 | 2,15 | 0,11 | 5,04% | 2,01 | 2,29 |
| L1 | Linhas do dataset | 5 | 8.257,2 | 26,86 | 0,33% | 8.222 | 8.286 |
| L1 | Tempo de execução | 5 | 42,94 | 0,06 | 0,14% | 42,86 | 43,01 |
| L1 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L1 | Latência p95 censurada | 5 | 6,26 | 0,75 | 11,98% | 4,96 | 6,82 |
| L2 | CPU média na fase attack | 5 | 2,2 | 0,06 | 2,65% | 2,13 | 2,28 |
| L2 | Linhas do dataset | 5 | 8.222,8 | 19,01 | 0,23% | 8.206 | 8.248 |
| L2 | Tempo de execução | 5 | 42,99 | 0,09 | 0,22% | 42,88 | 43,12 |
| L2 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L2 | Latência p95 censurada | 5 | 6,13 | 0,41 | 6,63% | 5,79 | 6,83 |
| L3 | CPU média na fase attack | 5 | 2,15 | 0,02 | 1,13% | 2,13 | 2,19 |
| L3 | Linhas do dataset | 5 | 8.259,6 | 19,31 | 0,23% | 8.242 | 8.286 |
| L3 | Tempo de execução | 5 | 42,91 | 0,05 | 0,11% | 42,86 | 42,98 |
| L3 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L3 | Latência p95 censurada | 5 | 5,37 | 0,38 | 7,02% | 5 | 5,85 |

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
<td><img src="../../assets/campaign_doc/web_https_heartbleed/F3_v1_timeseries_https_web_https_heartbleed_L0_run01.png" alt="Série temporal L0 run01" width="420"><br><sub>Série temporal L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/web_https_heartbleed/F3_v1_timeseries_https_web_https_heartbleed_L1_run01.png" alt="Série temporal L1 run01" width="420"><br><sub>Série temporal L1 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/web_https_heartbleed/F3_v1_timeseries_https_web_https_heartbleed_L2_run01.png" alt="Série temporal L2 run01" width="420"><br><sub>Série temporal L2 run01</sub></td>
<td><img src="../../assets/campaign_doc/web_https_heartbleed/F3_v1_timeseries_https_web_https_heartbleed_L3_run01.png" alt="Série temporal L3 run01" width="420"><br><sub>Série temporal L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/web_https_heartbleed/F5_resources_https_web_https_heartbleed_L0_run01.png" alt="Recursos L0 run01" width="420"><br><sub>Recursos L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/web_https_heartbleed/F5_resources_https_web_https_heartbleed_L3_run01.png" alt="Recursos L3 run01" width="420"><br><sub>Recursos L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/web_https_heartbleed/F4_v2_failrate_https_web_https_heartbleed_L0.png" alt="Taxa de falha L0" width="420"><br><sub>Taxa de falha L0</sub></td>
<td><img src="../../assets/campaign_doc/web_https_heartbleed/F4_v2_failrate_https_web_https_heartbleed_L3.png" alt="Taxa de falha L3" width="420"><br><sub>Taxa de falha L3</sub></td>
</tr>
</table>

## Fontes utilizadas

- Catálogo do ataque: `docker/attackers/web-https-heartbleed/attack.yaml`
- Artefatos da campanha: `experiments/60att_5runs_l0l1l2l3/web_https_heartbleed`
