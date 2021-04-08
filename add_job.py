import requests
import base64
import sys
import string
import random

# TODO: communicate with context
# TODO: from libs import form


def generate_random_key():
    """
    example: 8a72a77e-2b4d-4ee6-9b8f-241a8864a393
    number of chars: 36
    positions of dashes: 8, 13, 18, 23
    range of chars: [0-9a-f]
    """
    return ''.join([
        ''.join(random.choices(string.hexdigits.lower(), k=8)), "-",
        ''.join(random.choices(string.hexdigits.lower(), k=4)), "-",
        ''.join(random.choices(string.hexdigits.lower(), k=4)), "-",
        ''.join(random.choices(string.hexdigits.lower(), k=4)), "-",
        ''.join(random.choices(string.hexdigits.lower(), k=12)),
    ])


def add_job_data(key, csrf_token):
    url_path = "http://0.0.0.0:9000/update-job"

    # TODO: data should be taken by a file (i.e YAML, json)
    data = {
        "csrf_token": csrf_token,
        "upload_key": key,
        "name": "libfuzzer_asan_linux_openssl",
        "platform": "LINUX",
        "dropdown-trigger": "undefined",
        "dropdown-content": "undefined",
        "prefix": "undefined",
        "label": "undefined",
        "input": "undefined",
        "suffix": "undefined",
        "add-on": "undefined",
        "fuzzers": "libFuzzer",
        "description": "",
        "templates": "libfuzzer\nengine_asan",
        "environment_string": "CORPUS_PRUNE=True"
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    r = requests.post(url_path, headers=headers, data=data)
    print(r.status_code)
    return


def add_job_file(key, zip_name):
    """
    files = {
        "value_1": (None, "12345"),
        "value_2": (None, "67890")
    }

    --85e90a4bbb05474ca1e23dbebdd68ed9
    Content-Disposition: form-data; name="value_1"

    12345
    --85e90a4bbb05474ca1e23dbebdd68ed9
    Content-Disposition: form-data; name="value_2"

    67890
    --85e90a4bbb05474ca1e23dbebdd68ed9--

    files = {'file': ('report.xls', open('report.xls', 'rb'),
    'application/vnd.ms-excel', {'Expires': '0'})}
    """

    url_path = "http://0.0.0.0:9008"

    # TODO: craft it programatically, the values are not that necessary
    policy_string = '{"expiration": "2021-03-06T13:40:35.264915Z", \
                      "conditions": [{"key": ' + key + '}, \
                                     {"bucket": "test-blobs-bucket"}, \
                                     ["content-length-range", 0, 16106127360], \
                                     ["starts-with", "$x-goog-meta-filename", ""]]}'

    policy_encoded = base64.b64encode(policy_string.encode("utf-8"))
    files = {
        "bucket": (None, "test-blobs-bucket"),
        "key": (None, key),
        "GoogleAccessId": (None, "service_account"),
        "policy": (None, policy_encoded),
        "signature": (None, "SIGNATURE"),
        "x-goog-meta-filename": (None, zip_name),
        "file": (zip_name, open(zip_name, "rb"), "application/zip")
    }

    r = requests.post(url_path, files=files)
    print(r.status_code)
    return


if __name__ == "__main__":

    # TODO: programmatically with communication to the context
    # csrf_token = form.generate_csrf_token()

    bucket_id = generate_random_key()
    zipfile = sys.argv[1]
    token = sys.argv[2]
    add_job_file(key=bucket_id, zip_name=zipfile)
    add_job_data(key=bucket_id, csrf_token=token)


