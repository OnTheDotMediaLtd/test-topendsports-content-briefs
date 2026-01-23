## Issue/Improvement

The current validation scripts are taking too long to run when processing large CSV files with thousands of rows. The performance issue is particularly noticeable when validating duplicate URLs across multiple files simultaneously. This impacts the development workflow as developers have to wait several minutes for validation to complete before they can commit their changes. The performance bottleneck appears to be in the duplicate detection logic which uses a simple nested loop approach instead of more efficient data structures.

## Impact

Impact Level: High

Slow validation scripts delay the entire development pipeline. Currently, a developer must wait 3-5 minutes for CSV validation on large datasets, which compounds when running the full validation suite. This impacts team productivity and creates frustration with the validation process.

## Suggested Solution

Optimize the duplicate URL detection by switching from nested loops to a set-based approach. Additionally, implement parallel processing for validating multiple files simultaneously using Python's concurrent.futures module. Consider caching validation results for files that haven't changed between runs.

## Example

Current performance: 300 rows CSV takes 4 minutes
Expected after optimization: 300 rows CSV in 15-20 seconds
