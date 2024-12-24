# Encoder/Decoder Implementation Task

## Overview

Implement an encoder/decoder that can serialize data structures into deterministic octet sequences and deserialize them back. The implementation must follow the provided specification (SPEC.md).

## Requirements

Implement encoders and decoders for:
1. Basic values (null, octets)
2. Integers (little-endian)
3. Sequences
4. Length-prefixed sequences
5. Dictionaries (key-ordered)

## Simple Test Vectors

Your implementation must correctly handle these test vectors:

```python
# Test Vector 1: Basic Types
INPUT_1 = {
    "null": None,
    "octets": bytes([1, 2, 3]),
    "integer": 12345
}
EXPECTED_1 = [
    0x03,                   # Dictionary with 3 items
    0x04, 0x6E, 0x75, 0x6C, 0x6C,         # "null"
    0x00,                   # Empty sequence
    0x06, 0x6F, 0x63, 0x74, 0x65, 0x74, 0x73,  # "octets"
    0x03, 0x01, 0x02, 0x03, # Byte sequence length 3
    0x07, 0x69, 0x6E, 0x74, 0x65, 0x67, 0x65, 0x72,  # "integer"
    0x39, 0x30             # 12345 in little-endian
]

# Test Vector 2: Nested Structures
INPUT_2 = {
    "outer": {
        "inner": [1, 2, 3],
        "value": 42
    }
}
EXPECTED_2 = [
    0x01,                   # Dictionary with 1 item
    0x05, 0x6F, 0x75, 0x74, 0x65, 0x72,   # "outer"
    0x02,                   # Dictionary with 2 items
    0x05, 0x69, 0x6E, 0x6E, 0x65, 0x72,   # "inner"
    0x03, 0x01, 0x02, 0x03, # Array [1,2,3]
    0x05, 0x76, 0x61, 0x6C, 0x75, 0x65,   # "value"
    0x2A                    # 42
]

# Test Vector 3: Large Integer
INPUT_3 = 18446744073709551615  # 2^64 - 1
EXPECTED_3 = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
```

## Performance Test Vector

1. Generate test data:
```bash
# Generate 10MB test file
python perf_test_gen.py --size 10485760 --seed 42 --output test_data.json
```

2. Run test:
```bash

# Run with custom paths
python YOUR_TEST_DIRECTORY/YOUR_TEST_RUNNER.py YOUR_ENCODER.py --input test_data.json --output result.json
```

3. Verify results:
```bash
# Should show success and performance metrics
cat results.json
```

#### Results Format

The test runner will generate a results file with this structure:
```json
{
    "result": "success",    // "success" or "failed"
    "time": 1000,           // Total time in milliseconds 
    "outputSize": 1000000,  // Size of encoded data in bytes
    "inputSize": 1000000,   // Size of input JSON in bytes
    "seed": 42              // Seed used to generate test data
}
```

## What to Submit

1. Source code implementing:
   - Encoder
   - Decoder 
   - Test suite

2. Documentation including:
   - Installation instructions
   - Usage examples
   - Error handling approach
   - Performance considerations

## Testing Your Implementation

```bash
# Run test vectors
python test_vectors.py

# Run performance test
python performance_test.py

# Run error handling tests
python error_tests.py
```

## Evaluation Criteria

1. Correctness (70%)
   - Exact match with test vectors
   - Proper error handling
   - Maintains ordering requirements

2. Code Quality (20%)
   - Clean, readable code
   - Good documentation
   - Proper type hints/checks

3. Performance (10%)
   - Meets performance requirements
   - Efficient memory usage

## Questions?

Open an issue in this repository for any questions about the specification or requirements.