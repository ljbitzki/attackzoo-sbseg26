# Ping Sweep (`recon_ping_sweep`)

[Índice da campanha](README.md)

Na campanha `experiments/60att_5runs_l0l1l2l3`, este documento consolida a execução do ataque `recon_ping_sweep`. No catálogo local, o ataque é descrito como: ICMP sweep for host discovery. A documentação abaixo usa apenas artefatos já presentes no repositório, principalmente as tabelas e figuras de `experiments/60att_5runs_l0l1l2l3/recon_ping_sweep`.

## Metadados do ataque

| Campo | Valor |
| --- | --- |
| ID | `recon_ping_sweep` |
| Categoria | 1) Reconnaissance and Discovery |
| Subcategoria | 1.1 Network-level host discovery |
| Serviços alvo | local network |
| Imagem | `attack-ping-sweep:latest` |
| Container | `attack-ping-sweep` |
| Runtime máximo do catálogo | 10 s |
| Parâmetros de intensidade | n/d |
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0043/](https://attack.mitre.org/tactics/TA0043/)<br>[https://attack.mitre.org/tactics/TA0007/](https://attack.mitre.org/tactics/TA0007/)<br>[https://attack.mitre.org/techniques/T1590/](https://attack.mitre.org/techniques/T1590/)<br>[https://attack.mitre.org/techniques/T1595/](https://attack.mitre.org/techniques/T1595/)<br>[https://attack.mitre.org/techniques/T1595/001/](https://attack.mitre.org/techniques/T1595/001/)<br>[https://attack.mitre.org/techniques/T1018/](https://attack.mitre.org/techniques/T1018/) |

## Resumo estatístico por nível

| Nível | Serviço | Runs | Amostras attack | Sucesso médio | Falha média | Lat p50/p95 ms | PCAP total MB | Dataset médio (min-max) | Exec média s | Extratores ok/total | CPU média/máx | Mem MB média |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | http | 5 | 200 | 100% | 0% | 4,45 / 5,79 | 5,06 | 9.628 (9.600-9.718) | 43,13 | 3/3 | 0,73% / 0,88% | 710,32 |
| L1 | http | 5 | 200 | 100% | 0% | 5,28 / 6,9 | 17,63 | 92.014 (89.990-94.078) | 49,53 | 3/3 | 0,79% / 0,98% | 712,56 |
| L2 | http | 5 | 199 | 100% | 0% | 4,69 / 5,93 | 17,32 | 90.024 (78.976-94.240) | 49,28 | 3/3 | 0,71% / 0,8% | 714,83 |
| L3 | http | 5 | 200 | 100% | 0% | 4,77 / 6,29 | 17,02 | 88.050 (81.228-91.574) | 49,14 | 3/3 | 0,78% / 0,97% | 716,9 |

## Estabilidade entre reexecuções

| Nível | Métrica | Runs | Média | Desvio | CV | Min | Max |
| --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | CPU média na fase attack | 5 | 0,73 | 0,09 | 12,32% | 0,63 | 0,84 |
| L0 | Linhas do dataset | 5 | 9.628,4 | 50,29 | 0,52% | 9.600 | 9.718 |
| L0 | Tempo de execução | 5 | 43,13 | 0,38 | 0,87% | 42,8 | 43,76 |
| L0 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L0 | Latência p95 censurada | 5 | 5,79 | 0,65 | 11,15% | 4,65 | 6,14 |
| L1 | CPU média na fase attack | 5 | 0,79 | 0,13 | 16,77% | 0,68 | 1,02 |
| L1 | Linhas do dataset | 5 | 92.014,4 | 1.577,72 | 1,71% | 89.990 | 94.078 |
| L1 | Tempo de execução | 5 | 49,53 | 0,25 | 0,5% | 49,23 | 49,89 |
| L1 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L1 | Latência p95 censurada | 5 | 6,9 | 0,98 | 14,16% | 5,91 | 8,34 |
| L2 | CPU média na fase attack | 5 | 0,71 | 0,09 | 12,53% | 0,64 | 0,86 |
| L2 | Linhas do dataset | 5 | 90.023,6 | 6.338,63 | 7,04% | 78.976 | 94.240 |
| L2 | Tempo de execução | 5 | 49,28 | 0,47 | 0,96% | 48,47 | 49,68 |
| L2 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L2 | Latência p95 censurada | 5 | 5,93 | 1,24 | 20,97% | 4,52 | 7,5 |
| L3 | CPU média na fase attack | 5 | 0,78 | 0,09 | 11,55% | 0,68 | 0,9 |
| L3 | Linhas do dataset | 5 | 88.050 | 4.086,29 | 4,64% | 81.228 | 91.574 |
| L3 | Tempo de execução | 5 | 49,14 | 0,37 | 0,75% | 48,52 | 49,49 |
| L3 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L3 | Latência p95 censurada | 5 | 6,29 | 0,8 | 12,74% | 5,18 | 7,1 |

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
<td><img src="../../assets/campaign_doc/recon_ping_sweep/F3_v1_timeseries_http_recon_ping_sweep_L0_run01.png" alt="Série temporal L0 run01" width="420"><br><sub>Série temporal L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/recon_ping_sweep/F3_v1_timeseries_http_recon_ping_sweep_L1_run01.png" alt="Série temporal L1 run01" width="420"><br><sub>Série temporal L1 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/recon_ping_sweep/F3_v1_timeseries_http_recon_ping_sweep_L2_run01.png" alt="Série temporal L2 run01" width="420"><br><sub>Série temporal L2 run01</sub></td>
<td><img src="../../assets/campaign_doc/recon_ping_sweep/F3_v1_timeseries_http_recon_ping_sweep_L3_run01.png" alt="Série temporal L3 run01" width="420"><br><sub>Série temporal L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/recon_ping_sweep/F5_resources_http_recon_ping_sweep_L0_run01.png" alt="Recursos L0 run01" width="420"><br><sub>Recursos L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/recon_ping_sweep/F5_resources_http_recon_ping_sweep_L3_run01.png" alt="Recursos L3 run01" width="420"><br><sub>Recursos L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/recon_ping_sweep/F4_v2_failrate_http_recon_ping_sweep_L0.png" alt="Taxa de falha L0" width="420"><br><sub>Taxa de falha L0</sub></td>
<td><img src="../../assets/campaign_doc/recon_ping_sweep/F4_v2_failrate_http_recon_ping_sweep_L3.png" alt="Taxa de falha L3" width="420"><br><sub>Taxa de falha L3</sub></td>
</tr>
</table>

## Fontes utilizadas

- Catálogo do ataque: `docker/attackers/ping-sweep/attack.yaml`
- Artefatos da campanha: `experiments/60att_5runs_l0l1l2l3/recon_ping_sweep`
