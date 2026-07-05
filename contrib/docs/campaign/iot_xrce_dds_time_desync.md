# XRCE-DDS Time Desynchronization (`iot_xrce_dds_time_desync`)

[Índice da campanha](README.md)

Na campanha `experiments/60att_5runs_l0l1l2l3`, este documento consolida a execução do ataque `iot_xrce_dds_time_desync`. No catálogo local, o ataque é descrito como: Manipulation of XRCE-DDS messages and time-related fields to induce logical desynchronization between client and agent. A documentação abaixo usa apenas artefatos já presentes no repositório, principalmente as tabelas e figuras de `experiments/60att_5runs_l0l1l2l3/iot_xrce_dds_time_desync`.

## Metadados do ataque

| Campo | Valor |
| --- | --- |
| ID | `iot_xrce_dds_time_desync` |
| Categoria | 7) IoT |
| Subcategoria | 7.1 IoT Protocols / XRCE-DDS |
| Serviços alvo | xrce-dds-agent |
| Imagem | `attack-xrce-dds-time-desync:latest` |
| Container | `attack-xrce-dds-time-desync` |
| Runtime máximo do catálogo | 30 s |
| Parâmetros de intensidade | duration_s |
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0040/](https://attack.mitre.org/tactics/TA0040/)<br>[https://attack.mitre.org/techniques/T1565/](https://attack.mitre.org/techniques/T1565/)<br>[https://attack.mitre.org/techniques/T1565/002/](https://attack.mitre.org/techniques/T1565/002/) |

## Resumo estatístico por nível

| Nível | Serviço | Runs | Amostras attack | Sucesso médio | Falha média | Lat p50/p95 ms | PCAP total MB | Dataset médio (min-max) | Exec média s | Extratores ok/total | CPU média/máx | Mem MB média |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | xrce | 5 | 100 | 100% | 0% | 500,69 / 500,81 | 0,05 | 234 (234-234) | 41,92 | 3/3 | 34,13% / 46,4% | 1.716,91 |
| L1 | xrce | 5 | 100 | 100% | 0% | 500,67 / 500,77 | 5,18 | 24.714 (24.714-24.714) | 45,2 | 3/3 | 33,77% / 49,1% | 1.716,93 |
| L2 | xrce | 5 | 100 | 100% | 0% | 500,72 / 500,86 | 5,18 | 24.714 (24.714-24.714) | 45,19 | 3/3 | 34,94% / 51,91% | 1.716,91 |
| L3 | xrce | 5 | 100 | 100% | 0% | 500,7 / 500,84 | 5,18 | 24.714 (24.714-24.714) | 45,17 | 3/3 | 36,41% / 51,81% | 1.716,93 |

## Estabilidade entre reexecuções

| Nível | Métrica | Runs | Média | Desvio | CV | Min | Max |
| --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | CPU média na fase attack | 5 | 34,13 | 2,93 | 8,6% | 31,82 | 38,2 |
| L0 | Linhas do dataset | 5 | 234 | 0 | 0% | 234 | 234 |
| L0 | Tempo de execução | 5 | 41,92 | 0,38 | 0,91% | 41,7 | 42,6 |
| L0 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L0 | Latência p95 censurada | 5 | 500,81 | 0,06 | 0,01% | 500,77 | 500,89 |
| L1 | CPU média na fase attack | 5 | 33,77 | 1,87 | 5,55% | 32,06 | 36,57 |
| L1 | Linhas do dataset | 5 | 24.714 | 0 | 0% | 24.714 | 24.714 |
| L1 | Tempo de execução | 5 | 45,2 | 0,03 | 0,07% | 45,17 | 45,25 |
| L1 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L1 | Latência p95 censurada | 5 | 500,77 | 0,07 | 0,01% | 500,71 | 500,88 |
| L2 | CPU média na fase attack | 5 | 34,94 | 3,75 | 10,73% | 29,82 | 38,61 |
| L2 | Linhas do dataset | 5 | 24.714 | 0 | 0% | 24.714 | 24.714 |
| L2 | Tempo de execução | 5 | 45,19 | 0,05 | 0,1% | 45,11 | 45,23 |
| L2 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L2 | Latência p95 censurada | 5 | 500,86 | 0,12 | 0,02% | 500,72 | 501,03 |
| L3 | CPU média na fase attack | 5 | 36,41 | 1,8 | 4,96% | 34,67 | 38,67 |
| L3 | Linhas do dataset | 5 | 24.714 | 0 | 0% | 24.714 | 24.714 |
| L3 | Tempo de execução | 5 | 45,17 | 0,05 | 0,12% | 45,11 | 45,24 |
| L3 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L3 | Latência p95 censurada | 5 | 500,84 | 0,1 | 0,02% | 500,72 | 500,95 |

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
<td><img src="../../assets/campaign_doc/iot_xrce_dds_time_desync/F3_v1_timeseries_xrce_iot_xrce_dds_time_desync_L0_run01.png" alt="Série temporal L0 run01" width="420"><br><sub>Série temporal L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/iot_xrce_dds_time_desync/F3_v1_timeseries_xrce_iot_xrce_dds_time_desync_L1_run01.png" alt="Série temporal L1 run01" width="420"><br><sub>Série temporal L1 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/iot_xrce_dds_time_desync/F3_v1_timeseries_xrce_iot_xrce_dds_time_desync_L2_run01.png" alt="Série temporal L2 run01" width="420"><br><sub>Série temporal L2 run01</sub></td>
<td><img src="../../assets/campaign_doc/iot_xrce_dds_time_desync/F3_v1_timeseries_xrce_iot_xrce_dds_time_desync_L3_run01.png" alt="Série temporal L3 run01" width="420"><br><sub>Série temporal L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/iot_xrce_dds_time_desync/F5_resources_xrce_iot_xrce_dds_time_desync_L0_run01.png" alt="Recursos L0 run01" width="420"><br><sub>Recursos L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/iot_xrce_dds_time_desync/F5_resources_xrce_iot_xrce_dds_time_desync_L3_run01.png" alt="Recursos L3 run01" width="420"><br><sub>Recursos L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/iot_xrce_dds_time_desync/F4_v2_failrate_xrce_iot_xrce_dds_time_desync_L0.png" alt="Taxa de falha L0" width="420"><br><sub>Taxa de falha L0</sub></td>
<td><img src="../../assets/campaign_doc/iot_xrce_dds_time_desync/F4_v2_failrate_xrce_iot_xrce_dds_time_desync_L3.png" alt="Taxa de falha L3" width="420"><br><sub>Taxa de falha L3</sub></td>
</tr>
</table>

## Fontes utilizadas

- Catálogo do ataque: `docker/attackers/xrce-dds-time-desync/attack.yaml`
- Artefatos da campanha: `experiments/60att_5runs_l0l1l2l3/iot_xrce_dds_time_desync`
