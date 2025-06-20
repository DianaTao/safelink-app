#!/usr/bin/env python3
"""
SafeLink App - Main Entry Point
A Flask application for connecting vulnerable populations with resources and support.
"""

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 