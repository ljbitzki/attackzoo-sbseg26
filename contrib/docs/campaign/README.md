# Campanha `60att_5runs_l0l1l2l3`

Esta pasta documenta a campanha `experiments/60att_5runs_l0l1l2l3` em um arquivo por ataque. Cada documento usa apenas informações já presentes no repositório: catálogo local dos ataques, tabelas `reports/tables`, artefatos de execução e figuras `reports/figs` copiadas para `contrib/assets/campaign_doc`.

- Ataques documentados: 60
- Ataques com tabelas agregadas: 56
- Figuras copiadas para a documentação: 448

## Documentos

| Ataque | ID | Resumo | Figuras copiadas | Tabelas agregadas |
| --- | --- | --- | --- | --- |
| [SSH Bruteforce](bf_ssh.md) | `bf_ssh` | sim | 8 | sim |
| [Telnet Bruteforce](bf_telnet.md) | `bf_telnet` | sim | 8 | sim |
| [FIN Flood](dos_fin_flood.md) | `dos_fin_flood` | sim | 8 | sim |
| [DoS HTTP Simple](dos_http_simple.md) | `dos_http_simple` | sim | 8 | sim |
| [DoS HTTP Slowloris](dos_http_slowloris.md) | `dos_http_slowloris` | sim | 8 | sim |
| [ICMP Flood](dos_icmp_flood.md) | `dos_icmp_flood` | sim | 8 | sim |
| [PSH Flood](dos_psh_flood.md) | `dos_psh_flood` | sim | 8 | sim |
| [RST Flood](dos_rst_flood.md) | `dos_rst_flood` | sim | 8 | sim |
| [SYN Flood](dos_syn_flood.md) | `dos_syn_flood` | sim | 8 | sim |
| [UDP Flood](dos_udp_flood.md) | `dos_udp_flood` | sim | 8 | sim |
| [DNS Tunneling](exf_dns_tunneling.md) | `exf_dns_tunneling` | sim | 8 | sim |
| [ICMP Tunnel](exf_icmp_tunnel.md) | `exf_icmp_tunnel` | sim | 8 | sim |
| [CoAP GET Flood](iot_coap_get_flood.md) | `iot_coap_get_flood` | sim | 8 | sim |
| [CoAP Resource Discovery Exhaustion](iot_coap_resource_exhaustion.md) | `iot_coap_resource_exhaustion` | sim | 8 | sim |
| [CoAP Response Fuzzing](iot_coap_response_fuzz.md) | `iot_coap_response_fuzz` | sim | 8 | sim |
| [CoAP Token Collision](iot_coap_token_collision.md) | `iot_coap_token_collision` | sim | 8 | sim |
| [MQTT Bruteforce](iot_mqtt_bruteforce.md) | `iot_mqtt_bruteforce` | sim | 8 | sim |
| [MQTT LWT Abuse](iot_mqtt_lwt_abuse.md) | `iot_mqtt_lwt_abuse` | sim | 8 | sim |
| [MQTT Publisher Flood](iot_mqtt_publisher.md) | `iot_mqtt_publisher` | sim | 8 | sim |
| [MQTT QoS 2 Amplification](iot_mqtt_qos_amplification.md) | `iot_mqtt_qos_amplification` | sim | 8 | sim |
| [XRCE-DDS Discovery Poisoning](iot_xrce_dds_discovery_poison.md) | `iot_xrce_dds_discovery_poison` | sim | 8 | sim |
| [XRCE-DDS Entity Flood](iot_xrce_dds_entity_flood.md) | `iot_xrce_dds_entity_flood` | sim | 8 | sim |
| [XRCE-DDS Fragment Abuse](iot_xrce_dds_fragment_abuse.md) | `iot_xrce_dds_fragment_abuse` | sim | 8 | sim |
| [XRCE-DDS Malformed Injection](iot_xrce_dds_malformed_inject.md) | `iot_xrce_dds_malformed_inject` | sim | 8 | sim |
| [XRCE-DDS Session Hijack](iot_xrce_dds_session_hijack.md) | `iot_xrce_dds_session_hijack` | sim | 8 | sim |
| [XRCE-DDS Time Desynchronization](iot_xrce_dds_time_desync.md) | `iot_xrce_dds_time_desync` | sim | 8 | sim |
| [XRCE-DDS UDP DoS](iot_xrce_dds_udp_dos.md) | `iot_xrce_dds_udp_dos` | sim | 8 | sim |
| [Zenoh-Pico Fragment Reassembly Flood](iot_zenoh_pico_fragments_reassembly.md) | `iot_zenoh_pico_fragments_reassembly` | sim | 8 | sim |
| [Zenoh-Pico Keepalive Flood](iot_zenoh_pico_keepalive_flood.md) | `iot_zenoh_pico_keepalive_flood` | sim | 8 | sim |
| [Zenoh-Pico Memory Exhaustion](iot_zenoh_pico_memory_exhaustion.md) | `iot_zenoh_pico_memory_exhaustion` | sim | 8 | sim |
| [Zenoh-Pico Protocol Fuzzer](iot_zenoh_pico_proto_fuzzer.md) | `iot_zenoh_pico_proto_fuzzer` | sim | 8 | sim |
| [Zenoh-Pico Sequence Exhaustion](iot_zenoh_pico_sequence_exhaustion.md) | `iot_zenoh_pico_sequence_exhaustion` | sim | 8 | sim |
| [Zenoh-Pico Timestamp Manipulation Flood](iot_zenoh_pico_timestamp_mess.md) | `iot_zenoh_pico_timestamp_mess` | sim | 8 | sim |
| [ARP Spoof](net_arp_spoof.md) | `net_arp_spoof` | sim | 8 | sim |
| [CDP Table Flood](net_cdp_table_flood.md) | `net_cdp_table_flood` | sim | 0 | não |
| [DHCP Starvation](net_dhcp_starvation.md) | `net_dhcp_starvation` | sim | 0 | não |
| [IPv6 MLD Flood](net_ipv6_mld_flood.md) | `net_ipv6_mld_flood` | sim | 0 | não |
| [IPv6 NS Flood](net_ipv6_ns_flood.md) | `net_ipv6_ns_flood` | sim | 8 | sim |
| [IPv6 RA Flood](net_ipv6_ra_flood.md) | `net_ipv6_ra_flood` | sim | 8 | sim |
| [STP Config Flood](net_stp_conf_flood.md) | `net_stp_conf_flood` | sim | 8 | sim |
| [STP TCN Flood](net_stp_tcn_flood.md) | `net_stp_tcn_flood` | sim | 0 | não |
| [PHP LFI Enumeration](php_lfi_enumeration.md) | `php_lfi_enumeration` | sim | 8 | sim |
| [ARP Scan](recon_arp_scan.md) | `recon_arp_scan` | sim | 8 | sim |
| [Ping Sweep](recon_ping_sweep.md) | `recon_ping_sweep` | sim | 8 | sim |
| [Port Scanner Aggressive](recon_port_scanner_aggressive.md) | `recon_port_scanner_aggressive` | sim | 8 | sim |
| [Port Scanner OS](recon_port_scanner_os.md) | `recon_port_scanner_os` | sim | 8 | sim |
| [Port Scanner TCP](recon_port_scanner_tcp.md) | `recon_port_scanner_tcp` | sim | 8 | sim |
| [Port Scanner UDP](recon_port_scanner_udp.md) | `recon_port_scanner_udp` | sim | 8 | sim |
| [Port Scanner Vulnerabilities](recon_port_scanner_vuln.md) | `recon_port_scanner_vuln` | sim | 8 | sim |
| [SMB Enumerating](recon_smb_enum.md) | `recon_smb_enum` | sim | 8 | sim |
| [SNMP Scanner](recon_snmp_scanner.md) | `recon_snmp_scanner` | sim | 8 | sim |
| [Web Directory Enumeration](web_dir_enumeration.md) | `web_dir_enumeration` | sim | 8 | sim |
| [HTTPS Heartbleed](web_https_heartbleed.md) | `web_https_heartbleed` | sim | 8 | sim |
| [IDOR Path Traversal](web_idor_path_traversal.md) | `web_idor_path_traversal` | sim | 8 | sim |
| [IDOR URL Parameter](web_idor_url_parameter.md) | `web_idor_url_parameter` | sim | 8 | sim |
| [Web POST Bruteforce](web_post_bruteforce.md) | `web_post_bruteforce` | sim | 8 | sim |
| [Web Simple Scanner](web_simple_scanner.md) | `web_simple_scanner` | sim | 8 | sim |
| [SQL Injection](web_sql_injection.md) | `web_sql_injection` | sim | 8 | sim |
| [Web Wide Scanner](web_wide_scanner.md) | `web_wide_scanner` | sim | 8 | sim |
| [XSS Scanner](web_xss_scanner.md) | `web_xss_scanner` | sim | 8 | sim |
