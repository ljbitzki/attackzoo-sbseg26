# Zenoh-Pico Sequence Exhaustion (`iot_zenoh_pico_sequence_exhaustion`)

[Índice da campanha](README.md)

Na campanha `experiments/60att_5runs_l0l1l2l3`, este documento consolida a execução do ataque `iot_zenoh_pico_sequence_exhaustion`. No catálogo local, o ataque é descrito como: Exhaustion or intensive manipulation of Zenoh/Zenoh-Pico sequence numbers to degrade ordering, reliability, or session-state control. A documentação abaixo usa apenas artefatos já presentes no repositório, principalmente as tabelas e figuras de `experiments/60att_5runs_l0l1l2l3/iot_zenoh_pico_sequence_exhaustion`.

## Metadados do ataque

| Campo | Valor |
| --- | --- |
| ID | `iot_zenoh_pico_sequence_exhaustion` |
| Categoria | 7) IoT |
| Subcategoria | 7.1 IoT Protocols / Zenoh |
| Serviços alvo | zenoh-router |
| Imagem | `attack-zenoh-pico-sequence-exhaustion:latest` |
| Container | `attack-zenoh-pico-sequence-exhaustion` |
| Runtime máximo do catálogo | 10 s |
| Parâmetros de intensidade | duration_s, threads |
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0040/](https://attack.mitre.org/tactics/TA0040/)<br>[https://attack.mitre.org/techniques/T1499/](https://attack.mitre.org/techniques/T1499/)<br>[https://attack.mitre.org/techniques/T1499/003/](https://attack.mitre.org/techniques/T1499/003/)<br>[https://attack.mitre.org/techniques/T1565/](https://attack.mitre.org/techniques/T1565/)<br>[https://attack.mitre.org/techniques/T1565/002/](https://attack.mitre.org/techniques/T1565/002/) |

## Resumo estatístico por nível

| Nível | Serviço | Runs | Amostras attack | Sucesso médio | Falha média | Lat p50/p95 ms | PCAP total MB | Dataset médio (min-max) | Exec média s | Extratores ok/total | CPU média/máx | Mem MB média |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | zenoh | 5 | 200 | 100% | 0% | 0,28 / 0,59 | 0,79 | 3.681 (3.650-3.694) | 42,58 | 3/3 | 0,12% / 0,16% | 5,42 |
| L1 | zenoh | 5 | 200 | 100% | 0% | 0,26 / 0,49 | 1.874,17 | 10.977.814 (10.791.630-11.194.890) | 1.628,15 | 3/3 | 0,11% / 0,15% | 5,41 |
| L2 | zenoh | 5 | 200 | 100% | 0% | 0,26 / 0,5 | 1.867,2 | 10.937.272 (10.898.274-10.988.144) | 1.604,12 | 3/3 | 0,12% / 0,18% | 5,42 |
| L3 | zenoh | 5 | 200 | 100% | 0% | 0,26 / 0,47 | 1.801,32 | 10.553.527 (9.116.110-11.171.668) | 1.548,23 | 3/3 | 0,12% / 0,17% | 5,43 |

## Estabilidade entre reexecuções

| Nível | Métrica | Runs | Média | Desvio | CV | Min | Max |
| --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | CPU média na fase attack | 5 | 0,12 | 0,01 | 6,01% | 0,11 | 0,13 |
| L0 | Linhas do dataset | 5 | 3.680,8 | 18,74 | 0,51% | 3.650 | 3.694 |
| L0 | Tempo de execução | 5 | 42,58 | 0,35 | 0,83% | 42,33 | 43,19 |
| L0 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L0 | Latência p95 censurada | 5 | 0,59 | 0,06 | 10,92% | 0,5 | 0,69 |
| L1 | CPU média na fase attack | 5 | 0,11 | 0,01 | 8,76% | 0,1 | 0,12 |
| L1 | Linhas do dataset | 5 | 10.977.814 | 169.681,96 | 1,55% | 10.791.630 | 11.194.890 |
| L1 | Tempo de execução | 5 | 1.628,15 | 18,74 | 1,15% | 1.609,89 | 1.650,98 |
| L1 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L1 | Latência p95 censurada | 5 | 0,49 | 0,11 | 21,5% | 0,35 | 0,61 |
| L2 | CPU média na fase attack | 5 | 0,12 | 0,01 | 5,67% | 0,11 | 0,13 |
| L2 | Linhas do dataset | 5 | 10.937.272 | 43.110,44 | 0,39% | 10.898.274 | 10.988.144 |
| L2 | Tempo de execução | 5 | 1.604,12 | 15,1 | 0,94% | 1.579,13 | 1.617,72 |
| L2 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L2 | Latência p95 censurada | 5 | 0,5 | 0,05 | 10,07% | 0,42 | 0,55 |
| L3 | CPU média na fase attack | 5 | 0,12 | 0,01 | 6,08% | 0,11 | 0,13 |
| L3 | Linhas do dataset | 5 | 10.553.527,2 | 832.692,5 | 7,89% | 9.116.110 | 11.171.668 |
| L3 | Tempo de execução | 5 | 1.548,23 | 112,19 | 7,25% | 1.355,48 | 1.641,99 |
| L3 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L3 | Latência p95 censurada | 5 | 0,47 | 0,08 | 16,92% | 0,33 | 0,53 |

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
<td><img src="../../assets/campaign_doc/iot_zenoh_pico_sequence_exhaustion/F3_v1_timeseries_zenoh_iot_zenoh_pico_sequence_exhaustion_L0_run01.png" alt="Série temporal L0 run01" width="420"><br><sub>Série temporal L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/iot_zenoh_pico_sequence_exhaustion/F3_v1_timeseries_zenoh_iot_zenoh_pico_sequence_exhaustion_L1_run01.png" alt="Série temporal L1 run01" width="420"><br><sub>Série temporal L1 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/iot_zenoh_pico_sequence_exhaustion/F3_v1_timeseries_zenoh_iot_zenoh_pico_sequence_exhaustion_L2_run01.png" alt="Série temporal L2 run01" width="420"><br><sub>Série temporal L2 run01</sub></td>
<td><img src="../../assets/campaign_doc/iot_zenoh_pico_sequence_exhaustion/F3_v1_timeseries_zenoh_iot_zenoh_pico_sequence_exhaustion_L3_run01.png" alt="Série temporal L3 run01" width="420"><br><sub>Série temporal L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/iot_zenoh_pico_sequence_exhaustion/F5_resources_zenoh_iot_zenoh_pico_sequence_exhaustion_L0_run01.png" alt="Recursos L0 run01" width="420"><br><sub>Recursos L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/iot_zenoh_pico_sequence_exhaustion/F5_resources_zenoh_iot_zenoh_pico_sequence_exhaustion_L3_run01.png" alt="Recursos L3 run01" width="420"><br><sub>Recursos L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/iot_zenoh_pico_sequence_exhaustion/F4_v2_failrate_zenoh_iot_zenoh_pico_sequence_exhaustion_L0.png" alt="Taxa de falha L0" width="420"><br><sub>Taxa de falha L0</sub></td>
<td><img src="../../assets/campaign_doc/iot_zenoh_pico_sequence_exhaustion/F4_v2_failrate_zenoh_iot_zenoh_pico_sequence_exhaustion_L3.png" alt="Taxa de falha L3" width="420"><br><sub>Taxa de falha L3</sub></td>
</tr>
</table>

## Fontes utilizadas

- Catálogo do ataque: `docker/attackers/zenoh-pico-sequence-exhaustion/attack.yaml`
- Artefatos da campanha: `experiments/60att_5runs_l0l1l2l3/iot_zenoh_pico_sequence_exhaustion`
