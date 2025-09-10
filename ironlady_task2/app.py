from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from models import Database, Student, Course, Enrollment
from summarizer import OllamaSummarizer
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'

# Initialize database and models
db = Database()
student_model = Student(db)
course_model = Course(db)
enrollment_model = Enrollment(db)
summarizer = OllamaSummarizer()

@app.route('/')
def index():
    """Dashboard showing overview"""
    students = student_model.get_all()
    courses = course_model.get_all()
    return render_template('index.html', 
                         student_count=len(students), 
                         course_count=len(courses))

@app.route('/students')
def students():
    """List all students"""
    all_students = student_model.get_all()
    return render_template('students.html', students=all_students)

@app.route('/courses')
def courses():
    """List all courses"""
    all_courses = course_model.get_all()
    return render_template('courses.html', courses=all_courses)

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    """Add new student"""
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form.get('phone', '')
        
        if student_model.create(name, email, phone):
            flash('Student added successfully!', 'success')
            return redirect(url_for('students'))
        else:
            flash('Error: Email already exists!', 'error')
    
    return render_template('add_student.html')

@app.route('/add_course', methods=['GET', 'POST'])
def add_course():
    """Add new course"""
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        content = request.form['content']
        instructor = request.form['instructor']
        duration_hours = int(request.form['duration_hours'])
        difficulty_level = request.form['difficulty_level']
        
        course_model.create(title, description, content, instructor, duration_hours, difficulty_level)
        flash('Course added successfully!', 'success')
        return redirect(url_for('courses'))
    
    return render_template('add_course.html')

@app.route('/course/<int:course_id>')
def course_detail(course_id):
    """View course details"""
    course = course_model.get_by_id(course_id)
    enrolled_students = enrollment_model.get_course_students(course_id)
    return render_template('course_detail.html', course=course, students=enrolled_students)

@app.route('/student/<int:student_id>')
def student_detail(student_id):
    """View student details"""
    student = student_model.get_by_id(student_id)
    if not student:
        flash('Student not found!', 'error')
        return redirect(url_for('students'))
    
    enrolled_courses = enrollment_model.get_student_courses(student_id)
    
    # Get all courses for enrollment modal
    all_courses = course_model.get_all()
    # Filter out already enrolled courses
    enrolled_course_ids = [course['id'] for course in enrolled_courses]
    available_courses = [course for course in all_courses if course['id'] not in enrolled_course_ids]
    
    return render_template('student_detail.html', 
                         student=student, 
                         courses=enrolled_courses,
                         available_courses=available_courses)


@app.route('/summarize_course/<int:course_id>')
def summarize_course(course_id):
    """Generate course content summary using Ollama"""
    try:
        course = course_model.get_by_id(course_id)
        if not course:
            return jsonify({'error': 'Course not found'}), 404
        
        if not course['content']:
            return jsonify({'error': 'No content to summarize'}), 400
            
        summary = summarizer.summarize_content(course['content'])
        return jsonify({'summary': summary})
        
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/generate_outline/<int:course_id>')
def generate_outline(course_id):
    """Generate course outline using Ollama"""
    try:
        course = course_model.get_by_id(course_id)
        if not course:
            return jsonify({'error': 'Course not found'}), 404
            
        outline = summarizer.generate_course_outline(course['title'], course['description'])
        return jsonify({'outline': outline})
        
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@app.route('/enroll', methods=['POST'])
def enroll_student():
    """Enroll student in course"""
    try:
        student_id = request.form.get('student_id')
        course_id = request.form.get('course_id')
        
        # Validate input
        if not student_id or not course_id:
            flash('Error: Missing student or course information!', 'error')
            return redirect(url_for('students'))
        
        # Convert to integers
        student_id = int(student_id)
        course_id = int(course_id)
        
        # Check if student and course exist
        student = student_model.get_by_id(student_id)
        course = course_model.get_by_id(course_id)
        
        if not student:
            flash('Error: Student not found!', 'error')
            return redirect(url_for('students'))
            
        if not course:
            flash('Error: Course not found!', 'error')
            return redirect(url_for('student_detail', student_id=student_id))
        
        # Attempt enrollment
        if enrollment_model.enroll_student(student_id, course_id):
            flash(f'Student {student["name"]} successfully enrolled in {course["title"]}!', 'success')
        else:
            flash('Error: Student is already enrolled in this course!', 'error')
    
    except ValueError:
        flash('Error: Invalid student or course ID!', 'error')
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
    
    return redirect(url_for('student_detail', student_id=student_id))


@app.route('/delete_student/<int:student_id>', methods=['POST'])
def delete_student(student_id):
    """Delete student"""
    student_model.delete(student_id)
    flash('Student deleted successfully!', 'success')
    return redirect(url_for('students'))

@app.route('/delete_course/<int:course_id>', methods=['POST'])
def delete_course(course_id):
    """Delete course"""
    course_model.delete(course_id)
    flash('Course deleted successfully!', 'success')
    return redirect(url_for('courses'))

if __name__ == '__main__':
    app.run(debug=True)
