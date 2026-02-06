#!/usr/bin/env node
/**
 * Test Ahrefs API with Node.js
 * Testing fetch, axios, and https module with different configurations
 */

const https = require('https');
const http = require('http');

const API_KEY = "YOUR_AHREFS_API_KEY";
const BASE_URL_V3 = "https://api.ahrefs.com/v3";
const BASE_URL_V2 = "https://api.ahrefs.com/v2";

function printSeparator(title) {
    console.log("\n" + "=".repeat(80));
    console.log(` ${title}`);
    console.log("=".repeat(80) + "\n");
}

// Test with native fetch (Node.js 18+)
async function testFetch(testName, url, options = {}) {
    printSeparator(`FETCH TEST: ${testName}`);
    console.log(`URL: ${url}`);
    console.log(`Options: ${JSON.stringify(options, null, 2)}`);
    console.log("-".repeat(80));

    try {
        const response = await fetch(url, options);

        console.log(`Status: ${response.status} ${response.statusText}`);
        console.log("\nResponse Headers:");
        response.headers.forEach((value, key) => {
            console.log(`  ${key}: ${value}`);
        });

        const body = await response.text();
        console.log("\nResponse Body:");
        try {
            console.log(JSON.stringify(JSON.parse(body), null, 2));
        } catch {
            console.log(body);
        }

        return true;
    } catch (error) {
        console.log(`Error: ${error.name}`);
        console.log(`Message: ${error.message}`);
        console.log(`Stack: ${error.stack}`);
        return false;
    }
}

// Test with https module
async function testHttpsModule(testName, url, headers = {}) {
    printSeparator(`HTTPS MODULE TEST: ${testName}`);
    console.log(`URL: ${url}`);
    console.log(`Headers: ${JSON.stringify(headers, null, 2)}`);
    console.log("-".repeat(80));

    return new Promise((resolve) => {
        const urlObj = new URL(url);
        const options = {
            hostname: urlObj.hostname,
            port: urlObj.port || 443,
            path: urlObj.pathname + urlObj.search,
            method: 'GET',
            headers: headers,
            rejectUnauthorized: true
        };

        const req = https.request(options, (res) => {
            console.log(`Status: ${res.statusCode} ${res.statusMessage}`);
            console.log("\nResponse Headers:");
            Object.entries(res.headers).forEach(([key, value]) => {
                console.log(`  ${key}: ${value}`);
            });

            let body = '';
            res.on('data', (chunk) => {
                body += chunk;
            });

            res.on('end', () => {
                console.log("\nResponse Body:");
                try {
                    console.log(JSON.stringify(JSON.parse(body), null, 2));
                } catch {
                    console.log(body);
                }
                resolve(true);
            });
        });

        req.on('error', (error) => {
            console.log(`Error: ${error.name}`);
            console.log(`Message: ${error.message}`);
            console.log(`Code: ${error.code}`);
            console.log(`Stack: ${error.stack}`);
            resolve(false);
        });

        req.end();
    });
}

// Test with https module and disabled SSL verification
async function testHttpsModuleInsecure(testName, url, headers = {}) {
    printSeparator(`HTTPS MODULE TEST (SSL DISABLED): ${testName}`);
    console.log(`URL: ${url}`);
    console.log(`Headers: ${JSON.stringify(headers, null, 2)}`);
    console.log("-".repeat(80));

    return new Promise((resolve) => {
        const urlObj = new URL(url);
        const options = {
            hostname: urlObj.hostname,
            port: urlObj.port || 443,
            path: urlObj.pathname + urlObj.search,
            method: 'GET',
            headers: headers,
            rejectUnauthorized: false  // Disable SSL verification
        };

        const req = https.request(options, (res) => {
            console.log(`Status: ${res.statusCode} ${res.statusMessage}`);
            console.log("\nResponse Headers:");
            Object.entries(res.headers).forEach(([key, value]) => {
                console.log(`  ${key}: ${value}`);
            });

            let body = '';
            res.on('data', (chunk) => {
                body += chunk;
            });

            res.on('end', () => {
                console.log("\nResponse Body:");
                try {
                    console.log(JSON.stringify(JSON.parse(body), null, 2));
                } catch {
                    console.log(body);
                }
                resolve(true);
            });
        });

        req.on('error', (error) => {
            console.log(`Error: ${error.name}`);
            console.log(`Message: ${error.message}`);
            console.log(`Code: ${error.code}`);
            console.log(`Stack: ${error.stack}`);
            resolve(false);
        });

        req.end();
    });
}

// Test with axios (if available)
async function testAxios(testName, url, config = {}) {
    printSeparator(`AXIOS TEST: ${testName}`);

    try {
        const axios = require('axios');
        console.log(`URL: ${url}`);
        console.log(`Config: ${JSON.stringify(config, null, 2)}`);
        console.log("-".repeat(80));

        const response = await axios.get(url, config);

        console.log(`Status: ${response.status} ${response.statusText}`);
        console.log("\nResponse Headers:");
        Object.entries(response.headers).forEach(([key, value]) => {
            console.log(`  ${key}: ${value}`);
        });

        console.log("\nResponse Body:");
        console.log(JSON.stringify(response.data, null, 2));

        return true;
    } catch (error) {
        if (error.code === 'MODULE_NOT_FOUND') {
            console.log("Axios not installed - skipping axios tests");
            return null;
        }
        console.log(`Error: ${error.name}`);
        console.log(`Message: ${error.message}`);
        if (error.response) {
            console.log(`Response Status: ${error.response.status}`);
            console.log(`Response Data:`, error.response.data);
        }
        console.log(`Stack: ${error.stack}`);
        return false;
    }
}

async function runTests() {
    printSeparator("AHREFS API NODE.JS TESTING");
    console.log(`Test started at: ${new Date().toISOString()}`);

    const endpoint = "/site-explorer/domain-rating?target=ahrefs.com&date=2025-12-01";
    const urlV3 = BASE_URL_V3 + endpoint;
    const urlV2 = BASE_URL_V2 + endpoint;

    const results = { success: [], failed: [], skipped: [] };

    // Test 1: Fetch with Bearer token
    const test1 = await testFetch(
        "V3 API - Fetch with Bearer token",
        urlV3,
        {
            headers: {
                'Authorization': `Bearer ${API_KEY}`
            }
        }
    );
    test1 ? results.success.push("Fetch Bearer") : results.failed.push("Fetch Bearer");

    // Test 2: Fetch with direct API key
    const test2 = await testFetch(
        "V3 API - Fetch with direct API key",
        urlV3,
        {
            headers: {
                'Authorization': API_KEY
            }
        }
    );
    test2 ? results.success.push("Fetch Direct") : results.failed.push("Fetch Direct");

    // Test 3: Fetch with Token prefix
    const test3 = await testFetch(
        "V3 API - Fetch with Token prefix",
        urlV3,
        {
            headers: {
                'Authorization': `Token ${API_KEY}`
            }
        }
    );
    test3 ? results.success.push("Fetch Token") : results.failed.push("Fetch Token");

    // Test 4: HTTPS module with Bearer token
    const test4 = await testHttpsModule(
        "V3 API - HTTPS module with Bearer token",
        urlV3,
        {
            'Authorization': `Bearer ${API_KEY}`,
            'User-Agent': 'Node.js-HTTPS-Test/1.0'
        }
    );
    test4 ? results.success.push("HTTPS Bearer") : results.failed.push("HTTPS Bearer");

    // Test 5: HTTPS module with SSL disabled
    const test5 = await testHttpsModuleInsecure(
        "V3 API - HTTPS module SSL disabled",
        urlV3,
        {
            'Authorization': `Bearer ${API_KEY}`
        }
    );
    test5 ? results.success.push("HTTPS Insecure") : results.failed.push("HTTPS Insecure");

    // Test 6: V2 API with Bearer token
    const test6 = await testFetch(
        "V2 API - Fetch with Bearer token",
        urlV2,
        {
            headers: {
                'Authorization': `Bearer ${API_KEY}`
            }
        }
    );
    test6 ? results.success.push("V2 Fetch Bearer") : results.failed.push("V2 Fetch Bearer");

    // Test 7: Axios with Bearer token (if available)
    const test7 = await testAxios(
        "V3 API - Axios with Bearer token",
        urlV3,
        {
            headers: {
                'Authorization': `Bearer ${API_KEY}`
            }
        }
    );
    if (test7 === null) {
        results.skipped.push("Axios Bearer");
    } else {
        test7 ? results.success.push("Axios Bearer") : results.failed.push("Axios Bearer");
    }

    // Test 8: Axios with SSL disabled (if available)
    const test8 = await testAxios(
        "V3 API - Axios SSL disabled",
        urlV3,
        {
            headers: {
                'Authorization': `Bearer ${API_KEY}`
            },
            httpsAgent: new https.Agent({
                rejectUnauthorized: false
            })
        }
    );
    if (test8 === null) {
        results.skipped.push("Axios SSL Disabled");
    } else {
        test8 ? results.success.push("Axios SSL Disabled") : results.failed.push("Axios SSL Disabled");
    }

    // Test 9: Query parameter auth
    const test9 = await testFetch(
        "V3 API - Query parameter auth",
        urlV3 + `&token=${API_KEY}`,
        {}
    );
    test9 ? results.success.push("Query Param Auth") : results.failed.push("Query Param Auth");

    // Test 10: Alternative metrics endpoint
    const test10 = await testFetch(
        "V3 API - Metrics endpoint",
        "https://api.ahrefs.com/v3/site-explorer/metrics?target=ahrefs.com&date=2025-12-01",
        {
            headers: {
                'Authorization': `Bearer ${API_KEY}`
            }
        }
    );
    test10 ? results.success.push("Metrics Endpoint") : results.failed.push("Metrics Endpoint");

    // Summary
    printSeparator("TEST SUMMARY");
    console.log(`Successful tests: ${results.success.length}`);
    results.success.forEach(name => console.log(`  ✓ ${name}`));

    console.log(`\nFailed tests: ${results.failed.length}`);
    results.failed.forEach(name => console.log(`  ✗ ${name}`));

    if (results.skipped.length > 0) {
        console.log(`\nSkipped tests: ${results.skipped.length}`);
        results.skipped.forEach(name => console.log(`  - ${name}`));
    }

    console.log(`\nTest completed at: ${new Date().toISOString()}`);
}

runTests().catch(console.error);
