import mysql.connector
from config import DB_CONFIG

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

def insert_resume_data(data):
    conn = get_connection()
    cursor = conn.cursor()
    sql = """INSERT INTO resumes (name, email, phone, skills, summary, approved)
             VALUES (%s, %s, %s, %s, %s, %s)"""
    cursor.execute(sql, (
        data.get('name'),
        data.get('email'),
        data.get('phone'),
        ', '.join(data.get('skills', [])),
        data.get('summary'),
        0
    ))
    conn.commit()
    conn.close()

def get_all_data():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM resumes")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_pending_data():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM resumes WHERE approved=0")
    rows = cursor.fetchall()
    conn.close()
    return rows

def approve_record(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE resumes SET approved=1 WHERE id=%s", (id,))
    conn.commit()
    conn.close()