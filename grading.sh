#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "🔍 Starting grading process..."

# Check if result.json exists
if [ ! -f "result.json" ]; then
    echo -e "${RED}❌ Error: result.json file not found${NC}"
    exit 1
fi

# Check if file is empty
if [ ! -s "result.json" ]; then
    echo -e "${RED}❌ Error: result.json is empty${NC}"
    exit 1
fi

# Check if file is valid JSON
if ! jq empty result.json 2>/dev/null; then
    echo -e "${RED}❌ Error: result.json is not valid JSON${NC}"
    exit 1
fi

echo "📊 Validating result.json contents..."

# Check result field
RESULT=$(jq -r '.result' result.json)
if [ "$RESULT" != "success" ] && [ "$RESULT" != "failed" ]; then
    echo -e "${RED}❌ Error: Invalid result value. Must be 'success' or 'failed'${NC}"
    exit 1
fi

# Check if time is the default placeholder value
TIME=$(jq -r '.time' result.json)
if [ "$TIME" -eq 1000 ]; then
    echo -e "${RED}❌ Error: Time value appears to be the default placeholder (1000)${NC}"
    exit 1
fi

# Check if outputSize is the default placeholder value
OUTPUT_SIZE=$(jq -r '.outputSize' result.json)
if [ "$OUTPUT_SIZE" -eq 1000000 ]; then
    echo -e "${RED}❌ Error: outputSize appears to be the default placeholder (1000000)${NC}"
    exit 1
fi

# Check if inputSize is the default placeholder value
INPUT_SIZE=$(jq -r '.inputSize' result.json)
if [ "$INPUT_SIZE" -eq 1000000 ]; then
    echo -e "${RED}❌ Error: inputSize appears to be the default placeholder (1000000)${NC}"
    exit 1
fi

# Validate reasonable ranges
if [ "$TIME" -le 0 ]; then
    echo -e "${RED}❌ Error: Time value must be positive${NC}"
    exit 1
fi

if [ "$OUTPUT_SIZE" -le 0 ]; then
    echo -e "${RED}❌ Error: outputSize must be positive${NC}"
    exit 1
fi

if [ "$INPUT_SIZE" -le 0 ]; then
    echo -e "${RED}❌ Error: inputSize must be positive${NC}"
    exit 1
fi

# Check seed value exists and is an integer
if ! jq -e '.seed' result.json > /dev/null; then
    echo -e "${RED}❌ Error: Missing seed value${NC}"
    exit 1
fi

# Additional sanity checks
if [ "$OUTPUT_SIZE" -gt $((1024 * 1024 * 100)) ]; then
    echo -e "${YELLOW}⚠️  Warning: outputSize is unusually large (>100MB)${NC}"
fi

if [ "$TIME" -gt 300000 ]; then
    echo -e "${YELLOW}⚠️  Warning: Execution time is unusually high (>5 minutes)${NC}"
fi

# Calculate compression ratio
RATIO=$(echo "scale=2; $OUTPUT_SIZE / $INPUT_SIZE" | bc)
if (( $(echo "$RATIO > 2" | bc -l) )); then
    echo -e "${YELLOW}⚠️  Warning: Output size is more than twice the input size${NC}"
fi

echo -e "${GREEN}✅ All validation checks passed${NC}"
echo "📊 Statistics:"
echo "- Time: ${TIME}ms"
echo "- Input Size: ${INPUT_SIZE} bytes"
echo "- Output Size: ${OUTPUT_SIZE} bytes"
echo "- Compression Ratio: ${RATIO}"

exit 0
