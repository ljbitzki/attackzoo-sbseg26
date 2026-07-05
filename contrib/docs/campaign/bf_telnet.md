# Telnet Bruteforce (`bf_telnet`)

[Índice da campanha](README.md)

Na campanha `experiments/60att_5runs_l0l1l2l3`, este documento consolida a execução do ataque `bf_telnet`. No catálogo local, o ataque é descrito como: Telnet authentication brute force. A documentação abaixo usa apenas artefatos já presentes no repositório, principalmente as tabelas e figuras de `experiments/60att_5runs_l0l1l2l3/bf_telnet`.

## Metadados do ataque

| Campo | Valor |
| --- | --- |
| ID | `bf_telnet` |
| Categoria | 4) Brute Force Against Remote Access Applications |
| Subcategoria | 4.1 Brute Force |
| Serviços alvo | telnet-server |
| Imagem | `attack-telnet-bruteforce:latest` |
| Container | `attack-telnet-bruteforce` |
| Runtime máximo do catálogo | 10 s |
| Parâmetros de intensidade | n/d |
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0006/](https://attack.mitre.org/tactics/TA0006/)<br>[https://attack.mitre.org/techniques/T1110/](https://attack.mitre.org/techniques/T1110/)<br>[https://attack.mitre.org/techniques/T1110/001/](https://attack.mitre.org/techniques/T1110/001/) |

## Resumo estatístico por nível

| Nível | Serviço | Runs | Amostras attack | Sucesso médio | Falha média | Lat p50/p95 ms | PCAP total MB | Dataset médio (min-max) | Exec média s | Extratores ok/total | CPU média/máx | Mem MB média |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | telnet | 5 | 200 | 100% | 0% | 3,71 / 4,98 | 0,29 | 1.309 (1.304-1.312) | 42,01 | 3/3 | 0,59% / 0,72% | 2,06 |
| L1 | telnet | 5 | 200 | 100% | 0% | 4,12 / 5,75 | 1,23 | 5.521 (5.498-5.548) | 42,78 | 3/3 | 3,45% / 14,67% | 17,89 |
| L2 | telnet | 5 | 200 | 100% | 0% | 3,83 / 4,82 | 1,24 | 5.558 (5.518-5.626) | 42,38 | 3/3 | 2,46% / 11,74% | 17,82 |
| L3 | telnet | 5 | 200 | 100% | 0% | 4 / 5,62 | 1,25 | 5.607 (5.468-5.782) | 42,49 | 3/3 | 2,95% / 13,39% | 17,96 |

## Estabilidade entre reexecuções

| Nível | Métrica | Runs | Média | Desvio | CV | Min | Max |
| --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | CPU média na fase attack | 5 | 0,59 | 0,03 | 5,73% | 0,55 | 0,62 |
| L0 | Linhas do dataset | 5 | 1.309,2 | 3,9 | 0,3% | 1.304 | 1.312 |
| L0 | Tempo de execução | 5 | 42,01 | 0,41 | 0,97% | 41,76 | 42,73 |
| L0 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L0 | Latência p95 censurada | 5 | 4,98 | 0,55 | 11,12% | 4,11 | 5,47 |
| L1 | CPU média na fase attack | 5 | 3,45 | 0,54 | 15,71% | 2,71 | 4,14 |
| L1 | Linhas do dataset | 5 | 5.521,2 | 20,72 | 0,38% | 5.498 | 5.548 |
| L1 | Tempo de execução | 5 | 42,78 | 0,61 | 1,43% | 42,44 | 43,87 |
| L1 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L1 | Latência p95 censurada | 5 | 5,75 | 0,71 | 12,31% | 4,91 | 6,58 |
| L2 | CPU média na fase attack | 5 | 2,46 | 0,43 | 17,54% | 2,17 | 3,21 |
| L2 | Linhas do dataset | 5 | 5.558 | 45,76 | 0,82% | 5.518 | 5.626 |
| L2 | Tempo de execução | 5 | 42,38 | 0,04 | 0,09% | 42,31 | 42,41 |
| L2 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L2 | Latência p95 censurada | 5 | 4,82 | 0,89 | 18,42% | 3,79 | 6,2 |
| L3 | CPU média na fase attack | 5 | 2,95 | 0,65 | 21,97% | 2,17 | 3,95 |
| L3 | Linhas do dataset | 5 | 5.607,2 | 119,64 | 2,13% | 5.468 | 5.782 |
| L3 | Tempo de execução | 5 | 42,49 | 0,09 | 0,21% | 42,42 | 42,63 |
| L3 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L3 | Latência p95 censurada | 5 | 5,62 | 0,59 | 10,58% | 4,87 | 6,28 |

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
<td><img src="../../assets/campaign_doc/bf_telnet/F3_v1_timeseries_telnet_bf_telnet_L0_run01.png" alt="Série temporal L0 run01" width="420"><br><sub>Série temporal L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/bf_telnet/F3_v1_timeseries_telnet_bf_telnet_L1_run01.png" alt="Série temporal L1 run01" width="420"><br><sub>Série temporal L1 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/bf_telnet/F3_v1_timeseries_telnet_bf_telnet_L2_run01.png" alt="Série temporal L2 run01" width="420"><br><sub>Série temporal L2 run01</sub></td>
<td><img src="../../assets/campaign_doc/bf_telnet/F3_v1_timeseries_telnet_bf_telnet_L3_run01.png" alt="Série temporal L3 run01" width="420"><br><sub>Série temporal L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/bf_telnet/F5_resources_telnet_bf_telnet_L0_run01.png" alt="Recursos L0 run01" width="420"><br><sub>Recursos L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/bf_telnet/F5_resources_telnet_bf_telnet_L3_run01.png" alt="Recursos L3 run01" width="420"><br><sub>Recursos L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/bf_telnet/F4_v2_failrate_telnet_bf_telnet_L0.png" alt="Taxa de falha L0" width="420"><br><sub>Taxa de falha L0</sub></td>
<td><img src="../../assets/campaign_doc/bf_telnet/F4_v2_failrate_telnet_bf_telnet_L3.png" alt="Taxa de falha L3" width="420"><br><sub>Taxa de falha L3</sub></td>
</tr>
</table>

## Fontes utilizadas

- Catálogo do ataque: `docker/attackers/telnet-bruteforce/attack.yaml`
- Artefatos da campanha: `experiments/60att_5runs_l0l1l2l3/bf_telnet`
