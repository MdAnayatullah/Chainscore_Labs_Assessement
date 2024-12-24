#!/usr/bin/env python3
"""
Performance test JSON generator
Creates a large JSON test file with nested structures for encoder/decoder testing
"""

import random
import json
import base64
import argparse
from typing import Any, Dict, List
from pathlib import Path

class PerfTestGenerator:
    def __init__(self, seed: int = 42, target_size: int = 1_048_576):  # 1MB
        self.random = random.Random(seed)
        self.target_size = target_size
        self.current_size = 0
        
    def generate_string(self, min_len: int = 1, max_len: int = 100) -> str:
        """Generate a random ASCII string"""
        length = self.random.randint(min_len, max_len)
        return ''.join(chr(self.random.randint(32, 126)) for _ in range(length))
    
    def generate_bytes(self, min_len: int = 1, max_len: int = 100) -> str:
        """Generate random bytes and encode as base64 string"""
        length = self.random.randint(min_len, max_len)
        raw_bytes = bytes(self.random.randint(0, 255) for _ in range(length))
        return base64.b64encode(raw_bytes).decode('ascii')
    
    def generate_integer(self) -> int:
        """Generate a random integer up to 2^53-1 (JavaScript max safe integer)"""
        return self.random.randint(0, 2**53 - 1)

    def generate_nested_dict(self, depth: int = 0, max_depth: int = 32) -> Dict[str, Any]:
        """Generate a nested dictionary structure"""
        if depth >= max_depth:
            return {"value": self.generate_integer()}
        
        result = {}
        num_entries = self.random.randint(1, 5)
        
        for _ in range(num_entries):
            key = self.generate_string(1, 10)
            choice = self.random.randint(0, 6)
            
            if choice == 0:
                result[key] = self.generate_integer()
            elif choice == 1:
                result[key] = self.generate_string()
            elif choice == 2:
                result[key] = self.generate_bytes()
            elif choice == 3:
                result[key] = None
            elif choice == 4 and depth < max_depth - 1:
                result[key] = self.generate_nested_dict(depth + 1)
            elif choice == 5 and depth < max_depth - 1:
                result[key] = self.generate_nested_list(depth + 1)
            else:
                result[key] = self.generate_integer()
                
        return result
    
    def generate_nested_list(self, depth: int = 0, max_depth: int = 32) -> List[Any]:
        """Generate a nested list structure"""
        if depth >= max_depth:
            return [self.generate_integer()]
            
        length = self.random.randint(1, 5)
        result = []
        
        for _ in range(length):
            choice = self.random.randint(0, 6)
            
            if choice == 0:
                result.append(self.generate_integer())
            elif choice == 1:
                result.append(self.generate_string())
            elif choice == 2:
                result.append(self.generate_bytes())
            elif choice == 3:
                result.append(None)
            elif choice == 4 and depth < max_depth - 1:
                result.append(self.generate_nested_dict(depth + 1))
            elif choice == 5 and depth < max_depth - 1:
                result.append(self.generate_nested_list(depth + 1))
            else:
                result.append(self.generate_integer())
                
        return result

    def generate_performance_test(self) -> Dict[str, Any]:
        """Generate the main performance test data"""
        result = {
            "metadata": {
                "version": 1,
                "generator": "PerfTestGenerator",
                "seed": 42,
                "target_size_bytes": self.target_size,
                "format": "JSON"
            },
            "data": {}
        }
        
        # Keep adding data until we reach target size
        block_num = 0
        current_size = 0
        
        while current_size < self.target_size:
            block_id = f"block_{block_num}"
            result["data"][block_id] = {
                "dict": self.generate_nested_dict(0, 5),
                "list": self.generate_nested_list(0, 5),
                "bytes": self.generate_bytes(50, 200),
                "integer": self.generate_integer(),
                "string": self.generate_string(50, 200)
            }
            
            # Calculate current size
            current_size = len(json.dumps(result))
            block_num += 1
        
        return result

def main():
    parser = argparse.ArgumentParser(description='Generate performance test JSON')
    parser.add_argument('--size', type=int, default=1_048_576, 
                       help='Target size in bytes (default: 1MB)')
    parser.add_argument('--seed', type=int, default=42,
                       help='Random seed (default: 42)')
    parser.add_argument('--output', type=str, default='performance_test.json',
                       help='Output file path')
    parser.add_argument('--pretty', action='store_true',
                       help='Pretty print JSON output')
    args = parser.parse_args()
    
    # Generate test data
    generator = PerfTestGenerator(seed=args.seed, target_size=args.size)
    test_data = generator.generate_performance_test()
    
    # Convert to JSON
    if args.pretty:
        json_data = json.dumps(test_data, indent=2, sort_keys=True)
    else:
        json_data = json.dumps(test_data, sort_keys=True)
    
    # Write to file
    output_path = Path(args.output)
    output_path.write_text(json_data)
    
    # Print statistics
    print(f"\nPerformance Test JSON Generated:")
    print(f"Size: {len(json_data):,} bytes")
    print(f"Blocks: {len(test_data['data']):,}")
    print(f"Path: {output_path.absolute()}")
    print(f"Format: {'Pretty-printed' if args.pretty else 'Minified'} JSON")

if __name__ == "__main__":
    main()