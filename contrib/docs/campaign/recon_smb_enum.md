# SMB Enumerating (`recon_smb_enum`)

[Índice da campanha](README.md)

Na campanha `experiments/60att_5runs_l0l1l2l3`, este documento consolida a execução do ataque `recon_smb_enum`. No catálogo local, o ataque é descrito como: Enumeration of SMB share directories and vulnerabilities. A documentação abaixo usa apenas artefatos já presentes no repositório, principalmente as tabelas e figuras de `experiments/60att_5runs_l0l1l2l3/recon_smb_enum`.

## Metadados do ataque

| Campo | Valor |
| --- | --- |
| ID | `recon_smb_enum` |
| Categoria | 1) Reconnaissance and Discovery |
| Subcategoria | 1.2 Port, service, OS, and vulnerability scanning |
| Serviços alvo | target IP service |
| Imagem | `attack-smb-enumerating:latest` |
| Container | `attack-smb-enumerating` |
| Runtime máximo do catálogo | 10 s |
| Parâmetros de intensidade | n/d |
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0043/](https://attack.mitre.org/tactics/TA0043/)<br>[https://attack.mitre.org/tactics/TA0007/](https://attack.mitre.org/tactics/TA0007/)<br>[https://attack.mitre.org/techniques/T1590/](https://attack.mitre.org/techniques/T1590/)<br>[https://attack.mitre.org/techniques/T1592/](https://attack.mitre.org/techniques/T1592/)<br>[https://attack.mitre.org/techniques/T1595/](https://attack.mitre.org/techniques/T1595/)<br>[https://attack.mitre.org/techniques/T1595/002/](https://attack.mitre.org/techniques/T1595/002/)<br>[https://attack.mitre.org/techniques/T1046/](https://attack.mitre.org/techniques/T1046/)<br>[https://attack.mitre.org/techniques/T1135/](https://attack.mitre.org/techniques/T1135/)<br>[https://attack.mitre.org/techniques/T1087/](https://attack.mitre.org/techniques/T1087/)<br>[https://attack.mitre.org/techniques/T1069/](https://attack.mitre.org/techniques/T1069/) |

## Resumo estatístico por nível

| Nível | Serviço | Runs | Amostras attack | Sucesso médio | Falha média | Lat p50/p95 ms | PCAP total MB | Dataset médio (min-max) | Exec média s | Extratores ok/total | CPU média/máx | Mem MB média |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | smb | 5 | 200 | 100% | 0% | 3,44 / 4,55 | 1,26 | 4.855 (4.850-4.864) | 42,63 | 3/3 | 1,39% / 1,65% | 36,32 |
| L1 | smb | 5 | 200 | 100% | 0% | 3,67 / 5,31 | 2,34 | 7.317 (7.302-7.350) | 43,06 | 3/3 | 4,52% / 28,43% | 38,52 |
| L2 | smb | 5 | 200 | 100% | 0% | 4,22 / 6,04 | 2,34 | 7.303 (7.294-7.322) | 43,06 | 3/3 | 3,9% / 20,75% | 37,96 |
| L3 | smb | 5 | 200 | 100% | 0% | 3,76 / 5,21 | 2,34 | 7.301 (7.292-7.312) | 43 | 3/3 | 3,51% / 20,3% | 38,32 |

## Estabilidade entre reexecuções

| Nível | Métrica | Runs | Média | Desvio | CV | Min | Max |
| --- | --- | --- | --- | --- | --- | --- | --- |
| L0 | CPU média na fase attack | 5 | 1,39 | 0,06 | 4,17% | 1,31 | 1,46 |
| L0 | Linhas do dataset | 5 | 4.855,2 | 5,76 | 0,12% | 4.850 | 4.864 |
| L0 | Tempo de execução | 5 | 42,63 | 0,35 | 0,82% | 42,44 | 43,25 |
| L0 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L0 | Latência p95 censurada | 5 | 4,55 | 0,74 | 16,28% | 3,76 | 5,55 |
| L1 | CPU média na fase attack | 5 | 4,52 | 1,93 | 42,78% | 3,44 | 7,94 |
| L1 | Linhas do dataset | 5 | 7.317,2 | 19,68 | 0,27% | 7.302 | 7.350 |
| L1 | Tempo de execução | 5 | 43,06 | 0,09 | 0,2% | 42,98 | 43,19 |
| L1 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L1 | Latência p95 censurada | 5 | 5,31 | 0,94 | 17,64% | 3,74 | 6,22 |
| L2 | CPU média na fase attack | 5 | 3,9 | 0,3 | 7,66% | 3,42 | 4,13 |
| L2 | Linhas do dataset | 5 | 7.303,2 | 11,1 | 0,15% | 7.294 | 7.322 |
| L2 | Tempo de execução | 5 | 43,06 | 0,07 | 0,17% | 42,95 | 43,11 |
| L2 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L2 | Latência p95 censurada | 5 | 6,04 | 0,71 | 11,69% | 4,98 | 6,9 |
| L3 | CPU média na fase attack | 5 | 3,51 | 0,28 | 8,07% | 3,12 | 3,81 |
| L3 | Linhas do dataset | 5 | 7.300,8 | 8,07 | 0,11% | 7.292 | 7.312 |
| L3 | Tempo de execução | 5 | 43 | 0,07 | 0,17% | 42,9 | 43,07 |
| L3 | Falha na fase attack | 5 | 0 | 0 | n/d | 0 | 0 |
| L3 | Latência p95 censurada | 5 | 5,21 | 0,9 | 17,29% | 3,71 | 5,86 |

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
<td><img src="../../assets/campaign_doc/recon_smb_enum/F3_v1_timeseries_smb_recon_smb_enum_L0_run01.png" alt="Série temporal L0 run01" width="420"><br><sub>Série temporal L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/recon_smb_enum/F3_v1_timeseries_smb_recon_smb_enum_L1_run01.png" alt="Série temporal L1 run01" width="420"><br><sub>Série temporal L1 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/recon_smb_enum/F3_v1_timeseries_smb_recon_smb_enum_L2_run01.png" alt="Série temporal L2 run01" width="420"><br><sub>Série temporal L2 run01</sub></td>
<td><img src="../../assets/campaign_doc/recon_smb_enum/F3_v1_timeseries_smb_recon_smb_enum_L3_run01.png" alt="Série temporal L3 run01" width="420"><br><sub>Série temporal L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/recon_smb_enum/F5_resources_smb_recon_smb_enum_L0_run01.png" alt="Recursos L0 run01" width="420"><br><sub>Recursos L0 run01</sub></td>
<td><img src="../../assets/campaign_doc/recon_smb_enum/F5_resources_smb_recon_smb_enum_L3_run01.png" alt="Recursos L3 run01" width="420"><br><sub>Recursos L3 run01</sub></td>
</tr>
<tr>
<td><img src="../../assets/campaign_doc/recon_smb_enum/F4_v2_failrate_smb_recon_smb_enum_L0.png" alt="Taxa de falha L0" width="420"><br><sub>Taxa de falha L0</sub></td>
<td><img src="../../assets/campaign_doc/recon_smb_enum/F4_v2_failrate_smb_recon_smb_enum_L3.png" alt="Taxa de falha L3" width="420"><br><sub>Taxa de falha L3</sub></td>
</tr>
</table>

## Fontes utilizadas

- Catálogo do ataque: `docker/attackers/smb-enumerating/attack.yaml`
- Artefatos da campanha: `experiments/60att_5runs_l0l1l2l3/recon_smb_enum`
