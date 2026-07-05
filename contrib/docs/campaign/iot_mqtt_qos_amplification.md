# MQTT QoS 2 Amplification (`iot_mqtt_qos_amplification`)

[Índice da campanha](README.md)

Na campanha `experiments/60att_5runs_l0l1l2l3`, este documento consolida a execução do ataque `iot_mqtt_qos_amplification`. No catálogo local, o ataque é descrito como: Traffic and state-load amplification on the MQTT broker through multiple QoS 2 handshakes. A documentação abaixo usa apenas artefatos já presentes no repositório, principalmente as tabelas e figuras de `experiments/60att_5runs_l0l1l2l3/iot_mqtt_qos_amplification`.

## Metadados do ataque

| Campo | Valor |
| --- | --- |
| ID | `iot_mqtt_qos_amplification` |
| Categoria | 7) IoT |
| Subcategoria | 7.1 IoT Protocols / MQTT |
| Serviços alvo | mqtt-broker |
| Imagem | `attack-mqtt-qos-amplification:latest` |
| Container | `attack-mqtt-qos-amplification` |
| Runtime máximo do catálogo | 10 s |
| Parâmetros de intensidade | threads, count, delay_ms |
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0040/](https://attack.mitre.org/tactics/TA0040/)<br>[https://attack.mitre.org/techniques/T1499/](https://attack.mitre.org/techniques/T1499/)<br>[https://attack.mitre.org/techniques/T1499/003/](https://attack.mitre.org/techniques/T1499/003/) |

## Resumo estatístico por nível

| Nível | Serviço | Runs | Amostras attack | Sucesso médio | Falha média | Lat p50/p95 ms | PCAP total MB | Dataset médio (min-max) | Exec média s | Extratores ok/total | CPU média/máx | Mem MB média |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | mqtt | 5 | 200 | 0% | 100% | 2.000 / 2.000 | 1,06 | 4.775 (4.760-4.814) | 42,41 | 3/3 | 0,08% / 0,09% | 5,27 |
| L1 | mqtt | 5 | 200 | 0% | 100% | 2.000 / 2.000 | 20,73 | 82.533 (77.952-88.974) | 52,38 | 3/3 | 1,1% / 1,24% | 5,48 |
| L2 | mqtt | 5 | 200 | 0% | 100% | 2.000 / 2.000 | 20,98 | 83.498 (78.242-86.070) | 52,41 | 3/3 | 1,11% / 1,28% | 5,48 |
| L3 | mqtt | 5 | 200 | 0% | 100% | 2.000 / 2.000 | 20,95 | 83.388 (76.100-88.590) | 52,32 | 3/3 | 1,09% / 1,26% | 5,51 |

## Estabilidade entre reexecuções

| Nível | Métrica | Runs | Média | Desvio | CV | Min | Max |
| --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | CPU média na fase attack | 5 | 0,08 | 0 | 3,59% | 0,08 | 0,08 |
| L0 | Linhas do dataset | 5 | 4.775,2 | 22,03 | 0,46% | 4.760 | 4.814 |
| L0 | Tempo de execução | 5 | 42,41 | 0,35 | 0,83% | 42,2 | 43,04 |
| L0 | Falha na fase attack | 5 | 100 | 0 | 0% | 100 | 100 |
| L0 | Latência p95 censurada | 5 | 2.000 | 0 | 0% | 2.000 | 2.000 |
| L1 | CPU média na fase attack | 5 | 1,1 | 0,05 | 4,35% | 1,04 | 1,16 |
| L1 | Linhas do dataset | 5 | 82.533,2 | 5.297,56 | 6,42% | 77.952 | 88.974 |
| L1 | Tempo de execução | 5 | 52,38 | 0,7 | 1,34% | 51,75 | 53,19 |
| L1 | Falha na fase attack | 5 | 100 | 0 | 0% | 100 | 100 |
| L1 | Latência p95 censurada | 5 | 2.000 | 0 | 0% | 2.000 | 2.000 |
| L2 | CPU média na fase attack | 5 | 1,11 | 0,02 | 2,08% | 1,08 | 1,14 |
| L2 | Linhas do dataset | 5 | 83.497,6 | 3.087,03 | 3,7% | 78.242 | 86.070 |
| L2 | Tempo de execução | 5 | 52,41 | 0,34 | 0,64% | 51,84 | 52,71 |
| L2 | Falha na fase attack | 5 | 100 | 0 | 0% | 100 | 100 |
| L2 | Latência p95 censurada | 5 | 2.000 | 0 | 0% | 2.000 | 2.000 |
| L3 | CPU média na fase attack | 5 | 1,09 | 0,08 | 7,43% | 0,98 | 1,18 |
| L3 | Linhas do dataset | 5 | 83.388 | 5.284,58 | 6,34% | 76.100 | 88.590 |
| L3 | Tempo de execução | 5 | 52,32 | 0,75 | 1,44% | 51,29 | 53,18 |
| L3 | Falha na fase attack | 5 | 100 | 0 | 0% | 100 | 100 |
| L3 | Latência p95 censurada | 5 | 2.000 | 0 | 0% | 2.000 | 2.000 |

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
<td><img src="../../assets/campaign_doc/iot_mqtt_qos_amplification/F3_v1_timeseries_mqtt_iot_mqtt_qos_amplification_L0_run01.png" alt="Série temporal L0 run01" width="420"><br><sub>Série temporal L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/iot_mqtt_qos_amplification/F3_v1_timeseries_mqtt_iot_mqtt_qos_amplification_L1_run01.png" alt="Série temporal L1 run01" width="420"><br><sub>Série temporal L1 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/iot_mqtt_qos_amplification/F3_v1_timeseries_mqtt_iot_mqtt_qos_amplification_L2_run01.png" alt="Série temporal L2 run01" width="420"><br><sub>Série temporal L2 run01</sub></td>
<td><img src="../../assets/campaign_doc/iot_mqtt_qos_amplification/F3_v1_timeseries_mqtt_iot_mqtt_qos_amplification_L3_run01.png" alt="Série temporal L3 run01" width="420"><br><sub>Série temporal L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/iot_mqtt_qos_amplification/F5_resources_mqtt_iot_mqtt_qos_amplification_L0_run01.png" alt="Recursos L0 run01" width="420"><br><sub>Recursos L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/iot_mqtt_qos_amplification/F5_resources_mqtt_iot_mqtt_qos_amplification_L3_run01.png" alt="Recursos L3 run01" width="420"><br><sub>Recursos L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/iot_mqtt_qos_amplification/F4_v2_failrate_mqtt_iot_mqtt_qos_amplification_L0.png" alt="Taxa de falha L0" width="420"><br><sub>Taxa de falha L0</sub></td>
<td><img src="../../assets/campaign_doc/iot_mqtt_qos_amplification/F4_v2_failrate_mqtt_iot_mqtt_qos_amplification_L3.png" alt="Taxa de falha L3" width="420"><br><sub>Taxa de falha L3</sub></td>
</tr>
</table>

## Fontes utilizadas

- Catálogo do ataque: `docker/attackers/mqtt-qos-amplification/attack.yaml`
- Artefatos da campanha: `experiments/60att_5runs_l0l1l2l3/iot_mqtt_qos_amplification`
