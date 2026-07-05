# ICMP Tunnel (`exf_icmp_tunnel`)

[Índice da campanha](README.md)

Na campanha `experiments/60att_5runs_l0l1l2l3`, este documento consolida a execução do ataque `exf_icmp_tunnel`. No catálogo local, o ataque é descrito como: TCP port 22 (SSH) tunnel over ICMP (pings). A documentação abaixo usa apenas artefatos já presentes no repositório, principalmente as tabelas e figuras de `experiments/60att_5runs_l0l1l2l3/exf_icmp_tunnel`.

## Metadados do ataque

| Campo | Valor |
| --- | --- |
| ID | `exf_icmp_tunnel` |
| Categoria | 5) Exfiltration and Tunneling |
| Subcategoria | 5.1 Exfiltration and Tunneling |
| Serviços alvo | ssh-server |
| Imagem | `attack-icmp-tunnel:latest` |
| Container | `attack-icmp-tunnel` |
| Runtime máximo do catálogo | 10 s |
| Parâmetros de intensidade | n/d |
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0011/](https://attack.mitre.org/tactics/TA0011/)<br>[https://attack.mitre.org/techniques/T1090/](https://attack.mitre.org/techniques/T1090/)<br>[https://attack.mitre.org/techniques/T1095/](https://attack.mitre.org/techniques/T1095/)<br>[https://attack.mitre.org/techniques/T1572/](https://attack.mitre.org/techniques/T1572/) |

## Resumo estatístico por nível

| Nível | Serviço | Runs | Amostras attack | Sucesso médio | Falha média | Lat p50/p95 ms | PCAP total MB | Dataset médio (min-max) | Exec média s | Extratores ok/total | CPU média/máx | Mem MB média |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | ssh | 5 | 195 | 100% | 0% | 8,49 / 10,01 | 0,3 | 1.333 (1.314-1.342) | 42,06 | 3/3 | 1,96% / 2,22% | 10,77 |
| L1 | ssh | 5 | 195 | 100% | 0% | 8,45 / 11,26 | 4,29 | 6.680 (6.602-6.726) | 42,55 | 3/3 | 13,77% / 16,26% | 13,01 |
| L2 | ssh | 5 | 196 | 100% | 0% | 8,16 / 9,32 | 4,3 | 6.698 (6.658-6.720) | 42,53 | 3/3 | 13,15% / 15,01% | 13,23 |
| L3 | ssh | 5 | 196 | 100% | 0% | 8,19 / 10,11 | 4,31 | 6.701 (6.684-6.712) | 42,53 | 3/3 | 13,3% / 15,29% | 13,04 |

## Estabilidade entre reexecuções

| Nível | Métrica | Runs | Média | Desvio | CV | Min | Max |
| --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | CPU média na fase attack | 5 | 1,96 | 0,12 | 6,06% | 1,79 | 2,12 |
| L0 | Linhas do dataset | 5 | 1.332,8 | 10,92 | 0,82% | 1.314 | 1.342 |
| L0 | Tempo de execução | 5 | 42,06 | 0,38 | 0,91% | 41,82 | 42,74 |
| L0 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L0 | Latência p95 censurada | 5 | 10,01 | 1,24 | 12,38% | 8,86 | 12,12 |
| L1 | CPU média na fase attack | 5 | 13,77 | 0,5 | 3,6% | 13,07 | 14,37 |
| L1 | Linhas do dataset | 5 | 6.680 | 48,12 | 0,72% | 6.602 | 6.726 |
| L1 | Tempo de execução | 5 | 42,55 | 0,06 | 0,15% | 42,45 | 42,61 |
| L1 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L1 | Latência p95 censurada | 5 | 11,26 | 1,68 | 14,89% | 8,95 | 13,29 |
| L2 | CPU média na fase attack | 5 | 13,15 | 0,2 | 1,5% | 12,87 | 13,41 |
| L2 | Linhas do dataset | 5 | 6.698,4 | 23,93 | 0,36% | 6.658 | 6.720 |
| L2 | Tempo de execução | 5 | 42,53 | 0,05 | 0,11% | 42,48 | 42,6 |
| L2 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L2 | Latência p95 censurada | 5 | 9,32 | 0,77 | 8,3% | 8,49 | 10,48 |
| L3 | CPU média na fase attack | 5 | 13,3 | 0,26 | 1,97% | 13 | 13,59 |
| L3 | Linhas do dataset | 5 | 6.701,2 | 11,8 | 0,18% | 6.684 | 6.712 |
| L3 | Tempo de execução | 5 | 42,53 | 0,05 | 0,11% | 42,5 | 42,62 |
| L3 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L3 | Latência p95 censurada | 5 | 10,11 | 1,37 | 13,58% | 8,75 | 11,74 |

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
<td><img src="../../assets/campaign_doc/exf_icmp_tunnel/F3_v1_timeseries_ssh_exf_icmp_tunnel_L0_run01.png" alt="Série temporal L0 run01" width="420"><br><sub>Série temporal L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/exf_icmp_tunnel/F3_v1_timeseries_ssh_exf_icmp_tunnel_L1_run01.png" alt="Série temporal L1 run01" width="420"><br><sub>Série temporal L1 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/exf_icmp_tunnel/F3_v1_timeseries_ssh_exf_icmp_tunnel_L2_run01.png" alt="Série temporal L2 run01" width="420"><br><sub>Série temporal L2 run01</sub></td>
<td><img src="../../assets/campaign_doc/exf_icmp_tunnel/F3_v1_timeseries_ssh_exf_icmp_tunnel_L3_run01.png" alt="Série temporal L3 run01" width="420"><br><sub>Série temporal L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/exf_icmp_tunnel/F5_resources_ssh_exf_icmp_tunnel_L0_run01.png" alt="Recursos L0 run01" width="420"><br><sub>Recursos L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/exf_icmp_tunnel/F5_resources_ssh_exf_icmp_tunnel_L3_run01.png" alt="Recursos L3 run01" width="420"><br><sub>Recursos L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/exf_icmp_tunnel/F4_v2_failrate_ssh_exf_icmp_tunnel_L0.png" alt="Taxa de falha L0" width="420"><br><sub>Taxa de falha L0</sub></td>
<td><img src="../../assets/campaign_doc/exf_icmp_tunnel/F4_v2_failrate_ssh_exf_icmp_tunnel_L3.png" alt="Taxa de falha L3" width="420"><br><sub>Taxa de falha L3</sub></td>
</tr>
</table>

## Fontes utilizadas

- Catálogo do ataque: `docker/attackers/icmp-tunnel/attack.yaml`
- Artefatos da campanha: `experiments/60att_5runs_l0l1l2l3/exf_icmp_tunnel`
