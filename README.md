# Steps to run and test the app:

### 1. Clone the Github repository.

### 2. Build the docker image.
```docker build -t device_fingerprinting .```

### 3. Run the docker container.
```docker run -d -p 5000:5000 device_fingerprinting```

### 4. Provide IP addresses of target devices to test the app in browser, for instance:
http://localhost:5000/check_fingerprint?targets=www.google.com&targets=185.199.112.2

### 5. To run the unit tests:
```python unit_tests.py```
- The error messages have been generated intentionally, for invalid inputs.
- The warning message is related to HTTPS certificate verification for Ubiquiti WAP, and can be ignored.
