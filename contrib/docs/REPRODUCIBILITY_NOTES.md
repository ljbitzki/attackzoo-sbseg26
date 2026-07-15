# Reproducibility Notes

This document records the operational assumptions behind the reproducible-experiment claims in the root `README.md`.

## Official Review Mapping

The root `README.md` follows the SBSeg artifact template: each claim lists the command, flags, expected time, expected resources, and expected result. The scripts `run_claim1.sh`, `run_claim2.sh`, `run_claim3.sh`, and `run_claim_figures.sh` are the reviewer-facing entry points.

## Stochastic Traffic And Variance

AttackZoo executes live network traffic inside Docker containers. Some packet timing, TCP state, scheduler timing, Docker startup latency, and target response timing are inherently stochastic and are not controlled by a single global random seed. For that reason, exact packet timing should not be interpreted as the reproducibility target.

The reproducibility target is the generated evidence shape and the aggregate paper metrics:

- the attack catalog and category structure;
- successful target-server and attack-container orchestration;
- PCAP, feature, dataset, and report generation;
- the published full-campaign aggregate counts and figures.

The full campaign used five runs for each attack-level pair where supported. The campaign documentation reports per-level means, min/max values, and coefficient-of-variation tables to make run-to-run variability explicit.

## Published Dataset Audit Trail

The full raw campaign is intentionally not versioned in Git because it is too large. The paper-figure reproduction path uses the published Figshare archive:

- DOI: `10.6084/m9.figshare.32900828`
- Archive: `attackzoo-full_campaign_5runs_4levels.tar.gz`
- Compressed size: `16.9 GB`
- Expected extracted campaign: `60` attacks, `1200` PCAP files, `8` generated figure outputs

`run_claim_figures.sh` resolves the Figshare metadata through the public API, verifies the archive MD5 provided by Figshare, requires the extracted campaign to contain exactly `1200` PCAP files, runs `campaign_traffic_stats.py --plots all`, and fails if the resulting manifest does not report `1200/1200` processed PCAPs and `8` figures.

## Reduced Versus Complete Paths

`run_claim3.sh` is the reduced reviewer path. It proves the local pipeline end to end with a short `dos_http_simple` experiment over levels `L0,L1`; it is not expected to reproduce the paper distributions.

`run_claim_figures.sh` is the complete paper-figure path. It reproduces the paper-level aggregate figures from the published dataset without requiring reviewers to spend roughly 82 hours rerunning the full live campaign.

## Dependency Provenance

Python dependencies are pinned in `requirements.txt`. Docker base images that previously used mutable `latest` references are pinned by digest. NTLFlowLyzer is installed from the upstream Git repository at commit `86d0102466ea42ba03ddda5c649ac7e533fb25d9` by default; override `NTLFLOWLYZER_REF` only when intentionally testing another revision.

Local validation after the artifact cleanup used Ubuntu 24.04.4 LTS, Linux `6.8.0-134-generic`, Python `3.12.3`, and Docker Engine `29.6.1`. The setup accepts Docker Engine `27.0` or newer.
