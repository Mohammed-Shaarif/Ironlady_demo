import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_name='course_management.db'):
        self.db_name = db_name
        self.init_database()
    
    def get_connection(self):
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        conn = self.get_connection()
        
        # Students table
        conn.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                phone TEXT,
                enrollment_date DATE DEFAULT CURRENT_DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Courses table with full content
        conn.execute('''
            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                content TEXT NOT NULL,
                instructor TEXT,
                duration_hours INTEGER,
                difficulty_level TEXT CHECK(difficulty_level IN ('Beginner', 'Intermediate', 'Advanced')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Student-Course enrollment relationship
        conn.execute('''
            CREATE TABLE IF NOT EXISTS enrollments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER,
                course_id INTEGER,
                enrollment_date DATE DEFAULT CURRENT_DATE,
                completion_status TEXT DEFAULT 'Enrolled' CHECK(completion_status IN ('Enrolled', 'In Progress', 'Completed', 'Dropped')),
                FOREIGN KEY (student_id) REFERENCES students (id) ON DELETE CASCADE,
                FOREIGN KEY (course_id) REFERENCES courses (id) ON DELETE CASCADE,
                UNIQUE(student_id, course_id)
            )
        ''')
        
        conn.commit()
        conn.close()

class Student:
    def __init__(self, db):
        self.db = db
    
    def create(self, name, email, phone=None):
        conn = self.db.get_connection()
        try:
            conn.execute(
                'INSERT INTO students (name, email, phone) VALUES (?, ?, ?)',
                (name, email, phone)
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()
    
    def get_all(self):
        conn = self.db.get_connection()
        students = conn.execute('SELECT * FROM students ORDER BY name').fetchall()
        conn.close()
        return students
    
    def get_by_id(self, student_id):
        conn = self.db.get_connection()
        student = conn.execute('SELECT * FROM students WHERE id = ?', (student_id,)).fetchone()
        conn.close()
        return student
    
    def delete(self, student_id):
        conn = self.db.get_connection()
        conn.execute('DELETE FROM students WHERE id = ?', (student_id,))
        conn.commit()
        conn.close()

class Course:
    def __init__(self, db):
        self.db = db
    
    def create(self, title, description, content, instructor, duration_hours, difficulty_level):
        conn = self.db.get_connection()
        conn.execute(
            'INSERT INTO courses (title, description, content, instructor, duration_hours, difficulty_level) VALUES (?, ?, ?, ?, ?, ?)',
            (title, description, content, instructor, duration_hours, difficulty_level)
        )
        conn.commit()
        conn.close()
    
    def get_all(self):
        conn = self.db.get_connection()
        courses = conn.execute('SELECT * FROM courses ORDER BY title').fetchall()
        conn.close()
        return courses
    
    def get_by_id(self, course_id):
        conn = self.db.get_connection()
        course = conn.execute('SELECT * FROM courses WHERE id = ?', (course_id,)).fetchone()
        conn.close()
        return course
    
    def delete(self, course_id):
        conn = self.db.get_connection()
        conn.execute('DELETE FROM courses WHERE id = ?', (course_id,))
        conn.commit()
        conn.close()

class Enrollment:
    def __init__(self, db):
        self.db = db
    
    def enroll_student(self, student_id, course_id):
        conn = self.db.get_connection()
        try:
            # Check if enrollment already exists
            existing = conn.execute(
                'SELECT id FROM enrollments WHERE student_id = ? AND course_id = ?',
                (student_id, course_id)
            ).fetchone()
            
            if existing:
                return False  # Already enrolled
            
            # Create new enrollment
            conn.execute(
                'INSERT INTO enrollments (student_id, course_id) VALUES (?, ?)',
                (student_id, course_id)
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()
    
    def get_student_courses(self, student_id):
        conn = self.db.get_connection()
        courses = conn.execute('''
            SELECT c.*, e.enrollment_date, e.completion_status 
            FROM courses c 
            JOIN enrollments e ON c.id = e.course_id 
            WHERE e.student_id = ?
            ORDER BY e.enrollment_date DESC
        ''', (student_id,)).fetchall()
        conn.close()
        return courses
    
    def get_course_students(self, course_id):
        conn = self.db.get_connection()
        students = conn.execute('''
            SELECT s.*, e.enrollment_date, e.completion_status 
            FROM students s 
            JOIN enrollments e ON s.id = e.student_id 
            WHERE e.course_id = ?
            ORDER BY e.enrollment_date DESC
        ''', (course_id,)).fetchall()
        conn.close()
        return students

