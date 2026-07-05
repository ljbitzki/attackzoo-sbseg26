# XRCE-DDS Session Hijack (`iot_xrce_dds_session_hijack`)

[Índice da campanha](README.md)

Na campanha `experiments/60att_5runs_l0l1l2l3`, este documento consolida a execução do ataque `iot_xrce_dds_session_hijack`. No catálogo local, o ataque é descrito como: XRCE-DDS session hijacking or collision attempts through manipulation of identifiers, keys, or session fields. A documentação abaixo usa apenas artefatos já presentes no repositório, principalmente as tabelas e figuras de `experiments/60att_5runs_l0l1l2l3/iot_xrce_dds_session_hijack`.

## Metadados do ataque

| Campo | Valor |
| --- | --- |
| ID | `iot_xrce_dds_session_hijack` |
| Categoria | 7) IoT |
| Subcategoria | 7.1 IoT Protocols / XRCE-DDS |
| Serviços alvo | xrce-dds-agent |
| Imagem | `attack-xrce-dds-session-hijack:latest` |
| Container | `attack-xrce-dds-session-hijack` |
| Runtime máximo do catálogo | 30 s |
| Parâmetros de intensidade | duration_s |
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0008/](https://attack.mitre.org/tactics/TA0008/)<br>[https://attack.mitre.org/tactics/TA0040/](https://attack.mitre.org/tactics/TA0040/)<br>[https://attack.mitre.org/techniques/T1563/](https://attack.mitre.org/techniques/T1563/)<br>[https://attack.mitre.org/techniques/T1565/](https://attack.mitre.org/techniques/T1565/)<br>[https://attack.mitre.org/techniques/T1565/002/](https://attack.mitre.org/techniques/T1565/002/) |

## Resumo estatístico por nível

| Nível | Serviço | Runs | Amostras attack | Sucesso médio | Falha média | Lat p50/p95 ms | PCAP total MB | Dataset médio (min-max) | Exec média s | Extratores ok/total | CPU média/máx | Mem MB média |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | xrce | 5 | 100 | 100% | 0% | 500,7 / 500,78 | 0,05 | 234 (234-234) | 41,92 | 3/3 | 33,83% / 47,68% | 1.715,84 |
| L1 | xrce | 5 | 100 | 100% | 0% | 500,71 / 500,96 | 0,19 | 546 (546-546) | 41,85 | 3/3 | 38,03% / 56,34% | 1.717,34 |
| L2 | xrce | 5 | 100 | 100% | 0% | 500,71 / 500,86 | 0,19 | 551 (546-558) | 41,82 | 3/3 | 35,8% / 53,03% | 1.717,9 |
| L3 | xrce | 5 | 100 | 100% | 0% | 500,7 / 500,79 | 0,19 | 548 (546-558) | 41,76 | 3/3 | 36,84% / 64,39% | 1.717,77 |

## Estabilidade entre reexecuções

| Nível | Métrica | Runs | Média | Desvio | CV | Min | Max |
| --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | CPU média na fase attack | 5 | 33,83 | 1,35 | 4% | 32,29 | 35,55 |
| L0 | Linhas do dataset | 5 | 234 | 0 | 0% | 234 | 234 |
| L0 | Tempo de execução | 5 | 41,92 | 0,33 | 0,78% | 41,72 | 42,5 |
| L0 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L0 | Latência p95 censurada | 5 | 500,78 | 0,07 | 0,01% | 500,73 | 500,91 |
| L1 | CPU média na fase attack | 5 | 38,03 | 1,24 | 3,26% | 37,18 | 40,21 |
| L1 | Linhas do dataset | 5 | 546 | 0 | 0% | 546 | 546 |
| L1 | Tempo de execução | 5 | 41,85 | 0,03 | 0,08% | 41,82 | 41,9 |
| L1 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L1 | Latência p95 censurada | 5 | 500,96 | 0,17 | 0,03% | 500,77 | 501,22 |
| L2 | CPU média na fase attack | 5 | 35,8 | 1,12 | 3,14% | 34,92 | 37,67 |
| L2 | Linhas do dataset | 5 | 550,8 | 6,57 | 1,19% | 546 | 558 |
| L2 | Tempo de execução | 5 | 41,82 | 0,02 | 0,05% | 41,8 | 41,85 |
| L2 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L2 | Latência p95 censurada | 5 | 500,86 | 0,11 | 0,02% | 500,73 | 500,98 |
| L3 | CPU média na fase attack | 5 | 36,84 | 2,6 | 7,06% | 34,14 | 39,95 |
| L3 | Linhas do dataset | 5 | 548,4 | 5,37 | 0,98% | 546 | 558 |
| L3 | Tempo de execução | 5 | 41,76 | 0,06 | 0,14% | 41,67 | 41,82 |
| L3 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L3 | Latência p95 censurada | 5 | 500,79 | 0,08 | 0,02% | 500,72 | 500,92 |

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
<td><img src="../../assets/campaign_doc/iot_xrce_dds_session_hijack/F3_v1_timeseries_xrce_iot_xrce_dds_session_hijack_L0_run01.png" alt="Série temporal L0 run01" width="420"><br><sub>Série temporal L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/iot_xrce_dds_session_hijack/F3_v1_timeseries_xrce_iot_xrce_dds_session_hijack_L1_run01.png" alt="Série temporal L1 run01" width="420"><br><sub>Série temporal L1 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/iot_xrce_dds_session_hijack/F3_v1_timeseries_xrce_iot_xrce_dds_session_hijack_L2_run01.png" alt="Série temporal L2 run01" width="420"><br><sub>Série temporal L2 run01</sub></td>
<td><img src="../../assets/campaign_doc/iot_xrce_dds_session_hijack/F3_v1_timeseries_xrce_iot_xrce_dds_session_hijack_L3_run01.png" alt="Série temporal L3 run01" width="420"><br><sub>Série temporal L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/iot_xrce_dds_session_hijack/F5_resources_xrce_iot_xrce_dds_session_hijack_L0_run01.png" alt="Recursos L0 run01" width="420"><br><sub>Recursos L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/iot_xrce_dds_session_hijack/F5_resources_xrce_iot_xrce_dds_session_hijack_L3_run01.png" alt="Recursos L3 run01" width="420"><br><sub>Recursos L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/iot_xrce_dds_session_hijack/F4_v2_failrate_xrce_iot_xrce_dds_session_hijack_L0.png" alt="Taxa de falha L0" width="420"><br><sub>Taxa de falha L0</sub></td>
<td><img src="../../assets/campaign_doc/iot_xrce_dds_session_hijack/F4_v2_failrate_xrce_iot_xrce_dds_session_hijack_L3.png" alt="Taxa de falha L3" width="420"><br><sub>Taxa de falha L3</sub></td>
</tr>
</table>

## Fontes utilizadas

- Catálogo do ataque: `docker/attackers/xrce-dds-session-hijack/attack.yaml`
- Artefatos da campanha: `experiments/60att_5runs_l0l1l2l3/iot_xrce_dds_session_hijack`
