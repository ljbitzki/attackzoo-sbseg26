# MQTT Publisher Flood (`iot_mqtt_publisher`)

[Índice da campanha](README.md)

Na campanha `experiments/60att_5runs_l0l1l2l3`, este documento consolida a execução do ataque `iot_mqtt_publisher`. No catálogo local, o ataque é descrito como: MQTT publish flood to evaluate broker availability and behavior under load. A documentação abaixo usa apenas artefatos já presentes no repositório, principalmente as tabelas e figuras de `experiments/60att_5runs_l0l1l2l3/iot_mqtt_publisher`.

## Metadados do ataque

| Campo | Valor |
| --- | --- |
| ID | `iot_mqtt_publisher` |
| Categoria | 7) IoT |
| Subcategoria | 7.1 IoT Protocols / MQTT |
| Serviços alvo | mqtt-broker |
| Imagem | `attack-mqtt-publisher:latest` |
| Container | `attack-mqtt-publisher` |
| Runtime máximo do catálogo | 10 s |
| Parâmetros de intensidade | count, delay_ms, payload_size |
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0040/](https://attack.mitre.org/tactics/TA0040/)<br>[https://attack.mitre.org/techniques/T1499/](https://attack.mitre.org/techniques/T1499/)<br>[https://attack.mitre.org/techniques/T1499/002/](https://attack.mitre.org/techniques/T1499/002/) |

## Resumo estatístico por nível

| Nível | Serviço | Runs | Amostras attack | Sucesso médio | Falha média | Lat p50/p95 ms | PCAP total MB | Dataset médio (min-max) | Exec média s | Extratores ok/total | CPU média/máx | Mem MB média |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | mqtt | 5 | 200 | 0% | 100% | 2.000 / 2.000 | 1,06 | 4.778 (4.766-4.788) | 42,52 | 3/3 | 0,09% / 0,12% | 5,2 |
| L1 | mqtt | 5 | 200 | 0% | 100% | 2.000 / 2.000 | 14,28 | 64.859 (64.778-65.002) | 49,89 | 3/3 | 0,88% / 4,39% | 5,22 |
| L2 | mqtt | 5 | 200 | 0% | 100% | 2.000 / 2.000 | 14,28 | 64.870 (64.858-64.886) | 49,9 | 3/3 | 0,83% / 4,72% | 5,25 |
| L3 | mqtt | 5 | 200 | 0% | 100% | 2.000 / 2.000 | 14,28 | 64.884 (64.846-64.924) | 49,94 | 3/3 | 0,81% / 5,4% | 5,27 |

## Estabilidade entre reexecuções

| Nível | Métrica | Runs | Média | Desvio | CV | Min | Max |
| --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | CPU média na fase attack | 5 | 0,09 | 0,01 | 14,37% | 0,07 | 0,1 |
| L0 | Linhas do dataset | 5 | 4.777,6 | 8,65 | 0,18% | 4.766 | 4.788 |
| L0 | Tempo de execução | 5 | 42,52 | 0,33 | 0,77% | 42,32 | 43,1 |
| L0 | Falha na fase attack | 5 | 100 | 0 | 0% | 100 | 100 |
| L0 | Latência p95 censurada | 5 | 2.000 | 0 | 0% | 2.000 | 2.000 |
| L1 | CPU média na fase attack | 5 | 0,88 | 0,09 | 10,19% | 0,77 | 0,96 |
| L1 | Linhas do dataset | 5 | 64.858,8 | 87,56 | 0,14% | 64.778 | 65.002 |
| L1 | Tempo de execução | 5 | 49,89 | 0,13 | 0,27% | 49,66 | 49,97 |
| L1 | Falha na fase attack | 5 | 100 | 0 | 0% | 100 | 100 |
| L1 | Latência p95 censurada | 5 | 2.000 | 0 | 0% | 2.000 | 2.000 |
| L2 | CPU média na fase attack | 5 | 0,83 | 0,05 | 5,95% | 0,77 | 0,89 |
| L2 | Linhas do dataset | 5 | 64.870,4 | 11,35 | 0,02% | 64.858 | 64.886 |
| L2 | Tempo de execução | 5 | 49,9 | 0,06 | 0,12% | 49,83 | 49,99 |
| L2 | Falha na fase attack | 5 | 100 | 0 | 0% | 100 | 100 |
| L2 | Latência p95 censurada | 5 | 2.000 | 0 | 0% | 2.000 | 2.000 |
| L3 | CPU média na fase attack | 5 | 0,81 | 0,04 | 4,82% | 0,77 | 0,86 |
| L3 | Linhas do dataset | 5 | 64.883,6 | 36,75 | 0,06% | 64.846 | 64.924 |
| L3 | Tempo de execução | 5 | 49,94 | 0,12 | 0,24% | 49,82 | 50,07 |
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
<td><img src="../../assets/campaign_doc/iot_mqtt_publisher/F3_v1_timeseries_mqtt_iot_mqtt_publisher_L0_run01.png" alt="Série temporal L0 run01" width="420"><br><sub>Série temporal L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/iot_mqtt_publisher/F3_v1_timeseries_mqtt_iot_mqtt_publisher_L1_run01.png" alt="Série temporal L1 run01" width="420"><br><sub>Série temporal L1 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/iot_mqtt_publisher/F3_v1_timeseries_mqtt_iot_mqtt_publisher_L2_run01.png" alt="Série temporal L2 run01" width="420"><br><sub>Série temporal L2 run01</sub></td>
<td><img src="../../assets/campaign_doc/iot_mqtt_publisher/F3_v1_timeseries_mqtt_iot_mqtt_publisher_L3_run01.png" alt="Série temporal L3 run01" width="420"><br><sub>Série temporal L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/iot_mqtt_publisher/F5_resources_mqtt_iot_mqtt_publisher_L0_run01.png" alt="Recursos L0 run01" width="420"><br><sub>Recursos L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/iot_mqtt_publisher/F5_resources_mqtt_iot_mqtt_publisher_L3_run01.png" alt="Recursos L3 run01" width="420"><br><sub>Recursos L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/iot_mqtt_publisher/F4_v2_failrate_mqtt_iot_mqtt_publisher_L0.png" alt="Taxa de falha L0" width="420"><br><sub>Taxa de falha L0</sub></td>
<td><img src="../../assets/campaign_doc/iot_mqtt_publisher/F4_v2_failrate_mqtt_iot_mqtt_publisher_L3.png" alt="Taxa de falha L3" width="420"><br><sub>Taxa de falha L3</sub></td>
</tr>
</table>

## Fontes utilizadas

- Catálogo do ataque: `docker/attackers/mqtt-publisher-flood/attack.yaml`
- Artefatos da campanha: `experiments/60att_5runs_l0l1l2l3/iot_mqtt_publisher`
