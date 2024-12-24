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


Codec Systems Encoder/Decoder

This project implements an encoder and decoder capable of serializing and deserializing data structures into deterministic octet sequences, as specified in the provided SPEC.md. The implementation ensures correctness, efficiency, and robustness.

Features

Supported Data Types:

Null values

Octet sequences (bytes)

Integers (little-endian encoding)

Sequences (arrays/lists)

Dictionaries (key-ordered)

Performance:

Optimized for large datasets

Supports streaming and efficient memory usage

Robustness:

Comprehensive error handling

Graceful handling of corrupted or invalid inputs

Installation

Clone the repository:

git clone https://github.com/Chainscore-Hiring/codec-systems-MdAnayatullah.git
cd codec-systems-MdAnayatullah

Install dependencies:

pip install -r requirements.txt

Usage

Encoding and Decoding Example

from encoder import encode
from decoder import decode

# Sample data
data = {
    "key": "value",
    "list": [1, 2, 3]
}

# Encode the data
encoded = encode(data)
print("Encoded Data:", encoded)

# Decode the data
decoded, _ = decode(encoded)
print("Decoded Data:", decoded)

# Verify correctness
assert decoded == data

Testing

Running Unit Tests

Run test vectors:

python test_vectors.py

Run error handling tests:

python error_tests.py

Run performance tests:

Generate large test data:

python perf_test_gen.py --size 10485760 --seed 42 --output test_data.json

Run performance tests:

python performance_test.py

Error Handling

Unsupported Types:

Raises TypeError for unsupported data types such as set.

Corrupted Data:

Raises ValueError when encountering invalid or incomplete input data.

Examples:

try:
    encode(set([1, 2, 3]))  # Unsupported type
except TypeError as e:
    print("Error:", e)

try:
    decode(b'\x03\xFF\xFF')  # Corrupted data
except ValueError as e:
    print("Error:", e)

Performance Considerations

Efficient Data Handling:

Uses streaming processing for large datasets.

Lazy Decoding:

Avoids unnecessary computation by decoding data only when accessed.

Optimized Memory Usage:

Processes large sequences and dictionaries in chunks to minimize memory overhead.

Evaluation Criteria

Correctness (70%):

Exact match with provided test vectors.

Handles nested and complex data structures.

Code Quality (20%):

Clean, readable, and Pythonic code.

Well-documented functions and classes.

Performance (10%):

Handles large datasets efficiently.

Meets performance benchmarks.

Repository Structure

.
├── encoder.py          # Encoding logic
├── decoder.py          # Decoding logic
├── test_vectors.py     # Test vectors for validation
├── error_tests.py      # Error handling tests
├── performance_test.py # Performance test script
├── perf_test_gen.py    # Test data generator
├── requirements.txt    # Python dependencies
├── SPEC.md             # Specification document
└── README.md           # Project documentation

Future Enhancements

Support for Additional Data Types:

Floating-point numbers

Boolean values

Advanced Error Reporting:

Detailed tracebacks for decoding errors.

Streaming Support:

Real-time encoding/decoding for large data streams.
