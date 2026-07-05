# Zenoh-Pico Timestamp Manipulation Flood (`iot_zenoh_pico_timestamp_mess`)

[Índice da campanha](README.md)

Na campanha `experiments/60att_5runs_l0l1l2l3`, este documento consolida a execução do ataque `iot_zenoh_pico_timestamp_mess`. No catálogo local, o ataque é descrito como: Flood of Zenoh/Zenoh-Pico packets with manipulated timestamps to affect target ordering, expiration, or time logic. A documentação abaixo usa apenas artefatos já presentes no repositório, principalmente as tabelas e figuras de `experiments/60att_5runs_l0l1l2l3/iot_zenoh_pico_timestamp_mess`.

## Metadados do ataque

| Campo | Valor |
| --- | --- |
| ID | `iot_zenoh_pico_timestamp_mess` |
| Categoria | 7) IoT |
| Subcategoria | 7.1 IoT Protocols / Zenoh |
| Serviços alvo | zenoh-router |
| Imagem | `attack-zenoh-pico-timestamp-mess:latest` |
| Container | `attack-zenoh-pico-timestamp-mess` |
| Runtime máximo do catálogo | 10 s |
| Parâmetros de intensidade | duration_s, threads |
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0040/](https://attack.mitre.org/tactics/TA0040/)<br>[https://attack.mitre.org/techniques/T1499/](https://attack.mitre.org/techniques/T1499/)<br>[https://attack.mitre.org/techniques/T1499/003/](https://attack.mitre.org/techniques/T1499/003/)<br>[https://attack.mitre.org/techniques/T1565/](https://attack.mitre.org/techniques/T1565/)<br>[https://attack.mitre.org/techniques/T1565/002/](https://attack.mitre.org/techniques/T1565/002/) |

## Resumo estatístico por nível

| Nível | Serviço | Runs | Amostras attack | Sucesso médio | Falha média | Lat p50/p95 ms | PCAP total MB | Dataset médio (min-max) | Exec média s | Extratores ok/total | CPU média/máx | Mem MB média |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | zenoh | 5 | 200 | 100% | 0% | 0,31 / 0,47 | 0,79 | 3.689 (3.674-3.702) | 42,56 | 3/3 | 0,13% / 0,17% | 5,4 |
| L1 | zenoh | 5 | 200 | 100% | 0% | 0,27 / 0,43 | 34,48 | 146.365 (143.784-147.870) | 62,67 | 3/3 | 0,12% / 0,15% | 5,41 |
| L2 | zenoh | 5 | 200 | 100% | 0% | 0,32 / 0,45 | 34,73 | 147.451 (145.744-148.140) | 62,81 | 3/3 | 0,13% / 0,17% | 5,4 |
| L3 | zenoh | 5 | 200 | 100% | 0% | 0,29 / 0,46 | 34,59 | 146.868 (144.664-148.212) | 62,6 | 3/3 | 0,12% / 0,16% | 5,43 |

## Estabilidade entre reexecuções

| Nível | Métrica | Runs | Média | Desvio | CV | Min | Max |
| --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | CPU média na fase attack | 5 | 0,13 | 0,01 | 8,6% | 0,11 | 0,14 |
| L0 | Linhas do dataset | 5 | 3.688,8 | 10,83 | 0,29% | 3.674 | 3.702 |
| L0 | Tempo de execução | 5 | 42,56 | 0,6 | 1,42% | 42,23 | 43,64 |
| L0 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L0 | Latência p95 censurada | 5 | 0,47 | 0,04 | 9,37% | 0,43 | 0,54 |
| L1 | CPU média na fase attack | 5 | 0,12 | 0,01 | 6,94% | 0,11 | 0,14 |
| L1 | Linhas do dataset | 5 | 146.365,2 | 1.874,79 | 1,28% | 143.784 | 147.870 |
| L1 | Tempo de execução | 5 | 62,67 | 0,13 | 0,21% | 62,48 | 62,81 |
| L1 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L1 | Latência p95 censurada | 5 | 0,43 | 0,04 | 8,35% | 0,37 | 0,47 |
| L2 | CPU média na fase attack | 5 | 0,13 | 0,01 | 6,89% | 0,12 | 0,14 |
| L2 | Linhas do dataset | 5 | 147.451,2 | 968,44 | 0,66% | 145.744 | 148.140 |
| L2 | Tempo de execução | 5 | 62,81 | 0,26 | 0,42% | 62,47 | 63,18 |
| L2 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L2 | Latência p95 censurada | 5 | 0,45 | 0,04 | 9,53% | 0,4 | 0,51 |
| L3 | CPU média na fase attack | 5 | 0,12 | 0,01 | 8,58% | 0,11 | 0,14 |
| L3 | Linhas do dataset | 5 | 146.867,6 | 1.687,79 | 1,15% | 144.664 | 148.212 |
| L3 | Tempo de execução | 5 | 62,6 | 0,42 | 0,67% | 62,01 | 63,16 |
| L3 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L3 | Latência p95 censurada | 5 | 0,46 | 0,05 | 10,65% | 0,39 | 0,52 |

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
<td><img src="../../assets/campaign_doc/iot_zenoh_pico_timestamp_mess/F3_v1_timeseries_zenoh_iot_zenoh_pico_timestamp_mess_L0_run01.png" alt="Série temporal L0 run01" width="420"><br><sub>Série temporal L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/iot_zenoh_pico_timestamp_mess/F3_v1_timeseries_zenoh_iot_zenoh_pico_timestamp_mess_L1_run01.png" alt="Série temporal L1 run01" width="420"><br><sub>Série temporal L1 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/iot_zenoh_pico_timestamp_mess/F3_v1_timeseries_zenoh_iot_zenoh_pico_timestamp_mess_L2_run01.png" alt="Série temporal L2 run01" width="420"><br><sub>Série temporal L2 run01</sub></td>
<td><img src="../../assets/campaign_doc/iot_zenoh_pico_timestamp_mess/F3_v1_timeseries_zenoh_iot_zenoh_pico_timestamp_mess_L3_run01.png" alt="Série temporal L3 run01" width="420"><br><sub>Série temporal L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/iot_zenoh_pico_timestamp_mess/F5_resources_zenoh_iot_zenoh_pico_timestamp_mess_L0_run01.png" alt="Recursos L0 run01" width="420"><br><sub>Recursos L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/iot_zenoh_pico_timestamp_mess/F5_resources_zenoh_iot_zenoh_pico_timestamp_mess_L3_run01.png" alt="Recursos L3 run01" width="420"><br><sub>Recursos L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/iot_zenoh_pico_timestamp_mess/F4_v2_failrate_zenoh_iot_zenoh_pico_timestamp_mess_L0.png" alt="Taxa de falha L0" width="420"><br><sub>Taxa de falha L0</sub></td>
<td><img src="../../assets/campaign_doc/iot_zenoh_pico_timestamp_mess/F4_v2_failrate_zenoh_iot_zenoh_pico_timestamp_mess_L3.png" alt="Taxa de falha L3" width="420"><br><sub>Taxa de falha L3</sub></td>
</tr>
</table>

## Fontes utilizadas

- Catálogo do ataque: `docker/attackers/zenoh-pico-timestamp-mess/attack.yaml`
- Artefatos da campanha: `experiments/60att_5runs_l0l1l2l3/iot_zenoh_pico_timestamp_mess`
