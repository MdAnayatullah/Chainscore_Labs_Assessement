# Detailed Encoding Specification

## 1. Basic Concepts

### 1.1 Core Functions

Two primary functions are defined:
- `E(x)`: Encodes a value into a sequence of bytes
- `E⁻¹(x)`: Decodes a sequence of bytes back into a value

### 1.2 Operators

- `⌢` (Concatenation): Joins two byte sequences together
  ```
  [1, 2] ⌢ [3, 4] = [1, 2, 3, 4]
  ```

- `↕` (Length Prefix): Indicates a value should be prefixed with its length
  ```
  ↕[1, 2, 3] = [3, 1, 2, 3]  // 3 is the length prefix
  ```

- `^^` (Order By): Indicates items should be ordered
  ```
  [3, 1, 2] ^^ = [1, 2, 3]  // Orders items
  ```
- `⌊x⌋` (Floor): Returns the floor of x
  ```
  ⌊3.14⌋ = 3
  ```

## 2. Basic Type Encoding

### 2.1 Empty/Null Value

Formula: `E(∅) ≡ []`

This means:
- Null or empty values encode to an empty byte sequence
- Example: `E(None) = []`

### 2.2 Octet Sequences (Raw Bytes)

Formula: `E(x ∈ Y) ≡ x`

This means:
- Byte sequences are encoded as themselves without modification
- Example: `E(bytes([1, 2, 3])) = [1, 2, 3]`

### 2.3 Tuples

Formula: `E({a, b, ...}) ≡ E(a) ⌢ E(b) ⌢ ...`

This means:
- Each element is encoded individually
- Results are concatenated in order
- Example: 
  ```python
  E({1, "abc"}) = E(1) ⌢ E("abc")
  ```

## 3. Integer Encoding

### 3.1 Fixed-Length Integer Encoding

Formula:
```
E[l ∈ N]: N(2^(8l)) → Yl (Y octet sequence of length l)
x ↦ {
    [] if l = 0
    [x mod 256] ⌢ El-1(⌊x/256⌋) otherwise
}
```

This means:
- Integers are encoded in little-endian format
- l determines number of bytes to use
- Each byte represents 8 bits of the number 
- Example for E2 (2-byte encoding):
  ```python
  E2(1234) = [210, 4]  # 1234 = 210 + 4*256
  ```
- For simplicity, assume all integers are encoded in 8 bytes in testing and use 8-byte encoding for all integers

## 4. Sequence Encoding

### 4.1 Basic Sequence

Formula: `E([i0, i1, ...]) ≡ E(i0) ⌢ E(i1) ⌢ ...`

This means:
- Each element is encoded individually
- Results are concatenated in order
- Example:
  ```python
  E([1, 2, 3]) = E(1) ⌢ E(2) ⌢ E(3)
  ```

### 4.2 Length-Prefixed Sequence

Formula:
```
↕x ≡ {|x|, x}
E(↕x) ≡ E(|x|) ⌢ E(x)
```

This means:
- The length of the sequence is encoded first
- The encoded sequence follows
- Example:
  ```python
  E(↕[1, 2, 3]) = E(3) ⌢ E([1, 2, 3])
  # If E(3) = [3], result would be [3, 1, 2, 3]
  ```

## 5. Dictionary Encoding

Formula: `E(d ∈ D⟨K → V⟩) ≡ E(↕[k ^^ {E(k), E(d[k])} | k ∈ K(d)])`

This means:
1. Sort dictionary by keys
2. For each key-value pair:
   - Encode the key
   - Encode the value
   - Combine them as a pair
3. Create a sequence of these pairs
4. Length-prefix the sequence

Example:
```python
input_dict = {"b": 2, "a": 1}
# 1. Sort by keys: [("a", 1), ("b", 2)]
# 2. Encode each pair:
#    - Pair 1: E("a") ⌢ E(1)
#    - Pair 2: E("b") ⌢ E(2)
# 3. Create sequence of pairs
# 4. Add length prefix (2 pairs)
```

## 6. Complete Example

Let's encode a simple structure:
```python
data = {
    "nums": [1, 2],
    "text": "hi"
}
```

Encoding process:
1. Start with dictionary encoding
   - Sort keys: ["nums", "text"]
   - Length prefix: 2 pairs

2. First pair ("nums", [1, 2]):
   - Encode key "nums"
   - Encode array [1, 2] with length prefix

3. Second pair ("text", "hi"):
   - Encode key "text"
   - Encode string "hi" with length prefix

Final byte sequence might look like:
```python
[
    2,                    # Dictionary has 2 pairs
    4, 'n','u','m','s',  # Key "nums"
    2, 1, 2,             # Value [1, 2] (length 2, then values)
    4, 't','e','x','t',  # Key "text"
    2, 'h','i'           # Value "hi" (length 2, then string)
]
```

## 7. Implementation Notes

1. Integer Encoding:
   - Always use little-endian
   - Use minimum required bytes
   - Handle overflow checking

2. Sequence Encoding:
   - Length must be encoded first
   - Length encoding must be consistent

3. Dictionary Encoding:
   - Must sort keys
   - Handle non-string keys
   - Consistent key ordering

4. Error Handling:
   - Invalid input types
   - Integer overflow
   - Maximum sequence length
   - Dictionary key type restrictions