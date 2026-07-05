# DoS HTTP Simple (`dos_http_simple`)

[Índice da campanha](README.md)

Na campanha `experiments/60att_5runs_l0l1l2l3`, este documento consolida a execução do ataque `dos_http_simple`. No catálogo local, o ataque é descrito como: Simple HTTP application DoS. A documentação abaixo usa apenas artefatos já presentes no repositório, principalmente as tabelas e figuras de `experiments/60att_5runs_l0l1l2l3/dos_http_simple`.

## Metadados do ataque

| Campo | Valor |
| --- | --- |
| ID | `dos_http_simple` |
| Categoria | 6) Denial of Service and Impact |
| Subcategoria | 6.2 Application-layer DoS |
| Serviços alvo | http-server |
| Imagem | `attack-dos-http-simple:latest` |
| Container | `attack-dos-http-simple` |
| Runtime máximo do catálogo | 10 s |
| Parâmetros de intensidade | duration_s, count, concurrency, delay_ms, payload_size |
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0040/](https://attack.mitre.org/tactics/TA0040/)<br>[https://attack.mitre.org/techniques/T1499/](https://attack.mitre.org/techniques/T1499/)<br>[https://attack.mitre.org/techniques/T1499/002/](https://attack.mitre.org/techniques/T1499/002/) |

## Resumo estatístico por nível

| Nível | Serviço | Runs | Amostras attack | Sucesso médio | Falha média | Lat p50/p95 ms | PCAP total MB | Dataset médio (min-max) | Exec média s | Extratores ok/total | CPU média/máx | Mem MB média |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | http | 5 | 200 | 100% | 0% | 4,13 / 5,18 | 1,67 | 3.168 (3.160-3.202) | 42,23 | 3/3 | 0,62% / 0,77% | 214,54 |
| L1 | http | 5 | 200 | 100% | 0% | 4,17 / 5,77 | 2,94 | 6.848 (6.800-6.880) | 42,57 | 3/3 | 1,04% / 1,19% | 217,23 |
| L2 | http | 5 | 200 | 100% | 0% | 4,36 / 5,73 | 2,93 | 6.832 (6.780-6.880) | 42,66 | 3/3 | 1,08% / 1,26% | 220,35 |
| L3 | http | 5 | 200 | 100% | 0% | 4,41 / 6,35 | 2,93 | 6.828 (6.740-6.882) | 42,72 | 3/3 | 1,12% / 1,34% | 223,4 |

## Estabilidade entre reexecuções

| Nível | Métrica | Runs | Média | Desvio | CV | Min | Max |
| --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | CPU média na fase attack | 5 | 0,62 | 0,06 | 9,31% | 0,53 | 0,69 |
| L0 | Linhas do dataset | 5 | 3.168,4 | 18,78 | 0,59% | 3.160 | 3.202 |
| L0 | Tempo de execução | 5 | 42,23 | 0,34 | 0,81% | 42,04 | 42,84 |
| L0 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L0 | Latência p95 censurada | 5 | 5,18 | 0,68 | 13,12% | 4,53 | 6,13 |
| L1 | CPU média na fase attack | 5 | 1,04 | 0,03 | 3,12% | 0,98 | 1,07 |
| L1 | Linhas do dataset | 5 | 6.848,4 | 33,36 | 0,49% | 6.800 | 6.880 |
| L1 | Tempo de execução | 5 | 42,57 | 0,04 | 0,09% | 42,51 | 42,62 |
| L1 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L1 | Latência p95 censurada | 5 | 5,77 | 1,07 | 18,46% | 4,69 | 7,53 |
| L2 | CPU média na fase attack | 5 | 1,08 | 0,05 | 4,93% | 1,02 | 1,13 |
| L2 | Linhas do dataset | 5 | 6.832 | 50,2 | 0,73% | 6.780 | 6.880 |
| L2 | Tempo de execução | 5 | 42,66 | 0,08 | 0,2% | 42,57 | 42,76 |
| L2 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L2 | Latência p95 censurada | 5 | 5,73 | 0,84 | 14,64% | 4,96 | 7,02 |
| L3 | CPU média na fase attack | 5 | 1,12 | 0,06 | 5,4% | 1,05 | 1,2 |
| L3 | Linhas do dataset | 5 | 6.828,4 | 64,6 | 0,95% | 6.740 | 6.882 |
| L3 | Tempo de execução | 5 | 42,72 | 0,08 | 0,2% | 42,63 | 42,84 |
| L3 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L3 | Latência p95 censurada | 5 | 6,35 | 0,45 | 7,05% | 5,7 | 6,83 |

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
<td><img src="../../assets/campaign_doc/dos_http_simple/F3_v1_timeseries_http_dos_http_simple_L0_run01.png" alt="Série temporal L0 run01" width="420"><br><sub>Série temporal L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/dos_http_simple/F3_v1_timeseries_http_dos_http_simple_L1_run01.png" alt="Série temporal L1 run01" width="420"><br><sub>Série temporal L1 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/dos_http_simple/F3_v1_timeseries_http_dos_http_simple_L2_run01.png" alt="Série temporal L2 run01" width="420"><br><sub>Série temporal L2 run01</sub></td>
<td><img src="../../assets/campaign_doc/dos_http_simple/F3_v1_timeseries_http_dos_http_simple_L3_run01.png" alt="Série temporal L3 run01" width="420"><br><sub>Série temporal L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/dos_http_simple/F5_resources_http_dos_http_simple_L0_run01.png" alt="Recursos L0 run01" width="420"><br><sub>Recursos L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/dos_http_simple/F5_resources_http_dos_http_simple_L3_run01.png" alt="Recursos L3 run01" width="420"><br><sub>Recursos L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/dos_http_simple/F4_v2_failrate_http_dos_http_simple_L0.png" alt="Taxa de falha L0" width="420"><br><sub>Taxa de falha L0</sub></td>
<td><img src="../../assets/campaign_doc/dos_http_simple/F4_v2_failrate_http_dos_http_simple_L3.png" alt="Taxa de falha L3" width="420"><br><sub>Taxa de falha L3</sub></td>
</tr>
</table>

## Fontes utilizadas

- Catálogo do ataque: `docker/attackers/dos-http-simple/attack.yaml`
- Artefatos da campanha: `experiments/60att_5runs_l0l1l2l3/dos_http_simple`
