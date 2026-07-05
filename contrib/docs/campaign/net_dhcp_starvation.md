# DHCP Starvation (`net_dhcp_starvation`)

[Índice da campanha](README.md)

Na campanha `experiments/60att_5runs_l0l1l2l3`, este documento consolida a execução do ataque `net_dhcp_starvation`. No catálogo local, o ataque é descrito como: DHCP lease exhaustion on the local network. A documentação abaixo usa apenas artefatos já presentes no repositório, principalmente as tabelas e figuras de `experiments/60att_5runs_l0l1l2l3/net_dhcp_starvation`.

## Metadados do ataque

| Campo | Valor |
| --- | --- |
| ID | `net_dhcp_starvation` |
| Categoria | 2) Network Interception and Exploitation |
| Subcategoria | 2.1 L2/L3 |
| Serviços alvo | local network |
| Imagem | `attack-dhcp-starvation:latest` |
| Container | `attack-dhcp-starvation` |
| Runtime máximo do catálogo | 10 s |
| Parâmetros de intensidade | n/d |
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0040/](https://attack.mitre.org/tactics/TA0040/)<br>[https://attack.mitre.org/techniques/T1498/](https://attack.mitre.org/techniques/T1498/)<br>[https://attack.mitre.org/techniques/T1498/001/](https://attack.mitre.org/techniques/T1498/001/)<br>[https://attack.mitre.org/techniques/T1499/](https://attack.mitre.org/techniques/T1499/)<br>[https://attack.mitre.org/techniques/T1499/002/](https://attack.mitre.org/techniques/T1499/002/) |

## Resumo estatístico por nível

| Nível | Serviço | Runs | Amostras attack | Sucesso médio | Falha média | Lat p50/p95 ms | PCAP total MB | Dataset médio (min-max) | Exec média s | Extratores ok/total | CPU média/máx | Mem MB média |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | http | 5 | 200 | 100% | 0% | 5,66 / 6,87 | 5,51 | 10.304 (10.072-10.796) | 40 | 2/3 | 0,27% / 1,06% | 137,99 |
| L1 | http | 2 | 80 | 100% | 0% | 6,35 / 7,34 | 14,64 | 53.796 (12.848-94.744) | 40 | 2/3 | 2,41% / 28,74% | 140,07 |

## Estabilidade entre reexecuções

| Nível | Métrica | Runs | Média | Desvio | CV | Min | Max |
| --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | Linhas do dataset | 5 | 10.303,6 | 261,34 | 2,54% | 10.072 | 10.796 |
| L0 | Tempo de execução | 5 | 40 | 0 | 0% | 40 | 40 |
| L0 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L0 | Latência p95 censurada | 5 | 6,87 | 0,47 | 6,87% | 6,32 | 7,69 |
| L0 | CPU média na fase attack | 5 | 0,27 | 0,06 | 20,37% | 0,22 | 0,35 |
| L1 | Linhas do dataset | 2 | 53.796 | 40.948 | 76,12% | 12.848 | 94.744 |
| L1 | Tempo de execução | 2 | 40 | 0 | 0% | 40 | 40 |
| L1 | Falha na fase attack | 2 | 0 | 0 | n/d | 0 | 0 |
| L1 | Latência p95 censurada | 2 | 7,34 | 0,19 | 2,64% | 7,15 | 7,53 |
| L1 | CPU média na fase attack | 2 | 2,41 | 0,61 | 25,27% | 1,8 | 3,02 |

## Validação de artefatos

Não foi encontrada tabela agregada de validação de artefatos para este ataque.

## Figuras selecionadas

Nenhuma figura agregada foi encontrada em `reports/figs` para este ataque.

## Fontes utilizadas

- Catálogo do ataque: `docker/attackers/dhcp-starvation/attack.yaml`
- Artefatos da campanha: `experiments/60att_5runs_l0l1l2l3/net_dhcp_starvation`
