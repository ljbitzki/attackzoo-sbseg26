# CoAP Resource Discovery Exhaustion (`iot_coap_resource_exhaustion`)

[Índice da campanha](README.md)

Na campanha `experiments/60att_5runs_l0l1l2l3`, este documento consolida a execução do ataque `iot_coap_resource_exhaustion`. No catálogo local, o ataque é descrito como: Burst of CoAP resource discovery/mapping messages, typically against /.well-known/core, intended to exhaust target resources. A documentação abaixo usa apenas artefatos já presentes no repositório, principalmente as tabelas e figuras de `experiments/60att_5runs_l0l1l2l3/iot_coap_resource_exhaustion`.

## Metadados do ataque

| Campo | Valor |
| --- | --- |
| ID | `iot_coap_resource_exhaustion` |
| Categoria | 7) IoT |
| Subcategoria | 7.1 IoT Protocols / CoAP |
| Serviços alvo | coap-server |
| Imagem | `attack-coap-resource-exhaustion:latest` |
| Container | `attack-coap-resource-exhaustion` |
| Runtime máximo do catálogo | 10 s |
| Parâmetros de intensidade | n/d |
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0043/](https://attack.mitre.org/tactics/TA0043/)<br>[https://attack.mitre.org/tactics/TA0040/](https://attack.mitre.org/tactics/TA0040/)<br>[https://attack.mitre.org/techniques/T1595/](https://attack.mitre.org/techniques/T1595/)<br>[https://attack.mitre.org/techniques/T1595/003/](https://attack.mitre.org/techniques/T1595/003/)<br>[https://attack.mitre.org/techniques/T1499/](https://attack.mitre.org/techniques/T1499/)<br>[https://attack.mitre.org/techniques/T1499/003/](https://attack.mitre.org/techniques/T1499/003/) |

## Resumo estatístico por nível

| Nível | Serviço | Runs | Amostras attack | Sucesso médio | Falha média | Lat p50/p95 ms | PCAP total MB | Dataset médio (min-max) | Exec média s | Extratores ok/total | CPU média/máx | Mem MB média |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | coap | 5 | 200 | 100% | 0% | 1,09 / 1,59 | 0,21 | 948 (948-948) | 42,04 | 3/3 | 0,12% / 0,17% | 6,34 |
| L1 | coap | 5 | 200 | 100% | 0% | 1,04 / 1,57 | 0,56 | 2.666 (2.628-2.676) | 42,09 | 3/3 | 0,43% / 1,89% | 6,37 |
| L2 | coap | 5 | 200 | 100% | 0% | 1,05 / 1,35 | 0,56 | 2.676 (2.676-2.676) | 42,04 | 3/3 | 0,45% / 2,26% | 6,38 |
| L3 | coap | 5 | 200 | 100% | 0% | 1,25 / 1,8 | 0,56 | 2.676 (2.676-2.676) | 42,19 | 3/3 | 0,49% / 2,29% | 6,36 |

## Estabilidade entre reexecuções

| Nível | Métrica | Runs | Média | Desvio | CV | Min | Max |
| --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | CPU média na fase attack | 5 | 0,12 | 0,01 | 9,76% | 0,11 | 0,14 |
| L0 | Linhas do dataset | 5 | 948 | 0 | 0% | 948 | 948 |
| L0 | Tempo de execução | 5 | 42,04 | 0,26 | 0,63% | 41,9 | 42,51 |
| L0 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L0 | Latência p95 censurada | 5 | 1,59 | 0,31 | 19,68% | 1,1 | 1,96 |
| L1 | CPU média na fase attack | 5 | 0,43 | 0,12 | 28,58% | 0,23 | 0,54 |
| L1 | Linhas do dataset | 5 | 2.666,4 | 21,47 | 0,81% | 2.628 | 2.676 |
| L1 | Tempo de execução | 5 | 42,09 | 0,06 | 0,14% | 42,05 | 42,19 |
| L1 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L1 | Latência p95 censurada | 5 | 1,57 | 0,44 | 28,21% | 1,09 | 2,02 |
| L2 | CPU média na fase attack | 5 | 0,45 | 0,04 | 8,69% | 0,41 | 0,51 |
| L2 | Linhas do dataset | 5 | 2.676 | 0 | 0% | 2.676 | 2.676 |
| L2 | Tempo de execução | 5 | 42,04 | 0,05 | 0,12% | 41,98 | 42,11 |
| L2 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L2 | Latência p95 censurada | 5 | 1,35 | 0,36 | 26,44% | 1,13 | 1,97 |
| L3 | CPU média na fase attack | 5 | 0,49 | 0,03 | 5,98% | 0,45 | 0,52 |
| L3 | Linhas do dataset | 5 | 2.676 | 0 | 0% | 2.676 | 2.676 |
| L3 | Tempo de execução | 5 | 42,19 | 0,1 | 0,24% | 42,06 | 42,33 |
| L3 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L3 | Latência p95 censurada | 5 | 1,8 | 0,29 | 16,33% | 1,31 | 2,1 |

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
<td><img src="../../assets/campaign_doc/iot_coap_resource_exhaustion/F3_v1_timeseries_coap_iot_coap_resource_exhaustion_L0_run01.png" alt="Série temporal L0 run01" width="420"><br><sub>Série temporal L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/iot_coap_resource_exhaustion/F3_v1_timeseries_coap_iot_coap_resource_exhaustion_L1_run01.png" alt="Série temporal L1 run01" width="420"><br><sub>Série temporal L1 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/iot_coap_resource_exhaustion/F3_v1_timeseries_coap_iot_coap_resource_exhaustion_L2_run01.png" alt="Série temporal L2 run01" width="420"><br><sub>Série temporal L2 run01</sub></td>
<td><img src="../../assets/campaign_doc/iot_coap_resource_exhaustion/F3_v1_timeseries_coap_iot_coap_resource_exhaustion_L3_run01.png" alt="Série temporal L3 run01" width="420"><br><sub>Série temporal L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/iot_coap_resource_exhaustion/F5_resources_coap_iot_coap_resource_exhaustion_L0_run01.png" alt="Recursos L0 run01" width="420"><br><sub>Recursos L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/iot_coap_resource_exhaustion/F5_resources_coap_iot_coap_resource_exhaustion_L3_run01.png" alt="Recursos L3 run01" width="420"><br><sub>Recursos L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/iot_coap_resource_exhaustion/F4_v2_failrate_coap_iot_coap_resource_exhaustion_L0.png" alt="Taxa de falha L0" width="420"><br><sub>Taxa de falha L0</sub></td>
<td><img src="../../assets/campaign_doc/iot_coap_resource_exhaustion/F4_v2_failrate_coap_iot_coap_resource_exhaustion_L3.png" alt="Taxa de falha L3" width="420"><br><sub>Taxa de falha L3</sub></td>
</tr>
</table>

## Fontes utilizadas

- Catálogo do ataque: `docker/attackers/coap-resource-exhaustion/attack.yaml`
- Artefatos da campanha: `experiments/60att_5runs_l0l1l2l3/iot_coap_resource_exhaustion`
