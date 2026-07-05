# XRCE-DDS Fragment Abuse (`iot_xrce_dds_fragment_abuse`)

[Índice da campanha](README.md)

Na campanha `experiments/60att_5runs_l0l1l2l3`, este documento consolida a execução do ataque `iot_xrce_dds_fragment_abuse`. No catálogo local, o ataque é descrito como: Fragmented, incomplete, or overlapping XRCE-DDS publications that stress reassembly, queues, and fragment handling on the agent. A documentação abaixo usa apenas artefatos já presentes no repositório, principalmente as tabelas e figuras de `experiments/60att_5runs_l0l1l2l3/iot_xrce_dds_fragment_abuse`.

## Metadados do ataque

| Campo | Valor |
| --- | --- |
| ID | `iot_xrce_dds_fragment_abuse` |
| Categoria | 7) IoT |
| Subcategoria | 7.1 IoT Protocols / XRCE-DDS |
| Serviços alvo | xrce-dds-agent |
| Imagem | `attack-xrce-dds-fragment-abuse:latest` |
| Container | `attack-xrce-dds-fragment-abuse` |
| Runtime máximo do catálogo | 30 s |
| Parâmetros de intensidade | duration_s |
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0040/](https://attack.mitre.org/tactics/TA0040/)<br>[https://attack.mitre.org/techniques/T1499/](https://attack.mitre.org/techniques/T1499/)<br>[https://attack.mitre.org/techniques/T1499/003/](https://attack.mitre.org/techniques/T1499/003/)<br>[https://attack.mitre.org/techniques/T1499/004/](https://attack.mitre.org/techniques/T1499/004/) |

## Resumo estatístico por nível

| Nível | Serviço | Runs | Amostras attack | Sucesso médio | Falha média | Lat p50/p95 ms | PCAP total MB | Dataset médio (min-max) | Exec média s | Extratores ok/total | CPU média/máx | Mem MB média |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | xrce | 5 | 100 | 100% | 0% | 500,71 / 500,82 | 0,05 | 234 (234-234) | 41,97 | 3/3 | 45,36% / 63,2% | 1.749,13 |
| L1 | xrce | 5 | 100 | 100% | 0% | 500,72 / 500,86 | 0,06 | 306 (306-306) | 41,81 | 3/3 | 47,08% / 63,92% | 1.749,13 |
| L2 | xrce | 5 | 100 | 100% | 0% | 500,71 / 500,89 | 0,06 | 308 (306-318) | 41,77 | 3/3 | 41,85% / 78,72% | 1.732,22 |
| L3 | xrce | 5 | 100 | 100% | 0% | 500,73 / 500,83 | 0,06 | 306 (306-306) | 41,75 | 3/3 | 35,52% / 50,95% | 1.719,06 |

## Estabilidade entre reexecuções

| Nível | Métrica | Runs | Média | Desvio | CV | Min | Max |
| --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | CPU média na fase attack | 5 | 45,36 | 3,25 | 7,17% | 41,37 | 48,96 |
| L0 | Linhas do dataset | 5 | 234 | 0 | 0% | 234 | 234 |
| L0 | Tempo de execução | 5 | 41,97 | 0,31 | 0,73% | 41,73 | 42,5 |
| L0 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L0 | Latência p95 censurada | 5 | 500,82 | 0,04 | 0,01% | 500,78 | 500,88 |
| L1 | CPU média na fase attack | 5 | 47,08 | 1,21 | 2,58% | 46,13 | 48,8 |
| L1 | Linhas do dataset | 5 | 306 | 0 | 0% | 306 | 306 |
| L1 | Tempo de execução | 5 | 41,81 | 0,05 | 0,11% | 41,74 | 41,85 |
| L1 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L1 | Latência p95 censurada | 5 | 500,86 | 0,09 | 0,02% | 500,77 | 500,98 |
| L2 | CPU média na fase attack | 5 | 41,85 | 6,54 | 15,64% | 32,78 | 47,48 |
| L2 | Linhas do dataset | 5 | 308,4 | 5,37 | 1,74% | 306 | 318 |
| L2 | Tempo de execução | 5 | 41,77 | 0,09 | 0,23% | 41,69 | 41,93 |
| L2 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L2 | Latência p95 censurada | 5 | 500,89 | 0,09 | 0,02% | 500,74 | 500,98 |
| L3 | CPU média na fase attack | 5 | 35,52 | 2,95 | 8,3% | 32,88 | 40,19 |
| L3 | Linhas do dataset | 5 | 306 | 0 | 0% | 306 | 306 |
| L3 | Tempo de execução | 5 | 41,75 | 0,03 | 0,07% | 41,72 | 41,79 |
| L3 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L3 | Latência p95 censurada | 5 | 500,83 | 0,1 | 0,02% | 500,74 | 500,99 |

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
<td><img src="../../assets/campaign_doc/iot_xrce_dds_fragment_abuse/F3_v1_timeseries_xrce_iot_xrce_dds_fragment_abuse_L0_run01.png" alt="Série temporal L0 run01" width="420"><br><sub>Série temporal L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/iot_xrce_dds_fragment_abuse/F3_v1_timeseries_xrce_iot_xrce_dds_fragment_abuse_L1_run01.png" alt="Série temporal L1 run01" width="420"><br><sub>Série temporal L1 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/iot_xrce_dds_fragment_abuse/F3_v1_timeseries_xrce_iot_xrce_dds_fragment_abuse_L2_run01.png" alt="Série temporal L2 run01" width="420"><br><sub>Série temporal L2 run01</sub></td>
<td><img src="../../assets/campaign_doc/iot_xrce_dds_fragment_abuse/F3_v1_timeseries_xrce_iot_xrce_dds_fragment_abuse_L3_run01.png" alt="Série temporal L3 run01" width="420"><br><sub>Série temporal L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/iot_xrce_dds_fragment_abuse/F5_resources_xrce_iot_xrce_dds_fragment_abuse_L0_run01.png" alt="Recursos L0 run01" width="420"><br><sub>Recursos L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/iot_xrce_dds_fragment_abuse/F5_resources_xrce_iot_xrce_dds_fragment_abuse_L3_run01.png" alt="Recursos L3 run01" width="420"><br><sub>Recursos L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/iot_xrce_dds_fragment_abuse/F4_v2_failrate_xrce_iot_xrce_dds_fragment_abuse_L0.png" alt="Taxa de falha L0" width="420"><br><sub>Taxa de falha L0</sub></td>
<td><img src="../../assets/campaign_doc/iot_xrce_dds_fragment_abuse/F4_v2_failrate_xrce_iot_xrce_dds_fragment_abuse_L3.png" alt="Taxa de falha L3" width="420"><br><sub>Taxa de falha L3</sub></td>
</tr>
</table>

## Fontes utilizadas

- Catálogo do ataque: `docker/attackers/xrce-dds-fragment-abuse/attack.yaml`
- Artefatos da campanha: `experiments/60att_5runs_l0l1l2l3/iot_xrce_dds_fragment_abuse`
