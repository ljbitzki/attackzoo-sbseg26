# DoS HTTP Slowloris (`dos_http_slowloris`)

[Índice da campanha](README.md)

Na campanha `experiments/60att_5runs_l0l1l2l3`, este documento consolida a execução do ataque `dos_http_slowloris`. No catálogo local, o ataque é descrito como: Slowloris-style HTTP application DoS. A documentação abaixo usa apenas artefatos já presentes no repositório, principalmente as tabelas e figuras de `experiments/60att_5runs_l0l1l2l3/dos_http_slowloris`.

## Metadados do ataque

| Campo | Valor |
| --- | --- |
| ID | `dos_http_slowloris` |
| Categoria | 6) Denial of Service and Impact |
| Subcategoria | 6.2 Application-layer DoS |
| Serviços alvo | http-server |
| Imagem | `attack-dos-http-slowloris:latest` |
| Container | `attack-dos-http-slowloris` |
| Runtime máximo do catálogo | 10 s |
| Parâmetros de intensidade | duration_s |
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0040/](https://attack.mitre.org/tactics/TA0040/)<br>[https://attack.mitre.org/techniques/T1499/](https://attack.mitre.org/techniques/T1499/)<br>[https://attack.mitre.org/techniques/T1499/003/](https://attack.mitre.org/techniques/T1499/003/) |

## Resumo estatístico por nível

| Nível | Serviço | Runs | Amostras attack | Sucesso médio | Falha média | Lat p50/p95 ms | PCAP total MB | Dataset médio (min-max) | Exec média s | Extratores ok/total | CPU média/máx | Mem MB média |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | http | 5 | 200 | 100% | 0% | 4,25 / 5,31 | 1,67 | 3.168 (3.160-3.200) | 42,27 | 3/3 | 0,66% / 0,77% | 225,81 |
| L1 | http | 5 | 51 | 31,3% | 68,7% | 2.002,81 / 2.002,81 | 2,42 | 6.568 (6.546-6.606) | 42,53 | 3/3 | 0,66% / 2,46% | 408,21 |
| L2 | http | 5 | 48 | 26,9% | 73,1% | 2.002,88 / 2.002,88 | 2,42 | 6.610 (6.518-6.842) | 42,59 | 3/3 | 0,47% / 1,9% | 444,84 |
| L3 | http | 5 | 48 | 26,9% | 73,1% | 2.002,95 / 2.002,95 | 2,41 | 6.536 (6.498-6.562) | 42,55 | 3/3 | 0,52% / 1,99% | 447,77 |

## Estabilidade entre reexecuções

| Nível | Métrica | Runs | Média | Desvio | CV | Min | Max |
| --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | CPU média na fase attack | 5 | 0,66 | 0,03 | 5,16% | 0,62 | 0,7 |
| L0 | Linhas do dataset | 5 | 3.168,4 | 17,69 | 0,56% | 3.160 | 3.200 |
| L0 | Tempo de execução | 5 | 42,27 | 0,46 | 1,08% | 42,01 | 43,08 |
| L0 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L0 | Latência p95 censurada | 5 | 5,31 | 0,8 | 15,15% | 4,45 | 6,32 |
| L1 | CPU média na fase attack | 5 | 0,66 | 0,36 | 54,24% | 0,43 | 1,3 |
| L1 | Linhas do dataset | 5 | 6.567,6 | 23,08 | 0,35% | 6.546 | 6.606 |
| L1 | Tempo de execução | 5 | 42,53 | 0,04 | 0,09% | 42,49 | 42,58 |
| L1 | Falha na fase attack | 5 | 68,73 | 2,85 | 4,14% | 63,64 | 70 |
| L1 | Latência p95 censurada | 5 | 2.002,81 | 0,07 | 0% | 2.002,76 | 2.002,94 |
| L2 | CPU média na fase attack | 5 | 0,47 | 0,09 | 20,2% | 0,39 | 0,63 |
| L2 | Linhas do dataset | 5 | 6.610 | 131,21 | 1,99% | 6.518 | 6.842 |
| L2 | Tempo de execução | 5 | 42,59 | 0,05 | 0,11% | 42,54 | 42,64 |
| L2 | Falha na fase attack | 5 | 73,11 | 4,26 | 5,83% | 70 | 77,78 |
| L2 | Latência p95 censurada | 5 | 2.002,88 | 0,29 | 0,01% | 2.002,72 | 2.003,39 |
| L3 | CPU média na fase attack | 5 | 0,52 | 0,11 | 20,18% | 0,43 | 0,7 |
| L3 | Linhas do dataset | 5 | 6.535,6 | 31,19 | 0,48% | 6.498 | 6.562 |
| L3 | Tempo de execução | 5 | 42,55 | 0,07 | 0,17% | 42,5 | 42,68 |
| L3 | Falha na fase attack | 5 | 73,11 | 4,26 | 5,83% | 70 | 77,78 |
| L3 | Latência p95 censurada | 5 | 2.002,95 | 0,35 | 0,02% | 2.002,69 | 2.003,55 |

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
<td><img src="../../assets/campaign_doc/dos_http_slowloris/F3_v1_timeseries_http_dos_http_slowloris_L0_run01.png" alt="Série temporal L0 run01" width="420"><br><sub>Série temporal L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/dos_http_slowloris/F3_v1_timeseries_http_dos_http_slowloris_L1_run01.png" alt="Série temporal L1 run01" width="420"><br><sub>Série temporal L1 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/dos_http_slowloris/F3_v1_timeseries_http_dos_http_slowloris_L2_run01.png" alt="Série temporal L2 run01" width="420"><br><sub>Série temporal L2 run01</sub></td>
<td><img src="../../assets/campaign_doc/dos_http_slowloris/F3_v1_timeseries_http_dos_http_slowloris_L3_run01.png" alt="Série temporal L3 run01" width="420"><br><sub>Série temporal L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/dos_http_slowloris/F5_resources_http_dos_http_slowloris_L0_run01.png" alt="Recursos L0 run01" width="420"><br><sub>Recursos L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/dos_http_slowloris/F5_resources_http_dos_http_slowloris_L3_run01.png" alt="Recursos L3 run01" width="420"><br><sub>Recursos L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/dos_http_slowloris/F4_v2_failrate_http_dos_http_slowloris_L0.png" alt="Taxa de falha L0" width="420"><br><sub>Taxa de falha L0</sub></td>
<td><img src="../../assets/campaign_doc/dos_http_slowloris/F4_v2_failrate_http_dos_http_slowloris_L3.png" alt="Taxa de falha L3" width="420"><br><sub>Taxa de falha L3</sub></td>
</tr>
</table>

## Fontes utilizadas

- Catálogo do ataque: `docker/attackers/dos-http-slowloris/attack.yaml`
- Artefatos da campanha: `experiments/60att_5runs_l0l1l2l3/dos_http_slowloris`
