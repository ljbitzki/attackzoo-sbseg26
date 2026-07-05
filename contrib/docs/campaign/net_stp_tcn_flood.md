# STP TCN Flood (`net_stp_tcn_flood`)

[Índice da campanha](README.md)

Na campanha `experiments/60att_5runs_l0l1l2l3`, este documento consolida a execução do ataque `net_stp_tcn_flood`. No catálogo local, o ataque é descrito como: BPDU (Bridge Protocol Data Unit) packet flood with STP topology change information and random MAC addresses. A documentação abaixo usa apenas artefatos já presentes no repositório, principalmente as tabelas e figuras de `experiments/60att_5runs_l0l1l2l3/net_stp_tcn_flood`.

## Metadados do ataque

| Campo | Valor |
| --- | --- |
| ID | `net_stp_tcn_flood` |
| Categoria | 2) Network Interception and Exploitation |
| Subcategoria | 2.1 L2/L3 |
| Serviços alvo | local network |
| Imagem | `attack-stp-tcn-flood:latest` |
| Container | `attack-stp-tcn-flood` |
| Runtime máximo do catálogo | 10 s |
| Parâmetros de intensidade | n/d |
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0040/](https://attack.mitre.org/tactics/TA0040/)<br>[https://attack.mitre.org/techniques/T1498/](https://attack.mitre.org/techniques/T1498/)<br>[https://attack.mitre.org/techniques/T1498/001/](https://attack.mitre.org/techniques/T1498/001/)<br>[https://attack.mitre.org/techniques/T1565/](https://attack.mitre.org/techniques/T1565/)<br>[https://attack.mitre.org/techniques/T1565/002/](https://attack.mitre.org/techniques/T1565/002/) |

## Resumo estatístico por nível

| Nível | Serviço | Runs | Amostras attack | Sucesso médio | Falha média | Lat p50/p95 ms | PCAP total MB | Dataset médio (min-max) | Exec média s | Extratores ok/total | CPU média/máx | Mem MB média |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | http | 5 | 200 | 100% | 0% | 5,29 / 6,81 | 5,02 | 9.552 (9.470-9.722) | 40 | 2/3 | 0,17% / 0,99% | 148,81 |
| L1 | http | 1 | 40 | 100% | 0% | 6,48 / 8,43 | 2,77 | 95.674 (95.674-95.674) | 40 | 2/3 | 5,26% / 64,73% | 150,04 |

## Estabilidade entre reexecuções

| Nível | Métrica | Runs | Média | Desvio | CV | Min | Max |
| --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | Linhas do dataset | 5 | 9.551,6 | 98,5 | 1,03% | 9.470 | 9.722 |
| L0 | Tempo de execução | 5 | 40 | 0 | 0% | 40 | 40 |
| L0 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L0 | Latência p95 censurada | 5 | 6,81 | 0,78 | 11,44% | 5,73 | 7,8 |
| L0 | CPU média na fase attack | 5 | 0,17 | 0,05 | 29,26% | 0,12 | 0,23 |
| L1 | Linhas do dataset | 1 | 95.674 | 0 | 0% | 95.674 | 95.674 |
| L1 | Tempo de execução | 1 | 40 | 0 | 0% | 40 | 40 |
| L1 | Falha na fase attack | 1 | 0 | 0 | n/d | 0 | 0 |
| L1 | Latência p95 censurada | 1 | 8,43 | 0 | 0% | 8,43 | 8,43 |
| L1 | CPU média na fase attack | 1 | 5,26 | 0 | 0% | 5,26 | 5,26 |

## Validação de artefatos

Não foi encontrada tabela agregada de validação de artefatos para este ataque.

## Figuras selecionadas

Nenhuma figura agregada foi encontrada em `reports/figs` para este ataque.

## Fontes utilizadas

- Catálogo do ataque: `docker/attackers/stp-tcn-flood/attack.yaml`
- Artefatos da campanha: `experiments/60att_5runs_l0l1l2l3/net_stp_tcn_flood`
