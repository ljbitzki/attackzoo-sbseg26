# Web POST Bruteforce (`web_post_bruteforce`)

[Índice da campanha](README.md)

Na campanha `experiments/60att_5runs_l0l1l2l3`, este documento consolida a execução do ataque `web_post_bruteforce`. No catálogo local, o ataque é descrito como: Web application POST authentication brute force using a wordlist. A documentação abaixo usa apenas artefatos já presentes no repositório, principalmente as tabelas e figuras de `experiments/60att_5runs_l0l1l2l3/web_post_bruteforce`.

## Metadados do ataque

| Campo | Valor |
| --- | --- |
| ID | `web_post_bruteforce` |
| Categoria | 3) Web Application Attacks |
| Subcategoria | 3.1 General Web |
| Serviços alvo | http-server |
| Imagem | `attack-web-post-bruteforce:latest` |
| Container | `attack-web-post-bruteforce` |
| Runtime máximo do catálogo | 10 s |
| Parâmetros de intensidade | n/d |
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0006/](https://attack.mitre.org/tactics/TA0006/)<br>[https://attack.mitre.org/techniques/T1110/](https://attack.mitre.org/techniques/T1110/)<br>[https://attack.mitre.org/techniques/T1110/001/](https://attack.mitre.org/techniques/T1110/001/) |

## Resumo estatístico por nível

| Nível | Serviço | Runs | Amostras attack | Sucesso médio | Falha média | Lat p50/p95 ms | PCAP total MB | Dataset médio (min-max) | Exec média s | Extratores ok/total | CPU média/máx | Mem MB média |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | http | 5 | 200 | 100% | 0% | 4,95 / 6,47 | 1,67 | 3.152 (3.120-3.162) | 42,32 | 3/3 | 0,76% / 0,95% | 961,5 |
| L1 | http | 5 | 161 | 95,6% | 4,4% | 5,35 / 809,77 | 5,25 | 7.600 (7.472-7.698) | 42,82 | 3/3 | 6,73% / 50,94% | 1.004,67 |
| L2 | http | 5 | 169 | 96,9% | 3,1% | 5,95 / 632,7 | 4,65 | 6.944 (4.160-7.662) | 42,72 | 3/3 | 5,84% / 42,31% | 1.009,12 |
| L3 | http | 5 | 163 | 96,3% | 3,7% | 6,12 / 713,47 | 5,24 | 7.560 (7.512-7.622) | 42,86 | 3/3 | 7,17% / 52,93% | 1.015,61 |

## Estabilidade entre reexecuções

| Nível | Métrica | Runs | Média | Desvio | CV | Min | Max |
| --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | CPU média na fase attack | 5 | 0,76 | 0,08 | 10,54% | 0,66 | 0,87 |
| L0 | Linhas do dataset | 5 | 3.152,4 | 18,13 | 0,58% | 3.120 | 3.162 |
| L0 | Tempo de execução | 5 | 42,32 | 0,34 | 0,8% | 42,07 | 42,91 |
| L0 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L0 | Latência p95 censurada | 5 | 6,47 | 1,08 | 16,66% | 5,04 | 7,79 |
| L1 | CPU média na fase attack | 5 | 6,73 | 0,41 | 6,13% | 6,42 | 7,35 |
| L1 | Linhas do dataset | 5 | 7.600,4 | 86,57 | 1,14% | 7.472 | 7.698 |
| L1 | Tempo de execução | 5 | 42,82 | 0,09 | 0,22% | 42,7 | 42,93 |
| L1 | Falha na fase attack | 5 | 4,36 | 1,73 | 39,7% | 3,03 | 6,25 |
| L1 | Latência p95 censurada | 5 | 809,77 | 114,3 | 14,12% | 632,53 | 906,18 |
| L2 | CPU média na fase attack | 5 | 5,84 | 2,53 | 43,27% | 1,38 | 7,34 |
| L2 | Linhas do dataset | 5 | 6.943,6 | 1.556,2 | 22,41% | 4.160 | 7.662 |
| L2 | Tempo de execução | 5 | 42,72 | 0,29 | 0,67% | 42,21 | 42,9 |
| L2 | Falha na fase attack | 5 | 3,11 | 2,21 | 71,15% | 0 | 6,25 |
| L2 | Latência p95 censurada | 5 | 632,7 | 373,51 | 59,03% | 5,8 | 906,66 |
| L3 | CPU média na fase attack | 5 | 7,17 | 0,32 | 4,42% | 6,75 | 7,43 |
| L3 | Linhas do dataset | 5 | 7.559,6 | 55,34 | 0,73% | 7.512 | 7.622 |
| L3 | Tempo de execução | 5 | 42,86 | 0,08 | 0,19% | 42,77 | 42,95 |
| L3 | Falha na fase attack | 5 | 3,69 | 1,43 | 38,72% | 3,03 | 6,25 |
| L3 | Latência p95 censurada | 5 | 713,47 | 144,94 | 20,31% | 573,46 | 905,77 |

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
<td><img src="../../assets/campaign_doc/web_post_bruteforce/F3_v1_timeseries_http_web_post_bruteforce_L0_run01.png" alt="Série temporal L0 run01" width="420"><br><sub>Série temporal L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/web_post_bruteforce/F3_v1_timeseries_http_web_post_bruteforce_L1_run01.png" alt="Série temporal L1 run01" width="420"><br><sub>Série temporal L1 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/web_post_bruteforce/F3_v1_timeseries_http_web_post_bruteforce_L2_run01.png" alt="Série temporal L2 run01" width="420"><br><sub>Série temporal L2 run01</sub></td>
<td><img src="../../assets/campaign_doc/web_post_bruteforce/F3_v1_timeseries_http_web_post_bruteforce_L3_run01.png" alt="Série temporal L3 run01" width="420"><br><sub>Série temporal L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/web_post_bruteforce/F5_resources_http_web_post_bruteforce_L0_run01.png" alt="Recursos L0 run01" width="420"><br><sub>Recursos L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/web_post_bruteforce/F5_resources_http_web_post_bruteforce_L3_run01.png" alt="Recursos L3 run01" width="420"><br><sub>Recursos L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/web_post_bruteforce/F4_v2_failrate_http_web_post_bruteforce_L0.png" alt="Taxa de falha L0" width="420"><br><sub>Taxa de falha L0</sub></td>
<td><img src="../../assets/campaign_doc/web_post_bruteforce/F4_v2_failrate_http_web_post_bruteforce_L3.png" alt="Taxa de falha L3" width="420"><br><sub>Taxa de falha L3</sub></td>
</tr>
</table>

## Fontes utilizadas

- Catálogo do ataque: `docker/attackers/web-post-bruteforce/attack.yaml`
- Artefatos da campanha: `experiments/60att_5runs_l0l1l2l3/web_post_bruteforce`
