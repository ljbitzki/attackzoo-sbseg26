# XRCE-DDS UDP DoS (`iot_xrce_dds_udp_dos`)

[Índice da campanha](README.md)

Na campanha `experiments/60att_5runs_l0l1l2l3`, este documento consolida a execução do ataque `iot_xrce_dds_udp_dos`. No catálogo local, o ataque é descrito como: UDP packet flood against the XRCE-DDS agent to degrade network or service availability. A documentação abaixo usa apenas artefatos já presentes no repositório, principalmente as tabelas e figuras de `experiments/60att_5runs_l0l1l2l3/iot_xrce_dds_udp_dos`.

## Metadados do ataque

| Campo | Valor |
| --- | --- |
| ID | `iot_xrce_dds_udp_dos` |
| Categoria | 7) IoT |
| Subcategoria | 7.1 IoT Protocols / XRCE-DDS |
| Serviços alvo | xrce-dds-agent |
| Imagem | `attack-xrce-dds-udp-dos:latest` |
| Container | `attack-xrce-dds-udp-dos` |
| Runtime máximo do catálogo | 10 s |
| Parâmetros de intensidade | duration_s |
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0040/](https://attack.mitre.org/tactics/TA0040/)<br>[https://attack.mitre.org/techniques/T1498/](https://attack.mitre.org/techniques/T1498/)<br>[https://attack.mitre.org/techniques/T1498/001/](https://attack.mitre.org/techniques/T1498/001/)<br>[https://attack.mitre.org/techniques/T1499/](https://attack.mitre.org/techniques/T1499/)<br>[https://attack.mitre.org/techniques/T1499/002/](https://attack.mitre.org/techniques/T1499/002/) |

## Resumo estatístico por nível

| Nível | Serviço | Runs | Amostras attack | Sucesso médio | Falha média | Lat p50/p95 ms | PCAP total MB | Dataset médio (min-max) | Exec média s | Extratores ok/total | CPU média/máx | Mem MB média |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | xrce | 5 | 100 | 100% | 0% | 500,69 / 500,81 | 0,05 | 234 (234-234) | 41,93 | 3/3 | 34,2% / 50,77% | 1.716,91 |
| L1 | xrce | 5 | 107 | 100% | 0% | 500,57 / 500,78 | 2.188,72 | 10.205.420 (7.981.848-10.934.412) | 1.515,98 | 3/3 | 192,92% / 230,01% | 1.716,91 |
| L2 | xrce | 5 | 105 | 100% | 0% | 500,48 / 500,69 | 2.297,12 | 10.709.760 (10.578.440-10.941.214) | 1.597,04 | 3/3 | 198,13% / 228,86% | 1.716,91 |
| L3 | xrce | 5 | 104 | 100% | 0% | 500,6 / 500,68 | 2.287,81 | 10.666.311 (9.928.674-11.018.584) | 1.599,34 | 3/3 | 195,4% / 228,67% | 1.716,91 |

## Estabilidade entre reexecuções

| Nível | Métrica | Runs | Média | Desvio | CV | Min | Max |
| --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | CPU média na fase attack | 5 | 34,2 | 2,1 | 6,13% | 31,87 | 37,37 |
| L0 | Linhas do dataset | 5 | 234 | 0 | 0% | 234 | 234 |
| L0 | Tempo de execução | 5 | 41,93 | 0,35 | 0,84% | 41,75 | 42,57 |
| L0 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L0 | Latência p95 censurada | 5 | 500,81 | 0,09 | 0,02% | 500,69 | 500,91 |
| L1 | CPU média na fase attack | 5 | 192,92 | 17,36 | 9% | 162,65 | 204,11 |
| L1 | Linhas do dataset | 5 | 10.205.419,6 | 1.250.996,32 | 12,26% | 7.981.848 | 10.934.412 |
| L1 | Tempo de execução | 5 | 1.515,98 | 181,12 | 11,95% | 1.193,15 | 1.614,74 |
| L1 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L1 | Latência p95 censurada | 5 | 500,78 | 0,07 | 0,01% | 500,71 | 500,85 |
| L2 | CPU média na fase attack | 5 | 198,13 | 0,97 | 0,49% | 196,66 | 199,3 |
| L2 | Linhas do dataset | 5 | 10.709.760,4 | 175.936,02 | 1,64% | 10.578.440 | 10.941.214 |
| L2 | Tempo de execução | 5 | 1.597,04 | 21,47 | 1,34% | 1.574,54 | 1.623,49 |
| L2 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L2 | Latência p95 censurada | 5 | 500,69 | 0,02 | 0% | 500,66 | 500,72 |
| L3 | CPU média na fase attack | 5 | 195,4 | 1,11 | 0,57% | 193,82 | 196,59 |
| L3 | Linhas do dataset | 5 | 10.666.310,8 | 456.689,09 | 4,28% | 9.928.674 | 11.018.584 |
| L3 | Tempo de execução | 5 | 1.599,34 | 66,03 | 4,13% | 1.495,33 | 1.657,69 |
| L3 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L3 | Latência p95 censurada | 5 | 500,68 | 0,03 | 0,01% | 500,65 | 500,71 |

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
<td><img src="../../assets/campaign_doc/iot_xrce_dds_udp_dos/F3_v1_timeseries_xrce_iot_xrce_dds_udp_dos_L0_run01.png" alt="Série temporal L0 run01" width="420"><br><sub>Série temporal L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/iot_xrce_dds_udp_dos/F3_v1_timeseries_xrce_iot_xrce_dds_udp_dos_L1_run01.png" alt="Série temporal L1 run01" width="420"><br><sub>Série temporal L1 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/iot_xrce_dds_udp_dos/F3_v1_timeseries_xrce_iot_xrce_dds_udp_dos_L2_run01.png" alt="Série temporal L2 run01" width="420"><br><sub>Série temporal L2 run01</sub></td>
<td><img src="../../assets/campaign_doc/iot_xrce_dds_udp_dos/F3_v1_timeseries_xrce_iot_xrce_dds_udp_dos_L3_run01.png" alt="Série temporal L3 run01" width="420"><br><sub>Série temporal L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/iot_xrce_dds_udp_dos/F5_resources_xrce_iot_xrce_dds_udp_dos_L0_run01.png" alt="Recursos L0 run01" width="420"><br><sub>Recursos L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/iot_xrce_dds_udp_dos/F5_resources_xrce_iot_xrce_dds_udp_dos_L3_run01.png" alt="Recursos L3 run01" width="420"><br><sub>Recursos L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/iot_xrce_dds_udp_dos/F4_v2_failrate_xrce_iot_xrce_dds_udp_dos_L0.png" alt="Taxa de falha L0" width="420"><br><sub>Taxa de falha L0</sub></td>
<td><img src="../../assets/campaign_doc/iot_xrce_dds_udp_dos/F4_v2_failrate_xrce_iot_xrce_dds_udp_dos_L3.png" alt="Taxa de falha L3" width="420"><br><sub>Taxa de falha L3</sub></td>
</tr>
</table>

## Fontes utilizadas

- Catálogo do ataque: `docker/attackers/xrce-dds-udp-dos/attack.yaml`
- Artefatos da campanha: `experiments/60att_5runs_l0l1l2l3/iot_xrce_dds_udp_dos`
