# SSH Bruteforce (`bf_ssh`)

[Índice da campanha](README.md)

Na campanha `experiments/60att_5runs_l0l1l2l3`, este documento consolida a execução do ataque `bf_ssh`. No catálogo local, o ataque é descrito como: SSH authentication brute force. A documentação abaixo usa apenas artefatos já presentes no repositório, principalmente as tabelas e figuras de `experiments/60att_5runs_l0l1l2l3/bf_ssh`.

## Metadados do ataque

| Campo | Valor |
| --- | --- |
| ID | `bf_ssh` |
| Categoria | 4) Brute Force Against Remote Access Applications |
| Subcategoria | 4.1 Brute Force |
| Serviços alvo | ssh-server |
| Imagem | `attack-ssh-bruteforce:latest` |
| Container | `attack-ssh-bruteforce` |
| Runtime máximo do catálogo | 10 s |
| Parâmetros de intensidade | n/d |
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0006/](https://attack.mitre.org/tactics/TA0006/)<br>[https://attack.mitre.org/techniques/T1110/](https://attack.mitre.org/techniques/T1110/)<br>[https://attack.mitre.org/techniques/T1110/001/](https://attack.mitre.org/techniques/T1110/001/) |

## Resumo estatístico por nível

| Nível | Serviço | Runs | Amostras attack | Sucesso médio | Falha média | Lat p50/p95 ms | PCAP total MB | Dataset médio (min-max) | Exec média s | Extratores ok/total | CPU média/máx | Mem MB média |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | ssh | 5 | 195 | 100% | 0% | 8,35 / 8,95 | 0,3 | 1.327 (1.316-1.334) | 42,11 | 3/3 | 1,92% / 2% | 9,68 |
| L1 | ssh | 5 | 200 | 68,5% | 31,5% | 9,17 / 2.000 | 0,81 | 2.485 (2.326-2.552) | 42,03 | 3/3 | 25,22% / 86,38% | 37,96 |
| L2 | ssh | 5 | 199 | 73,4% | 26,6% | 9,34 / 2.000 | 0,84 | 2.551 (2.500-2.618) | 42,07 | 3/3 | 26,97% / 96,56% | 40,86 |
| L3 | ssh | 5 | 199 | 70,4% | 29,6% | 8,93 / 2.000 | 0,84 | 2.538 (2.478-2.600) | 42,09 | 3/3 | 26,83% / 94,11% | 42,03 |

## Estabilidade entre reexecuções

| Nível | Métrica | Runs | Média | Desvio | CV | Min | Max |
| --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | CPU média na fase attack | 5 | 1,92 | 0,02 | 1,26% | 1,9 | 1,96 |
| L0 | Linhas do dataset | 5 | 1.326,8 | 8,2 | 0,62% | 1.316 | 1.334 |
| L0 | Tempo de execução | 5 | 42,11 | 0,81 | 1,92% | 41,73 | 43,56 |
| L0 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L0 | Latência p95 censurada | 5 | 8,95 | 0,2 | 2,23% | 8,61 | 9,08 |
| L1 | CPU média na fase attack | 5 | 25,22 | 4,19 | 16,61% | 20,65 | 30,59 |
| L1 | Linhas do dataset | 5 | 2.484,8 | 92,74 | 3,73% | 2.326 | 2.552 |
| L1 | Tempo de execução | 5 | 42,03 | 0,03 | 0,08% | 42 | 42,08 |
| L1 | Falha na fase attack | 5 | 31,5 | 9,45 | 30,01% | 15 | 37,5 |
| L1 | Latência p95 censurada | 5 | 2.000 | 0 | 0% | 2.000 | 2.000 |
| L2 | CPU média na fase attack | 5 | 26,97 | 3,13 | 11,61% | 23,53 | 30,65 |
| L2 | Linhas do dataset | 5 | 2.550,8 | 48,76 | 1,91% | 2.500 | 2.618 |
| L2 | Tempo de execução | 5 | 42,07 | 0,11 | 0,25% | 42,01 | 42,26 |
| L2 | Falha na fase attack | 5 | 26,58 | 7,89 | 29,67% | 15,38 | 37,5 |
| L2 | Latência p95 censurada | 5 | 2.000 | 0 | 0% | 2.000 | 2.000 |
| L3 | CPU média na fase attack | 5 | 26,83 | 4,19 | 15,63% | 22,3 | 32,16 |
| L3 | Linhas do dataset | 5 | 2.538 | 48,31 | 1,9% | 2.478 | 2.600 |
| L3 | Tempo de execução | 5 | 42,09 | 0,11 | 0,27% | 41,98 | 42,23 |
| L3 | Falha na fase attack | 5 | 29,63 | 2,48 | 8,36% | 25,64 | 32,5 |
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
<td><img src="../../assets/campaign_doc/bf_ssh/F3_v1_timeseries_ssh_bf_ssh_L0_run01.png" alt="Série temporal L0 run01" width="420"><br><sub>Série temporal L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/bf_ssh/F3_v1_timeseries_ssh_bf_ssh_L1_run01.png" alt="Série temporal L1 run01" width="420"><br><sub>Série temporal L1 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/bf_ssh/F3_v1_timeseries_ssh_bf_ssh_L2_run01.png" alt="Série temporal L2 run01" width="420"><br><sub>Série temporal L2 run01</sub></td>
<td><img src="../../assets/campaign_doc/bf_ssh/F3_v1_timeseries_ssh_bf_ssh_L3_run01.png" alt="Série temporal L3 run01" width="420"><br><sub>Série temporal L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/bf_ssh/F5_resources_ssh_bf_ssh_L0_run01.png" alt="Recursos L0 run01" width="420"><br><sub>Recursos L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/bf_ssh/F5_resources_ssh_bf_ssh_L3_run01.png" alt="Recursos L3 run01" width="420"><br><sub>Recursos L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/bf_ssh/F4_v2_failrate_ssh_bf_ssh_L0.png" alt="Taxa de falha L0" width="420"><br><sub>Taxa de falha L0</sub></td>
<td><img src="../../assets/campaign_doc/bf_ssh/F4_v2_failrate_ssh_bf_ssh_L3.png" alt="Taxa de falha L3" width="420"><br><sub>Taxa de falha L3</sub></td>
</tr>
</table>

## Fontes utilizadas

- Catálogo do ataque: `docker/attackers/ssh-bruteforce/attack.yaml`
- Artefatos da campanha: `experiments/60att_5runs_l0l1l2l3/bf_ssh`
