# CoAP Response Fuzzing (`iot_coap_response_fuzz`)

[Índice da campanha](README.md)

Na campanha `experiments/60att_5runs_l0l1l2l3`, este documento consolida a execução do ataque `iot_coap_response_fuzz`. No catálogo local, o ataque é descrito como: Burst of randomized or mutated CoAP messages intended to trigger errors, exceptions, or crashes on the target. A documentação abaixo usa apenas artefatos já presentes no repositório, principalmente as tabelas e figuras de `experiments/60att_5runs_l0l1l2l3/iot_coap_response_fuzz`.

## Metadados do ataque

| Campo | Valor |
| --- | --- |
| ID | `iot_coap_response_fuzz` |
| Categoria | 7) IoT |
| Subcategoria | 7.1 IoT Protocols / CoAP |
| Serviços alvo | coap-server |
| Imagem | `attack-coap-response-fuzz:latest` |
| Container | `attack-coap-response-fuzz` |
| Runtime máximo do catálogo | 10 s |
| Parâmetros de intensidade | n/d |
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0043/](https://attack.mitre.org/tactics/TA0043/)<br>[https://attack.mitre.org/tactics/TA0001/](https://attack.mitre.org/tactics/TA0001/)<br>[https://attack.mitre.org/tactics/TA0040/](https://attack.mitre.org/tactics/TA0040/)<br>[https://attack.mitre.org/techniques/T1595/](https://attack.mitre.org/techniques/T1595/)<br>[https://attack.mitre.org/techniques/T1595/002/](https://attack.mitre.org/techniques/T1595/002/)<br>[https://attack.mitre.org/techniques/T1190/](https://attack.mitre.org/techniques/T1190/)<br>[https://attack.mitre.org/techniques/T1499/](https://attack.mitre.org/techniques/T1499/)<br>[https://attack.mitre.org/techniques/T1499/004/](https://attack.mitre.org/techniques/T1499/004/) |

## Resumo estatístico por nível

| Nível | Serviço | Runs | Amostras attack | Sucesso médio | Falha média | Lat p50/p95 ms | PCAP total MB | Dataset médio (min-max) | Exec média s | Extratores ok/total | CPU média/máx | Mem MB média |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | coap | 5 | 200 | 100% | 0% | 1 / 1,17 | 0,21 | 948 (948-948) | 41,91 | 3/3 | 0,11% / 0,13% | 6,37 |
| L1 | coap | 5 | 196 | 1,1% | 98,9% | 2.000,44 / 2.000,44 | 0,22 | 380 (326-594) | 41,89 | 3/3 | 0,39% / 2,19% | 7,21 |
| L2 | coap | 5 | 200 | 0% | 100% | 2.000 / 2.000 | 0,22 | 326 (326-326) | 42,06 | 3/3 | 0,33% / 2,82% | 1.459,5 |
| L3 | coap | 5 | 200 | 0% | 100% | 2.000 / 2.000 | 0,22 | 326 (326-326) | 42,15 | 3/3 | 0,34% / 3,12% | 1.462,01 |

## Estabilidade entre reexecuções

| Nível | Métrica | Runs | Média | Desvio | CV | Min | Max |
| --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | CPU média na fase attack | 5 | 0,11 | 0,01 | 5,37% | 0,11 | 0,12 |
| L0 | Linhas do dataset | 5 | 948 | 0 | 0% | 948 | 948 |
| L0 | Tempo de execução | 5 | 41,91 | 0,36 | 0,85% | 41,7 | 42,55 |
| L0 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L0 | Latência p95 censurada | 5 | 1,17 | 0,11 | 9,18% | 1,09 | 1,36 |
| L1 | CPU média na fase attack | 5 | 0,39 | 0,23 | 59,28% | 0,25 | 0,79 |
| L1 | Linhas do dataset | 5 | 379,6 | 119,85 | 31,57% | 326 | 594 |
| L1 | Tempo de execução | 5 | 41,89 | 0,21 | 0,5% | 41,53 | 42,08 |
| L1 | Falha na fase attack | 5 | 98,89 | 2,48 | 2,51% | 94,44 | 100 |
| L1 | Latência p95 censurada | 5 | 2.000,44 | 0,98 | 0,05% | 2.000 | 2.002,18 |
| L2 | CPU média na fase attack | 5 | 0,33 | 0,05 | 15,96% | 0,29 | 0,41 |
| L2 | Linhas do dataset | 5 | 326 | 0 | 0% | 326 | 326 |
| L2 | Tempo de execução | 5 | 42,06 | 0,06 | 0,14% | 42 | 42,15 |
| L2 | Falha na fase attack | 5 | 100 | 0 | 0% | 100 | 100 |
| L2 | Latência p95 censurada | 5 | 2.000 | 0 | 0% | 2.000 | 2.000 |
| L3 | CPU média na fase attack | 5 | 0,34 | 0,06 | 18,09% | 0,28 | 0,44 |
| L3 | Linhas do dataset | 5 | 326 | 0 | 0% | 326 | 326 |
| L3 | Tempo de execução | 5 | 42,15 | 0,1 | 0,25% | 42 | 42,26 |
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
<td><img src="../../assets/campaign_doc/iot_coap_response_fuzz/F3_v1_timeseries_coap_iot_coap_response_fuzz_L0_run01.png" alt="Série temporal L0 run01" width="420"><br><sub>Série temporal L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/iot_coap_response_fuzz/F3_v1_timeseries_coap_iot_coap_response_fuzz_L1_run01.png" alt="Série temporal L1 run01" width="420"><br><sub>Série temporal L1 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/iot_coap_response_fuzz/F3_v1_timeseries_coap_iot_coap_response_fuzz_L2_run01.png" alt="Série temporal L2 run01" width="420"><br><sub>Série temporal L2 run01</sub></td>
<td><img src="../../assets/campaign_doc/iot_coap_response_fuzz/F3_v1_timeseries_coap_iot_coap_response_fuzz_L3_run01.png" alt="Série temporal L3 run01" width="420"><br><sub>Série temporal L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/iot_coap_response_fuzz/F5_resources_coap_iot_coap_response_fuzz_L0_run01.png" alt="Recursos L0 run01" width="420"><br><sub>Recursos L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/iot_coap_response_fuzz/F5_resources_coap_iot_coap_response_fuzz_L3_run01.png" alt="Recursos L3 run01" width="420"><br><sub>Recursos L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/iot_coap_response_fuzz/F4_v2_failrate_coap_iot_coap_response_fuzz_L0.png" alt="Taxa de falha L0" width="420"><br><sub>Taxa de falha L0</sub></td>
<td><img src="../../assets/campaign_doc/iot_coap_response_fuzz/F4_v2_failrate_coap_iot_coap_response_fuzz_L3.png" alt="Taxa de falha L3" width="420"><br><sub>Taxa de falha L3</sub></td>
</tr>
</table>

## Fontes utilizadas

- Catálogo do ataque: `docker/attackers/coap-response-fuzz/attack.yaml`
- Artefatos da campanha: `experiments/60att_5runs_l0l1l2l3/iot_coap_response_fuzz`
