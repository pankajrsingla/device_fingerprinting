#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
app.py: API endpoints for the Flask app for handling device fingerprinting verification.
"""

# Import modules
import concurrent.futures
from flask import Flask, request, jsonify
from fingerprint_handler import FingerprintHandler

fingerprint_handler = FingerprintHandler()

# Create and run the Flask app
app = Flask("Fingerprint_Verification")

@app.route('/check_fingerprint', methods=['GET', 'POST'])
def check_fingerprint():
    """
    API endpoint for checking fingerprints of target URLs, IP addresses, and IP ranges.
    Supports both GET and POST requests.
    Returns:
        dict: A dictionary containing the results of the fingerprint checks.
            The keys are the target IP addresses or IP ranges, and the values are the fingerprint matching results.
    """
    assert request.method in ["GET", "POST"], "Request should be either GET or POST."
    if request.method == 'POST':
        # Get the targets from the JSON payload of the POST request
        targets = request.json['targets']
    else:
        # Get the targets from the query parameters of the GET request
        targets = request.args.getlist('targets')
    
    # Use a ThreadPoolExecutor to parallelize the fingerprint checks
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Map the device_fingerprinting method over the targets
        results = executor.map(fingerprint_handler.device_fingerprinting, targets)
    return jsonify(list(results))

@app.route('/')
def index():
    """
    API endpoint for the root URL '/'
    Returns:
        str: A greeting message for the visitor.
    """
    return 'Hello, visitor!'

if __name__ == '__main__':
    # For making the output formatting easier to read
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
    app.run(debug=False, port=5000)