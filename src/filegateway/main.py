from .app import setup_app

__author__ = "snowstorm-alfredosalata"
__copyright__ = "snowstorm-alfredosalata"
__license__ = "MIT"

def main():
    app = setup_app()
    app.run()
    
if __name__ == "__main__":
    main()