# CoAP Token Collision (`iot_coap_token_collision`)

[Índice da campanha](README.md)

Na campanha `experiments/60att_5runs_l0l1l2l3`, este documento consolida a execução do ataque `iot_coap_token_collision`. No catálogo local, o ataque é descrito como: Burst of CoAP messages that forces token reuse or collisions to degrade target state tracking and transaction correlation. A documentação abaixo usa apenas artefatos já presentes no repositório, principalmente as tabelas e figuras de `experiments/60att_5runs_l0l1l2l3/iot_coap_token_collision`.

## Metadados do ataque

| Campo | Valor |
| --- | --- |
| ID | `iot_coap_token_collision` |
| Categoria | 7) IoT |
| Subcategoria | 7.1 IoT Protocols / CoAP |
| Serviços alvo | coap-server |
| Imagem | `attack-coap-token-collision:latest` |
| Container | `attack-coap-token-collision` |
| Runtime máximo do catálogo | 10 s |
| Parâmetros de intensidade | n/d |
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0040/](https://attack.mitre.org/tactics/TA0040/)<br>[https://attack.mitre.org/techniques/T1499/](https://attack.mitre.org/techniques/T1499/)<br>[https://attack.mitre.org/techniques/T1499/003/](https://attack.mitre.org/techniques/T1499/003/)<br>[https://attack.mitre.org/techniques/T1565/](https://attack.mitre.org/techniques/T1565/)<br>[https://attack.mitre.org/techniques/T1565/002/](https://attack.mitre.org/techniques/T1565/002/) |

## Resumo estatístico por nível

| Nível | Serviço | Runs | Amostras attack | Sucesso médio | Falha média | Lat p50/p95 ms | PCAP total MB | Dataset médio (min-max) | Exec média s | Extratores ok/total | CPU média/máx | Mem MB média |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | coap | 5 | 200 | 0% | 100% | 2.000 / 2.000 | 0,03 | 158 (158-158) | 42,19 | 3/3 | 0,15% / 0,89% | 1.383,55 |
| L1 | coap | 5 | 200 | 0% | 100% | 2.000 / 2.000 | 0,19 | 970 (970-970) | 42,03 | 3/3 | 0,39% / 2,93% | 1.447,16 |
| L2 | coap | 5 | 200 | 0% | 100% | 2.000 / 2.000 | 0,19 | 970 (970-970) | 42,23 | 3/3 | 0,4% / 2,81% | 1.454,97 |
| L3 | coap | 5 | 200 | 0% | 100% | 2.000 / 2.000 | 0,19 | 970 (970-970) | 42,09 | 3/3 | 0,4% / 2,75% | 1.453,34 |

## Estabilidade entre reexecuções

| Nível | Métrica | Runs | Média | Desvio | CV | Min | Max |
| --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | CPU média na fase attack | 5 | 0,15 | 0,05 | 33,99% | 0,11 | 0,21 |
| L0 | Linhas do dataset | 5 | 158 | 0 | 0% | 158 | 158 |
| L0 | Tempo de execução | 5 | 42,19 | 0,44 | 1,04% | 41,93 | 42,97 |
| L0 | Falha na fase attack | 5 | 100 | 0 | 0% | 100 | 100 |
| L0 | Latência p95 censurada | 5 | 2.000 | 0 | 0% | 2.000 | 2.000 |
| L1 | CPU média na fase attack | 5 | 0,39 | 0,05 | 11,93% | 0,34 | 0,44 |
| L1 | Linhas do dataset | 5 | 970 | 0 | 0% | 970 | 970 |
| L1 | Tempo de execução | 5 | 42,03 | 0,31 | 0,75% | 41,48 | 42,23 |
| L1 | Falha na fase attack | 5 | 100 | 0 | 0% | 100 | 100 |
| L1 | Latência p95 censurada | 5 | 2.000 | 0 | 0% | 2.000 | 2.000 |
| L2 | CPU média na fase attack | 5 | 0,4 | 0,06 | 14,85% | 0,34 | 0,47 |
| L2 | Linhas do dataset | 5 | 970 | 0 | 0% | 970 | 970 |
| L2 | Tempo de execução | 5 | 42,23 | 0,04 | 0,1% | 42,19 | 42,28 |
| L2 | Falha na fase attack | 5 | 100 | 0 | 0% | 100 | 100 |
| L2 | Latência p95 censurada | 5 | 2.000 | 0 | 0% | 2.000 | 2.000 |
| L3 | CPU média na fase attack | 5 | 0,4 | 0,07 | 18,17% | 0,33 | 0,48 |
| L3 | Linhas do dataset | 5 | 970 | 0 | 0% | 970 | 970 |
| L3 | Tempo de execução | 5 | 42,09 | 0,38 | 0,9% | 41,42 | 42,37 |
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
<td><img src="../../assets/campaign_doc/iot_coap_token_collision/F3_v1_timeseries_coap_iot_coap_token_collision_L0_run01.png" alt="Série temporal L0 run01" width="420"><br><sub>Série temporal L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/iot_coap_token_collision/F3_v1_timeseries_coap_iot_coap_token_collision_L1_run01.png" alt="Série temporal L1 run01" width="420"><br><sub>Série temporal L1 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/iot_coap_token_collision/F3_v1_timeseries_coap_iot_coap_token_collision_L2_run01.png" alt="Série temporal L2 run01" width="420"><br><sub>Série temporal L2 run01</sub></td>
<td><img src="../../assets/campaign_doc/iot_coap_token_collision/F3_v1_timeseries_coap_iot_coap_token_collision_L3_run01.png" alt="Série temporal L3 run01" width="420"><br><sub>Série temporal L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/iot_coap_token_collision/F5_resources_coap_iot_coap_token_collision_L0_run01.png" alt="Recursos L0 run01" width="420"><br><sub>Recursos L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/iot_coap_token_collision/F5_resources_coap_iot_coap_token_collision_L3_run01.png" alt="Recursos L3 run01" width="420"><br><sub>Recursos L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/iot_coap_token_collision/F4_v2_failrate_coap_iot_coap_token_collision_L0.png" alt="Taxa de falha L0" width="420"><br><sub>Taxa de falha L0</sub></td>
<td><img src="../../assets/campaign_doc/iot_coap_token_collision/F4_v2_failrate_coap_iot_coap_token_collision_L3.png" alt="Taxa de falha L3" width="420"><br><sub>Taxa de falha L3</sub></td>
</tr>
</table>

## Fontes utilizadas

- Catálogo do ataque: `docker/attackers/coap-token-collision/attack.yaml`
- Artefatos da campanha: `experiments/60att_5runs_l0l1l2l3/iot_coap_token_collision`
