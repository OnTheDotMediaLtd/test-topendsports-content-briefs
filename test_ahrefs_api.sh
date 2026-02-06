#!/bin/bash
###############################################################################
# Test Ahrefs API with curl and wget
# Testing different configurations, SSL settings, and TLS versions
###############################################################################

API_KEY="YOUR_AHREFS_API_KEY"
BASE_URL_V3="https://api.ahrefs.com/v3"
BASE_URL_V2="https://api.ahrefs.com/v2"
ENDPOINT="/site-explorer/domain-rating?target=ahrefs.com&date=2025-12-01"
URL_V3="${BASE_URL_V3}${ENDPOINT}"
URL_V2="${BASE_URL_V2}${ENDPOINT}"

SUCCESS_COUNT=0
FAIL_COUNT=0

print_separator() {
    echo ""
    echo "================================================================================"
    echo " $1"
    echo "================================================================================"
    echo ""
}

test_curl() {
    local test_name="$1"
    shift
    local curl_args=("$@")

    print_separator "CURL TEST: $test_name"
    echo "Command: curl ${curl_args[*]}"
    echo "--------------------------------------------------------------------------------"

    if curl "${curl_args[@]}" 2>&1; then
        echo ""
        echo "✓ Test completed successfully"
        ((SUCCESS_COUNT++))
        return 0
    else
        local exit_code=$?
        echo ""
        echo "✗ Test failed with exit code: $exit_code"
        ((FAIL_COUNT++))
        return $exit_code
    fi
}

test_wget() {
    local test_name="$1"
    shift
    local wget_args=("$@")

    print_separator "WGET TEST: $test_name"
    echo "Command: wget ${wget_args[*]}"
    echo "--------------------------------------------------------------------------------"

    if wget "${wget_args[@]}" 2>&1; then
        echo ""
        echo "✓ Test completed successfully"
        ((SUCCESS_COUNT++))
        return 0
    else
        local exit_code=$?
        echo ""
        echo "✗ Test failed with exit code: $exit_code"
        ((FAIL_COUNT++))
        return $exit_code
    fi
}

print_separator "AHREFS API CURL/WGET TESTING"
echo "Test started at: $(date)"
echo ""

###############################################################################
# CURL TESTS
###############################################################################

# Test 1: Basic curl with Bearer token
test_curl "V3 API - Bearer token (default SSL)" \
    -v \
    -H "Authorization: Bearer ${API_KEY}" \
    "${URL_V3}"

# Test 2: curl with Bearer token and SSL verification disabled
test_curl "V3 API - Bearer token (--insecure)" \
    -v \
    --insecure \
    -H "Authorization: Bearer ${API_KEY}" \
    "${URL_V3}"

# Test 3: curl with direct API key
test_curl "V3 API - Direct API key" \
    -v \
    -H "Authorization: ${API_KEY}" \
    "${URL_V3}"

# Test 4: curl with Token prefix
test_curl "V3 API - Token prefix" \
    -v \
    -H "Authorization: Token ${API_KEY}" \
    "${URL_V3}"

# Test 5: curl with TLS 1.2
test_curl "V3 API - TLS 1.2" \
    -v \
    --tlsv1.2 \
    -H "Authorization: Bearer ${API_KEY}" \
    "${URL_V3}"

# Test 6: curl with TLS 1.3
test_curl "V3 API - TLS 1.3" \
    -v \
    --tlsv1.3 \
    -H "Authorization: Bearer ${API_KEY}" \
    "${URL_V3}"

# Test 7: curl with maximum TLS 1.2
test_curl "V3 API - Max TLS 1.2" \
    -v \
    --tls-max 1.2 \
    -H "Authorization: Bearer ${API_KEY}" \
    "${URL_V3}"

# Test 8: curl with verbose SSL info
test_curl "V3 API - Verbose SSL info" \
    -vvv \
    --trace-time \
    -H "Authorization: Bearer ${API_KEY}" \
    "${URL_V3}"

# Test 9: curl with custom User-Agent
test_curl "V3 API - Custom User-Agent" \
    -v \
    -H "Authorization: Bearer ${API_KEY}" \
    -H "User-Agent: Custom-Curl-Test/1.0" \
    -H "Accept: application/json" \
    "${URL_V3}"

# Test 10: curl with query parameter auth
test_curl "V3 API - Query parameter auth" \
    -v \
    "${URL_V3}&token=${API_KEY}"

# Test 11: curl with X-API-Key header
test_curl "V3 API - X-API-Key header" \
    -v \
    -H "X-API-Key: ${API_KEY}" \
    "${URL_V3}"

# Test 12: V2 API with Bearer token
test_curl "V2 API - Bearer token" \
    -v \
    -H "Authorization: Bearer ${API_KEY}" \
    "${URL_V2}"

# Test 13: Alternative metrics endpoint
test_curl "V3 API - Metrics endpoint" \
    -v \
    -H "Authorization: Bearer ${API_KEY}" \
    "${BASE_URL_V3}/site-explorer/metrics?target=ahrefs.com&date=2025-12-01"

# Test 14: curl with IPv4 only
test_curl "V3 API - IPv4 only" \
    -v \
    -4 \
    -H "Authorization: Bearer ${API_KEY}" \
    "${URL_V3}"

# Test 15: curl with IPv6 only (if available)
test_curl "V3 API - IPv6 only" \
    -v \
    -6 \
    -H "Authorization: Bearer ${API_KEY}" \
    "${URL_V3}"

# Test 16: curl with compressed response
test_curl "V3 API - Compressed response" \
    -v \
    --compressed \
    -H "Authorization: Bearer ${API_KEY}" \
    "${URL_V3}"

# Test 17: curl with detailed timing
test_curl "V3 API - Detailed timing" \
    -v \
    -w "\n\nTiming:\n  DNS: %{time_namelookup}s\n  Connect: %{time_connect}s\n  SSL: %{time_appconnect}s\n  Start Transfer: %{time_starttransfer}s\n  Total: %{time_total}s\n" \
    -H "Authorization: Bearer ${API_KEY}" \
    "${URL_V3}"

# Test 18: curl with all headers shown
test_curl "V3 API - Include headers in output" \
    -v \
    -i \
    -H "Authorization: Bearer ${API_KEY}" \
    "${URL_V3}"

# Test 19: curl with SSL cert status
test_curl "V3 API - SSL cert status" \
    -v \
    --cert-status \
    -H "Authorization: Bearer ${API_KEY}" \
    "${URL_V3}"

# Test 20: curl with connection timeout
test_curl "V3 API - Connection timeout 10s" \
    -v \
    --connect-timeout 10 \
    --max-time 30 \
    -H "Authorization: Bearer ${API_KEY}" \
    "${URL_V3}"

###############################################################################
# WGET TESTS
###############################################################################

# Test 21: wget with Bearer token
test_wget "V3 API - wget with Bearer token" \
    --header="Authorization: Bearer ${API_KEY}" \
    --server-response \
    -O - \
    "${URL_V3}"

# Test 22: wget with no SSL check
test_wget "V3 API - wget no SSL check" \
    --no-check-certificate \
    --header="Authorization: Bearer ${API_KEY}" \
    --server-response \
    -O - \
    "${URL_V3}"

# Test 23: wget with debug output
test_wget "V3 API - wget debug" \
    --debug \
    --header="Authorization: Bearer ${API_KEY}" \
    -O - \
    "${URL_V3}"

# Test 24: wget with custom User-Agent
test_wget "V3 API - wget custom UA" \
    --user-agent="Custom-Wget-Test/1.0" \
    --header="Authorization: Bearer ${API_KEY}" \
    --server-response \
    -O - \
    "${URL_V3}"

# Test 25: wget with query parameter auth
test_wget "V3 API - wget query param" \
    --server-response \
    -O - \
    "${URL_V3}&token=${API_KEY}"

###############################################################################
# SUMMARY
###############################################################################

print_separator "TEST SUMMARY"
echo "Total successful tests: $SUCCESS_COUNT"
echo "Total failed tests: $FAIL_COUNT"
echo "Total tests: $((SUCCESS_COUNT + FAIL_COUNT))"
echo ""
echo "Test completed at: $(date)"
