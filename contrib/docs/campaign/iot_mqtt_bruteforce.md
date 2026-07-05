# MQTT Bruteforce (`iot_mqtt_bruteforce`)

[Índice da campanha](README.md)

Na campanha `experiments/60att_5runs_l0l1l2l3`, este documento consolida a execução do ataque `iot_mqtt_bruteforce`. No catálogo local, o ataque é descrito como: MQTT authentication brute force against the target broker using a controlled wordlist. A documentação abaixo usa apenas artefatos já presentes no repositório, principalmente as tabelas e figuras de `experiments/60att_5runs_l0l1l2l3/iot_mqtt_bruteforce`.

## Metadados do ataque

| Campo | Valor |
| --- | --- |
| ID | `iot_mqtt_bruteforce` |
| Categoria | 7) IoT |
| Subcategoria | 7.1 IoT Protocols / MQTT |
| Serviços alvo | mqtt-broker |
| Imagem | `attack-mqtt-bruteforce:latest` |
| Container | `attack-mqtt-bruteforce` |
| Runtime máximo do catálogo | 10 s |
| Parâmetros de intensidade | n/d |
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0006/](https://attack.mitre.org/tactics/TA0006/)<br>[https://attack.mitre.org/techniques/T1110/](https://attack.mitre.org/techniques/T1110/)<br>[https://attack.mitre.org/techniques/T1110/001/](https://attack.mitre.org/techniques/T1110/001/) |

## Resumo estatístico por nível

| Nível | Serviço | Runs | Amostras attack | Sucesso médio | Falha média | Lat p50/p95 ms | PCAP total MB | Dataset médio (min-max) | Exec média s | Extratores ok/total | CPU média/máx | Mem MB média |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | mqtt | 5 | 200 | 0% | 100% | 2.000 / 2.000 | 1,05 | 4.770 (4.768-4.772) | 42,67 | 3/3 | 0,1% / 0,12% | 1,66 |
| L1 | mqtt | 5 | 200 | 0% | 100% | 2.000 / 2.000 | 4,41 | 19.897 (19.892-19.904) | 44,35 | 3/3 | 0,41% / 3,09% | 5,08 |
| L2 | mqtt | 5 | 200 | 0% | 100% | 2.000 / 2.000 | 4,4 | 19.888 (19.874-19.908) | 44,21 | 3/3 | 0,36% / 2,88% | 5,17 |
| L3 | mqtt | 5 | 200 | 0% | 100% | 2.000 / 2.000 | 4,41 | 19.895 (19.890-19.904) | 44,28 | 3/3 | 0,45% / 3,71% | 5,18 |

## Estabilidade entre reexecuções

| Nível | Métrica | Runs | Média | Desvio | CV | Min | Max |
| --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | CPU média na fase attack | 5 | 0,1 | 0,01 | 5,58% | 0,09 | 0,11 |
| L0 | Linhas do dataset | 5 | 4.770,4 | 1,67 | 0,04% | 4.768 | 4.772 |
| L0 | Tempo de execução | 5 | 42,67 | 0,58 | 1,35% | 42,36 | 43,7 |
| L0 | Falha na fase attack | 5 | 100 | 0 | 0% | 100 | 100 |
| L0 | Latência p95 censurada | 5 | 2.000 | 0 | 0% | 2.000 | 2.000 |
| L1 | CPU média na fase attack | 5 | 0,41 | 0,16 | 38,38% | 0,15 | 0,53 |
| L1 | Linhas do dataset | 5 | 19.896,8 | 5,22 | 0,03% | 19.892 | 19.904 |
| L1 | Tempo de execução | 5 | 44,35 | 0,13 | 0,29% | 44,17 | 44,49 |
| L1 | Falha na fase attack | 5 | 100 | 0 | 0% | 100 | 100 |
| L1 | Latência p95 censurada | 5 | 2.000 | 0 | 0% | 2.000 | 2.000 |
| L2 | CPU média na fase attack | 5 | 0,36 | 0,12 | 34,68% | 0,14 | 0,42 |
| L2 | Linhas do dataset | 5 | 19.887,6 | 14,79 | 0,07% | 19.874 | 19.908 |
| L2 | Tempo de execução | 5 | 44,21 | 0,07 | 0,15% | 44,12 | 44,29 |
| L2 | Falha na fase attack | 5 | 100 | 0 | 0% | 100 | 100 |
| L2 | Latência p95 censurada | 5 | 2.000 | 0 | 0% | 2.000 | 2.000 |
| L3 | CPU média na fase attack | 5 | 0,45 | 0,02 | 4,75% | 0,43 | 0,48 |
| L3 | Linhas do dataset | 5 | 19.895,2 | 5,76 | 0,03% | 19.890 | 19.904 |
| L3 | Tempo de execução | 5 | 44,28 | 0,04 | 0,09% | 44,23 | 44,32 |
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
<td><img src="../../assets/campaign_doc/iot_mqtt_bruteforce/F3_v1_timeseries_mqtt_iot_mqtt_bruteforce_L0_run01.png" alt="Série temporal L0 run01" width="420"><br><sub>Série temporal L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/iot_mqtt_bruteforce/F3_v1_timeseries_mqtt_iot_mqtt_bruteforce_L1_run01.png" alt="Série temporal L1 run01" width="420"><br><sub>Série temporal L1 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/iot_mqtt_bruteforce/F3_v1_timeseries_mqtt_iot_mqtt_bruteforce_L2_run01.png" alt="Série temporal L2 run01" width="420"><br><sub>Série temporal L2 run01</sub></td>
<td><img src="../../assets/campaign_doc/iot_mqtt_bruteforce/F3_v1_timeseries_mqtt_iot_mqtt_bruteforce_L3_run01.png" alt="Série temporal L3 run01" width="420"><br><sub>Série temporal L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/iot_mqtt_bruteforce/F5_resources_mqtt_iot_mqtt_bruteforce_L0_run01.png" alt="Recursos L0 run01" width="420"><br><sub>Recursos L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/iot_mqtt_bruteforce/F5_resources_mqtt_iot_mqtt_bruteforce_L3_run01.png" alt="Recursos L3 run01" width="420"><br><sub>Recursos L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/iot_mqtt_bruteforce/F4_v2_failrate_mqtt_iot_mqtt_bruteforce_L0.png" alt="Taxa de falha L0" width="420"><br><sub>Taxa de falha L0</sub></td>
<td><img src="../../assets/campaign_doc/iot_mqtt_bruteforce/F4_v2_failrate_mqtt_iot_mqtt_bruteforce_L3.png" alt="Taxa de falha L3" width="420"><br><sub>Taxa de falha L3</sub></td>
</tr>
</table>

## Fontes utilizadas

- Catálogo do ataque: `docker/attackers/mqtt-bruteforce/attack.yaml`
- Artefatos da campanha: `experiments/60att_5runs_l0l1l2l3/iot_mqtt_bruteforce`
