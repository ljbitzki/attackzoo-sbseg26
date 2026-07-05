# DNS Tunneling (`exf_dns_tunneling`)

[Índice da campanha](README.md)

Na campanha `experiments/60att_5runs_l0l1l2l3`, este documento consolida a execução do ataque `exf_dns_tunneling`. No catálogo local, o ataque é descrito como: DNS tunneling exfiltration behavior through random domain name resolution. A documentação abaixo usa apenas artefatos já presentes no repositório, principalmente as tabelas e figuras de `experiments/60att_5runs_l0l1l2l3/exf_dns_tunneling`.

## Metadados do ataque

| Campo | Valor |
| --- | --- |
| ID | `exf_dns_tunneling` |
| Categoria | 5) Exfiltration and Tunneling |
| Subcategoria | 5.1 Exfiltration and Tunneling |
| Serviços alvo | external/local DNS resolver |
| Imagem | `attack-dns-tunneling:latest` |
| Container | `attack-dns-tunneling` |
| Runtime máximo do catálogo | 10 s |
| Parâmetros de intensidade | duration_s, count, delay_ms, payload_size |
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0010/](https://attack.mitre.org/tactics/TA0010/)<br>[https://attack.mitre.org/tactics/TA0011/](https://attack.mitre.org/tactics/TA0011/)<br>[https://attack.mitre.org/techniques/T1048/](https://attack.mitre.org/techniques/T1048/)<br>[https://attack.mitre.org/techniques/T1048/003/](https://attack.mitre.org/techniques/T1048/003/)<br>[https://attack.mitre.org/techniques/T1071/](https://attack.mitre.org/techniques/T1071/)<br>[https://attack.mitre.org/techniques/T1071/004/](https://attack.mitre.org/techniques/T1071/004/) |

## Resumo estatístico por nível

| Nível | Serviço | Runs | Amostras attack | Sucesso médio | Falha média | Lat p50/p95 ms | PCAP total MB | Dataset médio (min-max) | Exec média s | Extratores ok/total | CPU média/máx | Mem MB média |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | http | 5 | 200 | 100% | 0% | 4,13 / 4,76 | 5,06 | 9.640 (9.604-9.760) | 43,06 | 3/3 | 0,64% / 0,72% | 120,93 |
| L1 | http | 5 | 200 | 100% | 0% | 4,06 / 5,16 | 5,28 | 10.293 (10.282-10.302) | 43,06 | 3/3 | 0,63% / 0,74% | 123,07 |
| L2 | http | 5 | 200 | 100% | 0% | 4,36 / 5,5 | 5,28 | 10.305 (10.294-10.312) | 43,07 | 3/3 | 0,71% / 0,84% | 125,34 |
| L3 | http | 5 | 200 | 100% | 0% | 4,14 / 4,92 | 5,28 | 10.307 (10.302-10.310) | 43,08 | 3/3 | 0,65% / 0,77% | 127,32 |

## Estabilidade entre reexecuções

| Nível | Métrica | Runs | Média | Desvio | CV | Min | Max |
| --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | CPU média na fase attack | 5 | 0,64 | 0,07 | 11,03% | 0,59 | 0,76 |
| L0 | Linhas do dataset | 5 | 9.640,4 | 67,12 | 0,7% | 9.604 | 9.760 |
| L0 | Tempo de execução | 5 | 43,06 | 0,41 | 0,95% | 42,84 | 43,79 |
| L0 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L0 | Latência p95 censurada | 5 | 4,76 | 0,61 | 12,89% | 4,36 | 5,84 |
| L1 | CPU média na fase attack | 5 | 0,63 | 0,02 | 3,65% | 0,6 | 0,65 |
| L1 | Linhas do dataset | 5 | 10.293,2 | 7,69 | 0,07% | 10.282 | 10.302 |
| L1 | Tempo de execução | 5 | 43,06 | 0,07 | 0,16% | 43 | 43,17 |
| L1 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L1 | Latência p95 censurada | 5 | 5,16 | 0,83 | 16,18% | 4,38 | 6,52 |
| L2 | CPU média na fase attack | 5 | 0,71 | 0,11 | 15,06% | 0,59 | 0,82 |
| L2 | Linhas do dataset | 5 | 10.304,8 | 7,01 | 0,07% | 10.294 | 10.312 |
| L2 | Tempo de execução | 5 | 43,07 | 0,06 | 0,13% | 42,99 | 43,14 |
| L2 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L2 | Latência p95 censurada | 5 | 5,5 | 1,12 | 20,31% | 4,27 | 6,97 |
| L3 | CPU média na fase attack | 5 | 0,65 | 0,06 | 8,88% | 0,61 | 0,75 |
| L3 | Linhas do dataset | 5 | 10.306,8 | 3,63 | 0,04% | 10.302 | 10.310 |
| L3 | Tempo de execução | 5 | 43,08 | 0,02 | 0,05% | 43,04 | 43,09 |
| L3 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L3 | Latência p95 censurada | 5 | 4,92 | 0,71 | 14,4% | 4,26 | 5,97 |

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
<td><img src="../../assets/campaign_doc/exf_dns_tunneling/F3_v1_timeseries_http_exf_dns_tunneling_L0_run01.png" alt="Série temporal L0 run01" width="420"><br><sub>Série temporal L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/exf_dns_tunneling/F3_v1_timeseries_http_exf_dns_tunneling_L1_run01.png" alt="Série temporal L1 run01" width="420"><br><sub>Série temporal L1 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/exf_dns_tunneling/F3_v1_timeseries_http_exf_dns_tunneling_L2_run01.png" alt="Série temporal L2 run01" width="420"><br><sub>Série temporal L2 run01</sub></td>
<td><img src="../../assets/campaign_doc/exf_dns_tunneling/F3_v1_timeseries_http_exf_dns_tunneling_L3_run01.png" alt="Série temporal L3 run01" width="420"><br><sub>Série temporal L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/exf_dns_tunneling/F5_resources_http_exf_dns_tunneling_L0_run01.png" alt="Recursos L0 run01" width="420"><br><sub>Recursos L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/exf_dns_tunneling/F5_resources_http_exf_dns_tunneling_L3_run01.png" alt="Recursos L3 run01" width="420"><br><sub>Recursos L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/exf_dns_tunneling/F4_v2_failrate_http_exf_dns_tunneling_L0.png" alt="Taxa de falha L0" width="420"><br><sub>Taxa de falha L0</sub></td>
<td><img src="../../assets/campaign_doc/exf_dns_tunneling/F4_v2_failrate_http_exf_dns_tunneling_L3.png" alt="Taxa de falha L3" width="420"><br><sub>Taxa de falha L3</sub></td>
</tr>
</table>

## Fontes utilizadas

- Catálogo do ataque: `docker/attackers/dns-tunneling/attack.yaml`
- Artefatos da campanha: `experiments/60att_5runs_l0l1l2l3/exf_dns_tunneling`
