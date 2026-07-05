# IPv6 MLD Flood (`net_ipv6_mld_flood`)

[Índice da campanha](README.md)

Na campanha `experiments/60att_5runs_l0l1l2l3`, este documento consolida a execução do ataque `net_ipv6_mld_flood`. No catálogo local, o ataque é descrito como: ICMPv6 Multicast Listener Report MLD (131) flood on the local network. A documentação abaixo usa apenas artefatos já presentes no repositório, principalmente as tabelas e figuras de `experiments/60att_5runs_l0l1l2l3/net_ipv6_mld_flood`.

## Metadados do ataque

| Campo | Valor |
| --- | --- |
| ID | `net_ipv6_mld_flood` |
| Categoria | 2) Network Interception and Exploitation |
| Subcategoria | 2.2 IPv6 |
| Serviços alvo | local IPv6 network |
| Imagem | `attack-ipv6-mld-flood:latest` |
| Container | `attack-ipv6-mld-flood` |
| Runtime máximo do catálogo | 10 s |
| Parâmetros de intensidade | n/d |
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0040/](https://attack.mitre.org/tactics/TA0040/)<br>[https://attack.mitre.org/techniques/T1498/](https://attack.mitre.org/techniques/T1498/)<br>[https://attack.mitre.org/techniques/T1498/001/](https://attack.mitre.org/techniques/T1498/001/) |

## Resumo estatístico por nível

| Nível | Serviço | Runs | Amostras attack | Sucesso médio | Falha média | Lat p50/p95 ms | PCAP total MB | Dataset médio (min-max) | Exec média s | Extratores ok/total | CPU média/máx | Mem MB média |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | http | 5 | 200 | 100% | 0% | 4,84 / 6,32 | 9,64 | 18.084 (11.370-20.238) | 40 | 2/3 | 0,32% / 1,44% | 153,86 |
| L1 | http | 5 | 200 | 100% | 0% | 4,83 / 6,36 | 3.917,75 | 15.228.693 (13.952.550-17.001.768) | 40 | 2/3 | 7,76% / 9,57% | 122,47 |
| L2 | http | 4 | 160 | 100% | 0% | 4,87 / 6,97 | 3.367,33 | 16.336.531 (15.818.810-16.750.290) | 40 | 2/3 | 7,68% / 8,77% | 116,12 |

## Estabilidade entre reexecuções

| Nível | Métrica | Runs | Média | Desvio | CV | Min | Max |
| --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | Linhas do dataset | 5 | 18.084,4 | 3.367,82 | 18,62% | 11.370 | 20.238 |
| L0 | Tempo de execução | 5 | 40 | 0 | 0% | 40 | 40 |
| L0 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L0 | Latência p95 censurada | 5 | 6,32 | 0,21 | 3,26% | 5,99 | 6,61 |
| L0 | CPU média na fase attack | 5 | 0,32 | 0,05 | 16,55% | 0,25 | 0,38 |
| L1 | Linhas do dataset | 5 | 15.228.692,8 | 1.034.970,63 | 6,8% | 13.952.550 | 17.001.768 |
| L1 | Tempo de execução | 5 | 40 | 0 | 0% | 40 | 40 |
| L1 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L1 | Latência p95 censurada | 5 | 6,36 | 0,77 | 12,17% | 5,41 | 7,51 |
| L1 | CPU média na fase attack | 5 | 7,76 | 0,45 | 5,85% | 7,4 | 8,57 |
| L2 | Linhas do dataset | 4 | 16.336.531 | 415.821,61 | 2,55% | 15.818.810 | 16.750.290 |
| L2 | Tempo de execução | 4 | 40 | 0 | 0% | 40 | 40 |
| L2 | Falha na fase attack | 4 | 0 | 0 | n/d | 0 | 0 |
| L2 | Latência p95 censurada | 4 | 6,97 | 0,79 | 11,39% | 6,15 | 8,08 |
| L2 | CPU média na fase attack | 4 | 7,68 | 0,09 | 1,16% | 7,54 | 7,78 |

## Validação de artefatos

Não foi encontrada tabela agregada de validação de artefatos para este ataque.

## Figuras selecionadas

Nenhuma figura agregada foi encontrada em `reports/figs` para este ataque.

## Fontes utilizadas

- Catálogo do ataque: `docker/attackers/ipv6-mld-flood/attack.yaml`
- Artefatos da campanha: `experiments/60att_5runs_l0l1l2l3/net_ipv6_mld_flood`
