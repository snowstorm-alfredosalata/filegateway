#!/usr/bin/python3
from .app import setup_app

__author__ = "snowstorm-alfredosalata"
__copyright__ = "snowstorm-alfredosalata"
__license__ = "MIT"

def main():
    """
    Constructs and runs a Filegateway webapp.
    """
    app = setup_app()
    app.run(host='0.0.0.0', port=5000)
    
if __name__ == "__main__":
    main()