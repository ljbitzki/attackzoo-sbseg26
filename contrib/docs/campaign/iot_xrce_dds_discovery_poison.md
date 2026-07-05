# XRCE-DDS Discovery Poisoning (`iot_xrce_dds_discovery_poison`)

[Índice da campanha](README.md)

Na campanha `experiments/60att_5runs_l0l1l2l3`, este documento consolida a execução do ataque `iot_xrce_dds_discovery_poison`. No catálogo local, o ataque é descrito como: Poisoning or manipulation of XRCE-DDS agent discovery messages to induce incorrect association, redirection, or discovery degradation. A documentação abaixo usa apenas artefatos já presentes no repositório, principalmente as tabelas e figuras de `experiments/60att_5runs_l0l1l2l3/iot_xrce_dds_discovery_poison`.

## Metadados do ataque

| Campo | Valor |
| --- | --- |
| ID | `iot_xrce_dds_discovery_poison` |
| Categoria | 7) IoT |
| Subcategoria | 7.1 IoT Protocols / XRCE-DDS |
| Serviços alvo | xrce-dds-agent |
| Imagem | `attack-xrce-dds-discovery-poison:latest` |
| Container | `attack-xrce-dds-discovery-poison` |
| Runtime máximo do catálogo | 10 s |
| Parâmetros de intensidade | duration_s |
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0006/](https://attack.mitre.org/tactics/TA0006/)<br>[https://attack.mitre.org/tactics/TA0009/](https://attack.mitre.org/tactics/TA0009/)<br>[https://attack.mitre.org/tactics/TA0040/](https://attack.mitre.org/tactics/TA0040/)<br>[https://attack.mitre.org/techniques/T1557/](https://attack.mitre.org/techniques/T1557/)<br>[https://attack.mitre.org/techniques/T1565/](https://attack.mitre.org/techniques/T1565/)<br>[https://attack.mitre.org/techniques/T1565/002/](https://attack.mitre.org/techniques/T1565/002/) |

## Resumo estatístico por nível

| Nível | Serviço | Runs | Amostras attack | Sucesso médio | Falha média | Lat p50/p95 ms | PCAP total MB | Dataset médio (min-max) | Exec média s | Extratores ok/total | CPU média/máx | Mem MB média |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | xrce | 5 | 100 | 100% | 0% | 500,73 / 500,78 | 0,05 | 255 (234-334) | 41,87 | 3/3 | 0,03% / 0,03% | 2,24 |
| L1 | xrce | 5 | 100 | 100% | 0% | 500,78 / 501,02 | 0,05 | 234 (234-234) | 41,71 | 3/3 | 0,03% / 0,03% | 2,24 |
| L2 | xrce | 5 | 100 | 100% | 0% | 500,77 / 501,01 | 0,05 | 234 (234-234) | 41,83 | 3/3 | 0,03% / 0,04% | 2,24 |
| L3 | xrce | 5 | 100 | 100% | 0% | 500,76 / 500,9 | 0,05 | 234 (234-234) | 41,74 | 3/3 | 0,03% / 0,04% | 2,24 |

## Estabilidade entre reexecuções

| Nível | Métrica | Runs | Média | Desvio | CV | Min | Max |
| --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | CPU média na fase attack | 5 | 0,03 | 0 | 14,09% | 0,02 | 0,03 |
| L0 | Linhas do dataset | 5 | 254,8 | 44,31 | 17,39% | 234 | 334 |
| L0 | Tempo de execução | 5 | 41,87 | 0,51 | 1,22% | 41,62 | 42,78 |
| L0 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L0 | Latência p95 censurada | 5 | 500,78 | 0,02 | 0% | 500,74 | 500,79 |
| L1 | CPU média na fase attack | 5 | 0,03 | 0 | 15,74% | 0,02 | 0,04 |
| L1 | Linhas do dataset | 5 | 234 | 0 | 0% | 234 | 234 |
| L1 | Tempo de execução | 5 | 41,71 | 0,07 | 0,17% | 41,62 | 41,8 |
| L1 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L1 | Latência p95 censurada | 5 | 501,02 | 0,5 | 0,1% | 500,75 | 501,91 |
| L2 | CPU média na fase attack | 5 | 0,03 | 0 | 12,7% | 0,03 | 0,04 |
| L2 | Linhas do dataset | 5 | 234 | 0 | 0% | 234 | 234 |
| L2 | Tempo de execução | 5 | 41,83 | 0,08 | 0,2% | 41,75 | 41,96 |
| L2 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L2 | Latência p95 censurada | 5 | 501,01 | 0,14 | 0,03% | 500,79 | 501,16 |
| L3 | CPU média na fase attack | 5 | 0,03 | 0 | 13,37% | 0,03 | 0,04 |
| L3 | Linhas do dataset | 5 | 234 | 0 | 0% | 234 | 234 |
| L3 | Tempo de execução | 5 | 41,74 | 0,04 | 0,09% | 41,71 | 41,8 |
| L3 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L3 | Latência p95 censurada | 5 | 500,9 | 0,18 | 0,04% | 500,8 | 501,21 |

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
<td><img src="../../assets/campaign_doc/iot_xrce_dds_discovery_poison/F3_v1_timeseries_xrce_iot_xrce_dds_discovery_poison_L0_run01.png" alt="Série temporal L0 run01" width="420"><br><sub>Série temporal L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/iot_xrce_dds_discovery_poison/F3_v1_timeseries_xrce_iot_xrce_dds_discovery_poison_L1_run01.png" alt="Série temporal L1 run01" width="420"><br><sub>Série temporal L1 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/iot_xrce_dds_discovery_poison/F3_v1_timeseries_xrce_iot_xrce_dds_discovery_poison_L2_run01.png" alt="Série temporal L2 run01" width="420"><br><sub>Série temporal L2 run01</sub></td>
<td><img src="../../assets/campaign_doc/iot_xrce_dds_discovery_poison/F3_v1_timeseries_xrce_iot_xrce_dds_discovery_poison_L3_run01.png" alt="Série temporal L3 run01" width="420"><br><sub>Série temporal L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/iot_xrce_dds_discovery_poison/F5_resources_xrce_iot_xrce_dds_discovery_poison_L0_run01.png" alt="Recursos L0 run01" width="420"><br><sub>Recursos L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/iot_xrce_dds_discovery_poison/F5_resources_xrce_iot_xrce_dds_discovery_poison_L3_run01.png" alt="Recursos L3 run01" width="420"><br><sub>Recursos L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/iot_xrce_dds_discovery_poison/F4_v2_failrate_xrce_iot_xrce_dds_discovery_poison_L0.png" alt="Taxa de falha L0" width="420"><br><sub>Taxa de falha L0</sub></td>
<td><img src="../../assets/campaign_doc/iot_xrce_dds_discovery_poison/F4_v2_failrate_xrce_iot_xrce_dds_discovery_poison_L3.png" alt="Taxa de falha L3" width="420"><br><sub>Taxa de falha L3</sub></td>
</tr>
</table>

## Fontes utilizadas

- Catálogo do ataque: `docker/attackers/xrce-dds-discovery-poison/attack.yaml`
- Artefatos da campanha: `experiments/60att_5runs_l0l1l2l3/iot_xrce_dds_discovery_poison`
