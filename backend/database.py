from flask_pymongo import PyMongo
import os

class MockPyMongo(PyMongo):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def init_app(self, app, **kwargs):
        from mongita import MongitaClientDisk
        
        # Ensure the DB is stored in the same directory as this file (backend/)
        base_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(base_dir, ".mongita_db")
        print(f" * Database Persistence Path: {db_path}")
        
        self.cx = MongitaClientDisk(host=db_path)
        self.db = self.cx['disease_prediction_db']
        
        # Basic Flask extension registration
        if app is not None:
             if not hasattr(app, 'extensions'):
                 app.extensions = {}
             app.extensions['pymongo'] = self

# mongo = PyMongo()
# FALLBACK: Using MockPyMongo (wrapped Mongita) because local MongoDB server is not running.
mongo = MockPyMongo()

