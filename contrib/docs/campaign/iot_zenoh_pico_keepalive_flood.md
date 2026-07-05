# Zenoh-Pico Keepalive Flood (`iot_zenoh_pico_keepalive_flood`)

[Índice da campanha](README.md)

Na campanha `experiments/60att_5runs_l0l1l2l3`, este documento consolida a execução do ataque `iot_zenoh_pico_keepalive_flood`. No catálogo local, o ataque é descrito como: Flood of Zenoh/Zenoh-Pico keepalive messages to consume processing and session-handling capacity. A documentação abaixo usa apenas artefatos já presentes no repositório, principalmente as tabelas e figuras de `experiments/60att_5runs_l0l1l2l3/iot_zenoh_pico_keepalive_flood`.

## Metadados do ataque

| Campo | Valor |
| --- | --- |
| ID | `iot_zenoh_pico_keepalive_flood` |
| Categoria | 7) IoT |
| Subcategoria | 7.1 IoT Protocols / Zenoh |
| Serviços alvo | zenoh-router |
| Imagem | `attack-zenoh-pico-keepalive-flood:latest` |
| Container | `attack-zenoh-pico-keepalive-flood` |
| Runtime máximo do catálogo | 10 s |
| Parâmetros de intensidade | duration_s, threads |
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0040/](https://attack.mitre.org/tactics/TA0040/)<br>[https://attack.mitre.org/techniques/T1498/](https://attack.mitre.org/techniques/T1498/)<br>[https://attack.mitre.org/techniques/T1498/001/](https://attack.mitre.org/techniques/T1498/001/)<br>[https://attack.mitre.org/techniques/T1499/](https://attack.mitre.org/techniques/T1499/)<br>[https://attack.mitre.org/techniques/T1499/002/](https://attack.mitre.org/techniques/T1499/002/) |

## Resumo estatístico por nível

| Nível | Serviço | Runs | Amostras attack | Sucesso médio | Falha média | Lat p50/p95 ms | PCAP total MB | Dataset médio (min-max) | Exec média s | Extratores ok/total | CPU média/máx | Mem MB média |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | zenoh | 5 | 200 | 100% | 0% | 0,28 / 0,47 | 0,79 | 3.665 (3.646-3.680) | 42,48 | 3/3 | 0,12% / 0,16% | 5,45 |
| L1 | zenoh | 5 | 200 | 100% | 0% | 0,25 / 0,45 | 831,04 | 5.361.131 (4.288.772-6.141.316) | 822,58 | 3/3 | 0,1% / 0,15% | 5,45 |
| L2 | zenoh | 5 | 200 | 100% | 0% | 0,22 / 0,46 | 817,88 | 5.276.194 (3.647.092-5.944.726) | 808,42 | 3/3 | 0,1% / 0,13% | 5,44 |
| L3 | zenoh | 5 | 199 | 100% | 0% | 0,25 / 0,52 | 789 | 5.089.792 (3.864.286-6.098.366) | 781,36 | 3/3 | 0,12% / 0,16% | 5,43 |

## Estabilidade entre reexecuções

| Nível | Métrica | Runs | Média | Desvio | CV | Min | Max |
| --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | CPU média na fase attack | 5 | 0,12 | 0,01 | 8,63% | 0,1 | 0,13 |
| L0 | Linhas do dataset | 5 | 3.664,8 | 17,3 | 0,47% | 3.646 | 3.680 |
| L0 | Tempo de execução | 5 | 42,48 | 0,38 | 0,88% | 42,25 | 43,14 |
| L0 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L0 | Latência p95 censurada | 5 | 0,47 | 0,05 | 11,03% | 0,39 | 0,51 |
| L1 | CPU média na fase attack | 5 | 0,1 | 0,01 | 7,31% | 0,09 | 0,11 |
| L1 | Linhas do dataset | 5 | 5.361.130,8 | 918.554,86 | 17,13% | 4.288.772 | 6.141.316 |
| L1 | Tempo de execução | 5 | 822,58 | 133,73 | 16,26% | 670,64 | 932,65 |
| L1 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L1 | Latência p95 censurada | 5 | 0,45 | 0,06 | 13,73% | 0,36 | 0,51 |
| L2 | CPU média na fase attack | 5 | 0,1 | 0,01 | 7,85% | 0,1 | 0,12 |
| L2 | Linhas do dataset | 5 | 5.276.194,4 | 997.634,65 | 18,91% | 3.647.092 | 5.944.726 |
| L2 | Tempo de execução | 5 | 808,42 | 147,59 | 18,26% | 567,79 | 909,01 |
| L2 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L2 | Latência p95 censurada | 5 | 0,46 | 0,1 | 21,3% | 0,3 | 0,52 |
| L3 | CPU média na fase attack | 5 | 0,12 | 0,01 | 9,4% | 0,11 | 0,13 |
| L3 | Linhas do dataset | 5 | 5.089.792,4 | 927.874,47 | 18,23% | 3.864.286 | 6.098.366 |
| L3 | Tempo de execução | 5 | 781,36 | 135,14 | 17,3% | 604,09 | 931,15 |
| L3 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L3 | Latência p95 censurada | 5 | 0,52 | 0,03 | 6,36% | 0,46 | 0,55 |

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
<td><img src="../../assets/campaign_doc/iot_zenoh_pico_keepalive_flood/F3_v1_timeseries_zenoh_iot_zenoh_pico_keepalive_flood_L0_run01.png" alt="Série temporal L0 run01" width="420"><br><sub>Série temporal L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/iot_zenoh_pico_keepalive_flood/F3_v1_timeseries_zenoh_iot_zenoh_pico_keepalive_flood_L1_run01.png" alt="Série temporal L1 run01" width="420"><br><sub>Série temporal L1 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/iot_zenoh_pico_keepalive_flood/F3_v1_timeseries_zenoh_iot_zenoh_pico_keepalive_flood_L2_run01.png" alt="Série temporal L2 run01" width="420"><br><sub>Série temporal L2 run01</sub></td>
<td><img src="../../assets/campaign_doc/iot_zenoh_pico_keepalive_flood/F3_v1_timeseries_zenoh_iot_zenoh_pico_keepalive_flood_L3_run01.png" alt="Série temporal L3 run01" width="420"><br><sub>Série temporal L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/iot_zenoh_pico_keepalive_flood/F5_resources_zenoh_iot_zenoh_pico_keepalive_flood_L0_run01.png" alt="Recursos L0 run01" width="420"><br><sub>Recursos L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/iot_zenoh_pico_keepalive_flood/F5_resources_zenoh_iot_zenoh_pico_keepalive_flood_L3_run01.png" alt="Recursos L3 run01" width="420"><br><sub>Recursos L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/iot_zenoh_pico_keepalive_flood/F4_v2_failrate_zenoh_iot_zenoh_pico_keepalive_flood_L0.png" alt="Taxa de falha L0" width="420"><br><sub>Taxa de falha L0</sub></td>
<td><img src="../../assets/campaign_doc/iot_zenoh_pico_keepalive_flood/F4_v2_failrate_zenoh_iot_zenoh_pico_keepalive_flood_L3.png" alt="Taxa de falha L3" width="420"><br><sub>Taxa de falha L3</sub></td>
</tr>
</table>

## Fontes utilizadas

- Catálogo do ataque: `docker/attackers/zenoh-pico-keepalive-flood/attack.yaml`
- Artefatos da campanha: `experiments/60att_5runs_l0l1l2l3/iot_zenoh_pico_keepalive_flood`
