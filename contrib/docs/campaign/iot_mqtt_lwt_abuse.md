# MQTT LWT Abuse (`iot_mqtt_lwt_abuse`)

[Índice da campanha](README.md)

Na campanha `experiments/60att_5runs_l0l1l2l3`, este documento consolida a execução do ataque `iot_mqtt_lwt_abuse`. No catálogo local, o ataque é descrito como: Abuse of the MQTT Last Will and Testament mechanism to force critical publications or false alarms on sensitive topics. A documentação abaixo usa apenas artefatos já presentes no repositório, principalmente as tabelas e figuras de `experiments/60att_5runs_l0l1l2l3/iot_mqtt_lwt_abuse`.

## Metadados do ataque

| Campo | Valor |
| --- | --- |
| ID | `iot_mqtt_lwt_abuse` |
| Categoria | 7) IoT |
| Subcategoria | 7.1 IoT Protocols / MQTT |
| Serviços alvo | mqtt-broker |
| Imagem | `attack-mqtt-lwt-abuse:latest` |
| Container | `attack-mqtt-lwt-abuse` |
| Runtime máximo do catálogo | 10 s |
| Parâmetros de intensidade | count, delay_ms |
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0040/](https://attack.mitre.org/tactics/TA0040/)<br>[https://attack.mitre.org/techniques/T1565/](https://attack.mitre.org/techniques/T1565/)<br>[https://attack.mitre.org/techniques/T1565/001/](https://attack.mitre.org/techniques/T1565/001/)<br>[https://attack.mitre.org/techniques/T1565/002/](https://attack.mitre.org/techniques/T1565/002/) |

## Resumo estatístico por nível

| Nível | Serviço | Runs | Amostras attack | Sucesso médio | Falha média | Lat p50/p95 ms | PCAP total MB | Dataset médio (min-max) | Exec média s | Extratores ok/total | CPU média/máx | Mem MB média |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | mqtt | 5 | 200 | 0% | 100% | 2.000 / 2.000 | 1,05 | 4.768 (4.760-4.778) | 42,48 | 3/3 | 0,08% / 0,09% | 5,18 |
| L1 | mqtt | 5 | 200 | 0% | 100% | 2.000 / 2.000 | 1,57 | 6.938 (6.890-6.974) | 42,61 | 3/3 | 0,13% / 0,19% | 5,2 |
| L2 | mqtt | 5 | 200 | 0% | 100% | 2.000 / 2.000 | 1,57 | 6.951 (6.944-6.968) | 42,68 | 3/3 | 0,14% / 0,21% | 5,2 |
| L3 | mqtt | 5 | 200 | 0% | 100% | 2.000 / 2.000 | 1,57 | 6.942 (6.930-6.954) | 42,65 | 3/3 | 0,13% / 0,16% | 5,2 |

## Estabilidade entre reexecuções

| Nível | Métrica | Runs | Média | Desvio | CV | Min | Max |
| --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | CPU média na fase attack | 5 | 0,08 | 0 | 5,08% | 0,07 | 0,08 |
| L0 | Linhas do dataset | 5 | 4.768,4 | 6,99 | 0,15% | 4.760 | 4.778 |
| L0 | Tempo de execução | 5 | 42,48 | 0,35 | 0,83% | 42,25 | 43,1 |
| L0 | Falha na fase attack | 5 | 100 | 0 | 0% | 100 | 100 |
| L0 | Latência p95 censurada | 5 | 2.000 | 0 | 0% | 2.000 | 2.000 |
| L1 | CPU média na fase attack | 5 | 0,13 | 0,02 | 17,34% | 0,11 | 0,16 |
| L1 | Linhas do dataset | 5 | 6.938 | 30,89 | 0,45% | 6.890 | 6.974 |
| L1 | Tempo de execução | 5 | 42,61 | 0,07 | 0,17% | 42,51 | 42,72 |
| L1 | Falha na fase attack | 5 | 100 | 0 | 0% | 100 | 100 |
| L1 | Latência p95 censurada | 5 | 2.000 | 0 | 0% | 2.000 | 2.000 |
| L2 | CPU média na fase attack | 5 | 0,14 | 0,02 | 15,26% | 0,12 | 0,17 |
| L2 | Linhas do dataset | 5 | 6.951,2 | 10,26 | 0,15% | 6.944 | 6.968 |
| L2 | Tempo de execução | 5 | 42,68 | 0,07 | 0,15% | 42,57 | 42,74 |
| L2 | Falha na fase attack | 5 | 100 | 0 | 0% | 100 | 100 |
| L2 | Latência p95 censurada | 5 | 2.000 | 0 | 0% | 2.000 | 2.000 |
| L3 | CPU média na fase attack | 5 | 0,13 | 0,02 | 15,48% | 0,11 | 0,16 |
| L3 | Linhas do dataset | 5 | 6.942,4 | 10,24 | 0,15% | 6.930 | 6.954 |
| L3 | Tempo de execução | 5 | 42,65 | 0,12 | 0,27% | 42,49 | 42,8 |
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
<td><img src="../../assets/campaign_doc/iot_mqtt_lwt_abuse/F3_v1_timeseries_mqtt_iot_mqtt_lwt_abuse_L0_run01.png" alt="Série temporal L0 run01" width="420"><br><sub>Série temporal L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/iot_mqtt_lwt_abuse/F3_v1_timeseries_mqtt_iot_mqtt_lwt_abuse_L1_run01.png" alt="Série temporal L1 run01" width="420"><br><sub>Série temporal L1 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/iot_mqtt_lwt_abuse/F3_v1_timeseries_mqtt_iot_mqtt_lwt_abuse_L2_run01.png" alt="Série temporal L2 run01" width="420"><br><sub>Série temporal L2 run01</sub></td>
<td><img src="../../assets/campaign_doc/iot_mqtt_lwt_abuse/F3_v1_timeseries_mqtt_iot_mqtt_lwt_abuse_L3_run01.png" alt="Série temporal L3 run01" width="420"><br><sub>Série temporal L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/iot_mqtt_lwt_abuse/F5_resources_mqtt_iot_mqtt_lwt_abuse_L0_run01.png" alt="Recursos L0 run01" width="420"><br><sub>Recursos L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/iot_mqtt_lwt_abuse/F5_resources_mqtt_iot_mqtt_lwt_abuse_L3_run01.png" alt="Recursos L3 run01" width="420"><br><sub>Recursos L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/iot_mqtt_lwt_abuse/F4_v2_failrate_mqtt_iot_mqtt_lwt_abuse_L0.png" alt="Taxa de falha L0" width="420"><br><sub>Taxa de falha L0</sub></td>
<td><img src="../../assets/campaign_doc/iot_mqtt_lwt_abuse/F4_v2_failrate_mqtt_iot_mqtt_lwt_abuse_L3.png" alt="Taxa de falha L3" width="420"><br><sub>Taxa de falha L3</sub></td>
</tr>
</table>

## Fontes utilizadas

- Catálogo do ataque: `docker/attackers/mqtt-lwt-abuse/attack.yaml`
- Artefatos da campanha: `experiments/60att_5runs_l0l1l2l3/iot_mqtt_lwt_abuse`
