# Zenoh-Pico Protocol Fuzzer (`iot_zenoh_pico_proto_fuzzer`)

[Índice da campanha](README.md)

Na campanha `experiments/60att_5runs_l0l1l2l3`, este documento consolida a execução do ataque `iot_zenoh_pico_proto_fuzzer`. No catálogo local, o ataque é descrito como: Sending malformed or mutated Zenoh/Zenoh-Pico messages to trigger errors, exceptions, or crashes on the target. A documentação abaixo usa apenas artefatos já presentes no repositório, principalmente as tabelas e figuras de `experiments/60att_5runs_l0l1l2l3/iot_zenoh_pico_proto_fuzzer`.

## Metadados do ataque

| Campo | Valor |
| --- | --- |
| ID | `iot_zenoh_pico_proto_fuzzer` |
| Categoria | 7) IoT |
| Subcategoria | 7.1 IoT Protocols / Zenoh |
| Serviços alvo | zenoh-router |
| Imagem | `attack-zenoh-pico-proto-fuzzer:latest` |
| Container | `attack-zenoh-pico-proto-fuzzer` |
| Runtime máximo do catálogo | 10 s |
| Parâmetros de intensidade | duration_s, count |
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0043/](https://attack.mitre.org/tactics/TA0043/)<br>[https://attack.mitre.org/tactics/TA0001/](https://attack.mitre.org/tactics/TA0001/)<br>[https://attack.mitre.org/tactics/TA0040/](https://attack.mitre.org/tactics/TA0040/)<br>[https://attack.mitre.org/techniques/T1595/](https://attack.mitre.org/techniques/T1595/)<br>[https://attack.mitre.org/techniques/T1595/002/](https://attack.mitre.org/techniques/T1595/002/)<br>[https://attack.mitre.org/techniques/T1190/](https://attack.mitre.org/techniques/T1190/)<br>[https://attack.mitre.org/techniques/T1499/](https://attack.mitre.org/techniques/T1499/)<br>[https://attack.mitre.org/techniques/T1499/004/](https://attack.mitre.org/techniques/T1499/004/) |

## Resumo estatístico por nível

| Nível | Serviço | Runs | Amostras attack | Sucesso médio | Falha média | Lat p50/p95 ms | PCAP total MB | Dataset médio (min-max) | Exec média s | Extratores ok/total | CPU média/máx | Mem MB média |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | zenoh | 5 | 200 | 100% | 0% | 0,28 / 0,51 | 0,79 | 3.659 (3.644-3.692) | 42,39 | 3/3 | 0,12% / 0,16% | 5,43 |
| L1 | zenoh | 5 | 200 | 100% | 0% | 0,28 / 0,53 | 2,09 | 4.060 (4.022-4.110) | 42,39 | 3/3 | 0,12% / 0,15% | 5,45 |
| L2 | zenoh | 5 | 200 | 100% | 0% | 0,31 / 0,6 | 2,16 | 4.062 (4.046-4.080) | 42,38 | 3/3 | 0,13% / 0,17% | 5,41 |
| L3 | zenoh | 5 | 200 | 100% | 0% | 0,29 / 0,59 | 2,21 | 4.065 (4.056-4.082) | 42,44 | 3/3 | 0,11% / 0,17% | 5,42 |

## Estabilidade entre reexecuções

| Nível | Métrica | Runs | Média | Desvio | CV | Min | Max |
| --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | CPU média na fase attack | 5 | 0,11 | 0,01 | 10,81% | 0,1 | 0,13 |
| L0 | Linhas do dataset | 5 | 3.658,8 | 19,06 | 0,52% | 3.644 | 3.692 |
| L0 | Tempo de execução | 5 | 42,39 | 0,32 | 0,75% | 42,17 | 42,96 |
| L0 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L0 | Latência p95 censurada | 5 | 0,51 | 0,14 | 28,14% | 0,26 | 0,62 |
| L1 | CPU média na fase attack | 5 | 0,12 | 0,02 | 17,21% | 0,1 | 0,15 |
| L1 | Linhas do dataset | 5 | 4.060,4 | 32,69 | 0,81% | 4.022 | 4.110 |
| L1 | Tempo de execução | 5 | 42,39 | 0,04 | 0,09% | 42,32 | 42,42 |
| L1 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L1 | Latência p95 censurada | 5 | 0,53 | 0,1 | 18,07% | 0,37 | 0,62 |
| L2 | CPU média na fase attack | 5 | 0,13 | 0,01 | 10,42% | 0,11 | 0,15 |
| L2 | Linhas do dataset | 5 | 4.062,4 | 14,93 | 0,37% | 4.046 | 4.080 |
| L2 | Tempo de execução | 5 | 42,38 | 0,05 | 0,12% | 42,31 | 42,45 |
| L2 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L2 | Latência p95 censurada | 5 | 0,6 | 0,07 | 12,5% | 0,53 | 0,68 |
| L3 | CPU média na fase attack | 5 | 0,11 | 0,01 | 9,86% | 0,1 | 0,13 |
| L3 | Linhas do dataset | 5 | 4.065,2 | 10,26 | 0,25% | 4.056 | 4.082 |
| L3 | Tempo de execução | 5 | 42,44 | 0,08 | 0,19% | 42,34 | 42,51 |
| L3 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L3 | Latência p95 censurada | 5 | 0,59 | 0,05 | 7,72% | 0,53 | 0,65 |

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
<td><img src="../../assets/campaign_doc/iot_zenoh_pico_proto_fuzzer/F3_v1_timeseries_zenoh_iot_zenoh_pico_proto_fuzzer_L0_run01.png" alt="Série temporal L0 run01" width="420"><br><sub>Série temporal L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/iot_zenoh_pico_proto_fuzzer/F3_v1_timeseries_zenoh_iot_zenoh_pico_proto_fuzzer_L1_run01.png" alt="Série temporal L1 run01" width="420"><br><sub>Série temporal L1 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/iot_zenoh_pico_proto_fuzzer/F3_v1_timeseries_zenoh_iot_zenoh_pico_proto_fuzzer_L2_run01.png" alt="Série temporal L2 run01" width="420"><br><sub>Série temporal L2 run01</sub></td>
<td><img src="../../assets/campaign_doc/iot_zenoh_pico_proto_fuzzer/F3_v1_timeseries_zenoh_iot_zenoh_pico_proto_fuzzer_L3_run01.png" alt="Série temporal L3 run01" width="420"><br><sub>Série temporal L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/iot_zenoh_pico_proto_fuzzer/F5_resources_zenoh_iot_zenoh_pico_proto_fuzzer_L0_run01.png" alt="Recursos L0 run01" width="420"><br><sub>Recursos L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/iot_zenoh_pico_proto_fuzzer/F5_resources_zenoh_iot_zenoh_pico_proto_fuzzer_L3_run01.png" alt="Recursos L3 run01" width="420"><br><sub>Recursos L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/iot_zenoh_pico_proto_fuzzer/F4_v2_failrate_zenoh_iot_zenoh_pico_proto_fuzzer_L0.png" alt="Taxa de falha L0" width="420"><br><sub>Taxa de falha L0</sub></td>
<td><img src="../../assets/campaign_doc/iot_zenoh_pico_proto_fuzzer/F4_v2_failrate_zenoh_iot_zenoh_pico_proto_fuzzer_L3.png" alt="Taxa de falha L3" width="420"><br><sub>Taxa de falha L3</sub></td>
</tr>
</table>

## Fontes utilizadas

- Catálogo do ataque: `docker/attackers/zenoh-pico-proto-fuzzer/attack.yaml`
- Artefatos da campanha: `experiments/60att_5runs_l0l1l2l3/iot_zenoh_pico_proto_fuzzer`
