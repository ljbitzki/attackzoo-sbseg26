# CDP Table Flood (`net_cdp_table_flood`)

[Índice da campanha](README.md)

Na campanha `experiments/60att_5runs_l0l1l2l3`, este documento consolida a execução do ataque `net_cdp_table_flood`. No catálogo local, o ataque é descrito como: CDP (Cisco Discovery Protocol) table flood on the local network. A documentação abaixo usa apenas artefatos já presentes no repositório, principalmente as tabelas e figuras de `experiments/60att_5runs_l0l1l2l3/net_cdp_table_flood`.

## Metadados do ataque

| Campo | Valor |
| --- | --- |
| ID | `net_cdp_table_flood` |
| Categoria | 2) Network Interception and Exploitation |
| Subcategoria | 2.1 L2/L3 |
| Serviços alvo | local network |
| Imagem | `attack-cdp-table-flood:latest` |
| Container | `attack-cdp-table-flood` |
| Runtime máximo do catálogo | 10 s |
| Parâmetros de intensidade | n/d |
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0040/](https://attack.mitre.org/tactics/TA0040/)<br>[https://attack.mitre.org/techniques/T1498/](https://attack.mitre.org/techniques/T1498/)<br>[https://attack.mitre.org/techniques/T1498/001/](https://attack.mitre.org/techniques/T1498/001/) |

## Resumo estatístico por nível

| Nível | Serviço | Runs | Amostras attack | Sucesso médio | Falha média | Lat p50/p95 ms | PCAP total MB | Dataset médio (min-max) | Exec média s | Extratores ok/total | CPU média/máx | Mem MB média |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | http | 5 | 199 | 100% | 0% | 5,33 / 17,74 | 44,28 | 39.466 (39.162-40.060) | 40 | 2/3 | 1,27% / 2,3% | 117,25 |
| L1 | http | 1 | 40 | 100% | 0% | 5 / 22,02 | 8,82 | 39.366 (39.366-39.366) | 40 | 2/3 | 5,47% / 57,73% | 118,42 |

## Estabilidade entre reexecuções

| Nível | Métrica | Runs | Média | Desvio | CV | Min | Max |
| --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | Linhas do dataset | 5 | 39.466,4 | 331,3 | 0,84% | 39.162 | 40.060 |
| L0 | Tempo de execução | 5 | 40 | 0 | 0% | 40 | 40 |
| L0 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L0 | Latência p95 censurada | 5 | 17,74 | 5,37 | 30,29% | 7,17 | 21,76 |
| L0 | CPU média na fase attack | 5 | 1,27 | 0,1 | 7,55% | 1,16 | 1,42 |
| L1 | Linhas do dataset | 1 | 39.366 | 0 | 0% | 39.366 | 39.366 |
| L1 | Tempo de execução | 1 | 40 | 0 | 0% | 40 | 40 |
| L1 | Falha na fase attack | 1 | 0 | 0 | n/d | 0 | 0 |
| L1 | Latência p95 censurada | 1 | 22,02 | 0 | 0% | 22,02 | 22,02 |
| L1 | CPU média na fase attack | 1 | 5,47 | 0 | 0% | 5,47 | 5,47 |

## Validação de artefatos

Não foi encontrada tabela agregada de validação de artefatos para este ataque.

## Figuras selecionadas

Nenhuma figura agregada foi encontrada em `reports/figs` para este ataque.

## Fontes utilizadas

- Catálogo do ataque: `docker/attackers/cdp-table-flood/attack.yaml`
- Artefatos da campanha: `experiments/60att_5runs_l0l1l2l3/net_cdp_table_flood`
