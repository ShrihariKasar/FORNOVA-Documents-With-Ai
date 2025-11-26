import os

UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'jpg', 'jpeg', 'png'}

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root2',
    'database': 'fornova_ai'
}