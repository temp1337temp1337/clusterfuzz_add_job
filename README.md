# clusterfuzz_add_job
Python script to simulate the "ADD JOB" programmatically in ClusterFuzz

# Usage
`python3 add_job.py openssl_fuzzer.zip <token_in_base64>`

## TODO
Except of the code refactoring, the `csrf_token` should be given programmatically. This should be integrated as described [here](https://github.com/google/clusterfuzz/issues/2279)
