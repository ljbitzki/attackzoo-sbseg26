# SYN Flood (`dos_syn_flood`)

[Índice da campanha](README.md)

Na campanha `experiments/60att_5runs_l0l1l2l3`, este documento consolida a execução do ataque `dos_syn_flood`. No catálogo local, o ataque é descrito como: TCP packet flood with the SYN flag set. A documentação abaixo usa apenas artefatos já presentes no repositório, principalmente as tabelas e figuras de `experiments/60att_5runs_l0l1l2l3/dos_syn_flood`.

## Metadados do ataque

| Campo | Valor |
| --- | --- |
| ID | `dos_syn_flood` |
| Categoria | 6) Denial of Service and Impact |
| Subcategoria | 6.1 Network/transport floods (ICMP/TCP/UDP) |
| Serviços alvo | target IP service |
| Imagem | `attack-syn-flood:latest` |
| Container | `attack-syn-flood` |
| Runtime máximo do catálogo | 10 s |
| Parâmetros de intensidade | duration_s, count, rate_pps, delay_ms, payload_size |
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0040/](https://attack.mitre.org/tactics/TA0040/)<br>[https://attack.mitre.org/techniques/T1498/](https://attack.mitre.org/techniques/T1498/)<br>[https://attack.mitre.org/techniques/T1498/001/](https://attack.mitre.org/techniques/T1498/001/) |

## Resumo estatístico por nível

| Nível | Serviço | Runs | Amostras attack | Sucesso médio | Falha média | Lat p50/p95 ms | PCAP total MB | Dataset médio (min-max) | Exec média s | Extratores ok/total | CPU média/máx | Mem MB média |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | http | 5 | 200 | 100% | 0% | 4,06 / 8,03 | 1,67 | 3.161 (3.160-3.164) | 42,34 | 3/3 | 0,6% / 0,65% | 104,03 |
| L1 | http | 5 | 200 | 100% | 0% | 4,45 / 7,75 | 2,36 | 6.952 (6.278-7.212) | 42,61 | 3/3 | 0,7% / 0,8% | 106,13 |
| L2 | http | 5 | 200 | 100% | 0% | 4,48 / 5,76 | 2,38 | 7.012 (6.872-7.194) | 42,51 | 3/3 | 0,69% / 0,83% | 108,25 |
| L3 | http | 5 | 200 | 100% | 0% | 4,14 / 4,97 | 2,4 | 7.136 (7.046-7.192) | 42,54 | 3/3 | 0,64% / 0,74% | 110,43 |

## Estabilidade entre reexecuções

| Nível | Métrica | Runs | Média | Desvio | CV | Min | Max |
| --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | CPU média na fase attack | 5 | 0,6 | 0,04 | 6,2% | 0,55 | 0,63 |
| L0 | Linhas do dataset | 5 | 3.161,2 | 1,79 | 0,06% | 3.160 | 3.164 |
| L0 | Tempo de execução | 5 | 42,34 | 0,58 | 1,38% | 42,06 | 43,38 |
| L0 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L0 | Latência p95 censurada | 5 | 8,03 | 6,83 | 85,02% | 4,62 | 20,24 |
| L1 | CPU média na fase attack | 5 | 0,7 | 0,12 | 17,13% | 0,58 | 0,86 |
| L1 | Linhas do dataset | 5 | 6.952,4 | 385,23 | 5,54% | 6.278 | 7.212 |
| L1 | Tempo de execução | 5 | 42,61 | 0,11 | 0,26% | 42,43 | 42,7 |
| L1 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L1 | Latência p95 censurada | 5 | 7,75 | 5 | 64,51% | 4,1 | 16,21 |
| L2 | CPU média na fase attack | 5 | 0,69 | 0,09 | 12,48% | 0,61 | 0,81 |
| L2 | Linhas do dataset | 5 | 7.011,6 | 116,69 | 1,66% | 6.872 | 7.194 |
| L2 | Tempo de execução | 5 | 42,51 | 0,06 | 0,13% | 42,44 | 42,6 |
| L2 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L2 | Latência p95 censurada | 5 | 5,76 | 1,23 | 21,3% | 4,33 | 7,13 |
| L3 | CPU média na fase attack | 5 | 0,64 | 0,04 | 5,84% | 0,59 | 0,69 |
| L3 | Linhas do dataset | 5 | 7.135,6 | 57,61 | 0,81% | 7.046 | 7.192 |
| L3 | Tempo de execução | 5 | 42,54 | 0,08 | 0,2% | 42,43 | 42,66 |
| L3 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L3 | Latência p95 censurada | 5 | 4,97 | 0,76 | 15,39% | 4,29 | 5,86 |

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
<td><img src="../../assets/campaign_doc/dos_syn_flood/F3_v1_timeseries_http_dos_syn_flood_L0_run01.png" alt="Série temporal L0 run01" width="420"><br><sub>Série temporal L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/dos_syn_flood/F3_v1_timeseries_http_dos_syn_flood_L1_run01.png" alt="Série temporal L1 run01" width="420"><br><sub>Série temporal L1 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/dos_syn_flood/F3_v1_timeseries_http_dos_syn_flood_L2_run01.png" alt="Série temporal L2 run01" width="420"><br><sub>Série temporal L2 run01</sub></td>
<td><img src="../../assets/campaign_doc/dos_syn_flood/F3_v1_timeseries_http_dos_syn_flood_L3_run01.png" alt="Série temporal L3 run01" width="420"><br><sub>Série temporal L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/dos_syn_flood/F5_resources_http_dos_syn_flood_L0_run01.png" alt="Recursos L0 run01" width="420"><br><sub>Recursos L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/dos_syn_flood/F5_resources_http_dos_syn_flood_L3_run01.png" alt="Recursos L3 run01" width="420"><br><sub>Recursos L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/dos_syn_flood/F4_v2_failrate_http_dos_syn_flood_L0.png" alt="Taxa de falha L0" width="420"><br><sub>Taxa de falha L0</sub></td>
<td><img src="../../assets/campaign_doc/dos_syn_flood/F4_v2_failrate_http_dos_syn_flood_L3.png" alt="Taxa de falha L3" width="420"><br><sub>Taxa de falha L3</sub></td>
</tr>
</table>

## Fontes utilizadas

- Catálogo do ataque: `docker/attackers/syn-flood/attack.yaml`
- Artefatos da campanha: `experiments/60att_5runs_l0l1l2l3/dos_syn_flood`
