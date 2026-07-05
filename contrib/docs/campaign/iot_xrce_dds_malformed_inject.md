# XRCE-DDS Malformed Injection (`iot_xrce_dds_malformed_inject`)

[Índice da campanha](README.md)

Na campanha `experiments/60att_5runs_l0l1l2l3`, este documento consolida a execução do ataque `iot_xrce_dds_malformed_inject`. No catálogo local, o ataque é descrito como: Injection of malformed XRCE-DDS publications or messages against the agent to trigger errors, exceptions, or crashes. A documentação abaixo usa apenas artefatos já presentes no repositório, principalmente as tabelas e figuras de `experiments/60att_5runs_l0l1l2l3/iot_xrce_dds_malformed_inject`.

## Metadados do ataque

| Campo | Valor |
| --- | --- |
| ID | `iot_xrce_dds_malformed_inject` |
| Categoria | 7) IoT |
| Subcategoria | 7.1 IoT Protocols / XRCE-DDS |
| Serviços alvo | xrce-dds-agent |
| Imagem | `attack-xrce-dds-malformed-inject:latest` |
| Container | `attack-xrce-dds-malformed-inject` |
| Runtime máximo do catálogo | 30 s |
| Parâmetros de intensidade | duration_s |
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0043/](https://attack.mitre.org/tactics/TA0043/)<br>[https://attack.mitre.org/tactics/TA0001/](https://attack.mitre.org/tactics/TA0001/)<br>[https://attack.mitre.org/tactics/TA0040/](https://attack.mitre.org/tactics/TA0040/)<br>[https://attack.mitre.org/techniques/T1595/](https://attack.mitre.org/techniques/T1595/)<br>[https://attack.mitre.org/techniques/T1595/002/](https://attack.mitre.org/techniques/T1595/002/)<br>[https://attack.mitre.org/techniques/T1190/](https://attack.mitre.org/techniques/T1190/)<br>[https://attack.mitre.org/techniques/T1499/](https://attack.mitre.org/techniques/T1499/)<br>[https://attack.mitre.org/techniques/T1499/004/](https://attack.mitre.org/techniques/T1499/004/) |

## Resumo estatístico por nível

| Nível | Serviço | Runs | Amostras attack | Sucesso médio | Falha média | Lat p50/p95 ms | PCAP total MB | Dataset médio (min-max) | Exec média s | Extratores ok/total | CPU média/máx | Mem MB média |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | xrce | 5 | 100 | 100% | 0% | 500,73 / 500,85 | 0,05 | 234 (234-234) | 41,95 | 3/3 | 34,28% / 48,76% | 1.719,06 |
| L1 | xrce | 5 | 100 | 100% | 0% | 500,71 / 501,01 | 0,17 | 498 (498-498) | 41,79 | 3/3 | 36,78% / 54,3% | 1.717,75 |
| L2 | xrce | 5 | 100 | 100% | 0% | 500,7 / 500,8 | 0,17 | 498 (498-498) | 41,77 | 3/3 | 36,17% / 63,3% | 1.715,99 |
| L3 | xrce | 5 | 100 | 100% | 0% | 500,73 / 500,87 | 0,17 | 498 (498-498) | 41,77 | 3/3 | 35,21% / 49,81% | 1.716,03 |

## Estabilidade entre reexecuções

| Nível | Métrica | Runs | Média | Desvio | CV | Min | Max |
| --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | CPU média na fase attack | 5 | 34,28 | 2,51 | 7,31% | 32,59 | 38,6 |
| L0 | Linhas do dataset | 5 | 234 | 0 | 0% | 234 | 234 |
| L0 | Tempo de execução | 5 | 41,95 | 0,4 | 0,94% | 41,73 | 42,65 |
| L0 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L0 | Latência p95 censurada | 5 | 500,85 | 0,08 | 0,02% | 500,78 | 500,99 |
| L1 | CPU média na fase attack | 5 | 36,78 | 2 | 5,45% | 33,75 | 39,12 |
| L1 | Linhas do dataset | 5 | 498 | 0 | 0% | 498 | 498 |
| L1 | Tempo de execução | 5 | 41,79 | 0,08 | 0,19% | 41,71 | 41,91 |
| L1 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L1 | Latência p95 censurada | 5 | 501,01 | 0,21 | 0,04% | 500,8 | 501,29 |
| L2 | CPU média na fase attack | 5 | 36,17 | 1,4 | 3,86% | 34,73 | 38,49 |
| L2 | Linhas do dataset | 5 | 498 | 0 | 0% | 498 | 498 |
| L2 | Tempo de execução | 5 | 41,77 | 0,02 | 0,05% | 41,75 | 41,8 |
| L2 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L2 | Latência p95 censurada | 5 | 500,8 | 0,08 | 0,02% | 500,72 | 500,94 |
| L3 | CPU média na fase attack | 5 | 35,21 | 2,61 | 7,41% | 33,56 | 39,77 |
| L3 | Linhas do dataset | 5 | 498 | 0 | 0% | 498 | 498 |
| L3 | Tempo de execução | 5 | 41,77 | 0,03 | 0,07% | 41,72 | 41,8 |
| L3 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L3 | Latência p95 censurada | 5 | 500,87 | 0,09 | 0,02% | 500,75 | 500,96 |

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
<td><img src="../../assets/campaign_doc/iot_xrce_dds_malformed_inject/F3_v1_timeseries_xrce_iot_xrce_dds_malformed_inject_L0_run01.png" alt="Série temporal L0 run01" width="420"><br><sub>Série temporal L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/iot_xrce_dds_malformed_inject/F3_v1_timeseries_xrce_iot_xrce_dds_malformed_inject_L1_run01.png" alt="Série temporal L1 run01" width="420"><br><sub>Série temporal L1 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/iot_xrce_dds_malformed_inject/F3_v1_timeseries_xrce_iot_xrce_dds_malformed_inject_L2_run01.png" alt="Série temporal L2 run01" width="420"><br><sub>Série temporal L2 run01</sub></td>
<td><img src="../../assets/campaign_doc/iot_xrce_dds_malformed_inject/F3_v1_timeseries_xrce_iot_xrce_dds_malformed_inject_L3_run01.png" alt="Série temporal L3 run01" width="420"><br><sub>Série temporal L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/iot_xrce_dds_malformed_inject/F5_resources_xrce_iot_xrce_dds_malformed_inject_L0_run01.png" alt="Recursos L0 run01" width="420"><br><sub>Recursos L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/iot_xrce_dds_malformed_inject/F5_resources_xrce_iot_xrce_dds_malformed_inject_L3_run01.png" alt="Recursos L3 run01" width="420"><br><sub>Recursos L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/iot_xrce_dds_malformed_inject/F4_v2_failrate_xrce_iot_xrce_dds_malformed_inject_L0.png" alt="Taxa de falha L0" width="420"><br><sub>Taxa de falha L0</sub></td>
<td><img src="../../assets/campaign_doc/iot_xrce_dds_malformed_inject/F4_v2_failrate_xrce_iot_xrce_dds_malformed_inject_L3.png" alt="Taxa de falha L3" width="420"><br><sub>Taxa de falha L3</sub></td>
</tr>
</table>

## Fontes utilizadas

- Catálogo do ataque: `docker/attackers/xrce-dds-malformed-inject/attack.yaml`
- Artefatos da campanha: `experiments/60att_5runs_l0l1l2l3/iot_xrce_dds_malformed_inject`
