# Course Management System

A comprehensive web application for managing students and courses with AI-powered content summarization built using Flask, SQLite, and Ollama.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [AI Integration](#ai-integration)
- [Database Schema](#database-schema)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)


## 🎯 Overview

The Course Management System is a full-stack web application designed to streamline the management of educational courses and student enrollments. It provides an intuitive interface for administrators to manage students, courses, and enrollments while leveraging AI capabilities for intelligent content summarization and course outline generation.

### Key Highlights

- **Complete CRUD Operations**: Add, view, update, and delete students and courses
- **Enrollment Management**: Seamlessly enroll students in courses with tracking
- **AI-Powered Features**: Generate course summaries and outlines using local LLM
- **Rich Course Content**: Store detailed course materials with full-text content
- **Responsive Design**: Mobile-friendly interface built with Bootstrap
- **Local AI Processing**: Privacy-focused AI summarization using Ollama


## ✨ Features

### Core Functionality

- 🎓 **Student Management**: Register and manage student profiles with contact information
- 📚 **Course Management**: Create comprehensive courses with detailed content, difficulty levels, and instructor information
- 📝 **Enrollment System**: Track student-course relationships with enrollment status
- 🎯 **Dashboard**: Overview of system statistics and quick navigation


### AI-Enhanced Features

- 🤖 **Content Summarization**: Generate concise summaries of course content using local LLM
- 📊 **Course Outline Generation**: Create structured course outlines based on title and description
- 🔒 **Privacy-First**: All AI processing happens locally via Ollama


### User Experience

- 📱 **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- ⚡ **Real-time Updates**: Dynamic content loading for AI features
- 🎨 **Modern UI**: Clean, professional interface with Bootstrap styling
- 🔍 **Easy Navigation**: Intuitive menu structure and breadcrumbs


## 🛠 Technologies Used

### Backend

- **Flask 2.3.3** - Python web framework
- **SQLite** - Lightweight database for data persistence
- **Python 3.8+** - Core programming language


### Frontend

- **HTML5/CSS3** - Structure and styling
- **Bootstrap 5.1.3** - Responsive CSS framework
- **JavaScript (ES6+)** - Dynamic client-side functionality
- **Fetch API** - Asynchronous data retrieval


### AI Integration

- **Ollama** - Local LLM inference server
- **LLaMA 3** - Default language model (configurable)
- **Requests** - HTTP client for API communication


### Development Tools

- **SQLite3** - Database management
- **Jinja2** - Template engine (included with Flask)


## 📁 Project Structure

```
course_management_app/
├── app.py                 # Main Flask application
├── models.py             # Database models and operations
├── summarizer.py         # AI integration with Ollama
├── init_db.py           # Database initialization script
├── requirements.txt      # Python dependencies
├── course_management.db  # SQLite database (auto-generated)
├── README.md            # Project documentation
└── templates/           # HTML templates
    ├── base.html        # Base template with navigation
    ├── index.html       # Dashboard/home page
    ├── students.html    # Student listing page
    ├── courses.html     # Course listing page
    ├── add_student.html # Student registration form
    ├── add_course.html  # Course creation form
    ├── student_detail.html # Individual student profile
    └── course_detail.html  # Individual course details
```


## 📋 Prerequisites

### System Requirements

- **Python 3.8 or higher**
- **pip** (Python package installer)
- **Git** (for cloning the repository)


### AI Requirements (Optional but Recommended)

- **Ollama** - For AI-powered summarization features
- **Minimum 8GB RAM** - For running local LLM models
- **4GB free disk space** - For model storage


## 🚀 Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd course_management_app
```


### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv course_management_env

# Activate virtual environment
# On Windows:
course_management_env\Scripts\activate

# On macOS/Linux:
source course_management_env/bin/activate
```


### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```


### 4. Install Ollama (Optional - for AI features)

```bash
# Visit https://ollama.ai for installation instructions
# Or use these commands:

# On macOS:
brew install ollama

# On Linux:
curl -fsSL https://ollama.ai/install.sh | sh

# On Windows:
# Download from https://ollama.ai/download
```


### 5. Download AI Model (Optional)

```bash
# Pull the default model
ollama pull llama3

# Or use a lighter model for lower-resource systems
ollama pull phi3:mini
```


### 6. Initialize Database

```bash
python init_db.py
```


## ⚙️ Configuration

### Environment Variables (Optional)

Create a `.env` file in the project root:

```env
# Flask Configuration
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here

# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3

# Database Configuration
DATABASE_PATH=course_management.db
```


### Ollama Configuration

To use a different model, update `summarizer.py`:

```python
# Change the default model
summarizer = OllamaSummarizer(model="phi3:mini")  # For lower resource usage
# or
summarizer = OllamaSummarizer(model="gemma:7b")   # For better performance
```


## 🎮 Usage

### 1. Start Ollama Server (Optional - for AI features)

```bash
ollama serve
```


### 2. Run the Flask Application

```bash
python app.py
```


### 3. Access the Application

Open your web browser and navigate to:

```
http://localhost:5000
```


### 4. Using the Application

#### Dashboard

- View system overview with student and course counts
- Quick navigation to all major sections


#### Managing Students

1. Click "Students" in the navigation menu
2. Use "Add New Student" to register students
3. Click on student names to view detailed profiles
4. Enroll students in courses via the student detail page

#### Managing Courses

1. Click "Courses" in the navigation menu
2. Use "Add New Course" to create comprehensive courses
3. Include detailed course content for AI summarization
4. View course details to see enrolled students

#### AI Features

1. Navigate to any course detail page
2. Click "AI Summary" to generate content summaries
3. Click "Generate Outline" to create structured course outlines
4. Results appear dynamically below the course content

## 🔗 API Endpoints

### Core Routes

| Method | Endpoint | Description |
| :-- | :-- | :-- |
| GET | `/` | Dashboard with system overview |
| GET | `/students` | List all students |
| GET | `/courses` | List all courses |
| GET | `/student/<id>` | Student detail page |
| GET | `/course/<id>` | Course detail page |

### Form Handling

| Method | Endpoint | Description |
| :-- | :-- | :-- |
| POST | `/add_student` | Create new student |
| POST | `/add_course` | Create new course |
| POST | `/enroll` | Enroll student in course |
| POST | `/delete_student/<id>` | Delete student |
| POST | `/delete_course/<id>` | Delete course |

### AI Features

| Method | Endpoint | Description |
| :-- | :-- | :-- |
| GET | `/summarize_course/<id>` | Generate course content summary |
| GET | `/generate_outline/<id>` | Generate course outline |

## 🤖 AI Integration

### Ollama Setup

The system integrates with Ollama for local AI processing:

1. **Install Ollama**: Follow instructions at [ollama.ai](https://ollama.ai)
2. **Start Server**: Run `ollama serve`
3. **Pull Model**: Download with `ollama pull llama3`

### Supported Models

- **llama3** (Recommended) - Best balance of quality and performance
- **phi3:mini** - Lightweight for low-resource systems
- **gemma:7b** - High-quality responses for powerful systems
- **codellama** - Specialized for technical content


### AI Features

- **Content Summarization**: Condenses course content into key points
- **Outline Generation**: Creates structured learning paths
- **Local Processing**: All AI happens on your machine for privacy
- **Error Handling**: Graceful degradation when AI is unavailable


## 🗄️ Database Schema

### Students Table

```sql
CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT,
    enrollment_date DATE DEFAULT CURRENT_DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```


### Courses Table

```sql
CREATE TABLE courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    content TEXT NOT NULL,
    instructor TEXT,
    duration_hours INTEGER,
    difficulty_level TEXT CHECK(difficulty_level IN ('Beginner', 'Intermediate', 'Advanced')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```


### Enrollments Table

```sql
CREATE TABLE enrollments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    course_id INTEGER,
    enrollment_date DATE DEFAULT CURRENT_DATE,
    completion_status TEXT DEFAULT 'Enrolled' CHECK(completion_status IN ('Enrolled', 'In Progress', 'Completed', 'Dropped')),
    FOREIGN KEY (student_id) REFERENCES students (id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses (id) ON DELETE CASCADE,
    UNIQUE(student_id, course_id)
);
```


## 🐛 Troubleshooting

### Common Issues

#### 1. AI Summarization Not Working

**Symptoms**: "AI Summary" button shows errors
**Solutions**:

```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Start Ollama if needed
ollama serve

# Verify model is installed
ollama list
ollama pull llama3  # If not installed
```


#### 2. Enrollment Not Working

**Symptoms**: Students not enrolling in courses
**Solutions**:

- Check browser console for JavaScript errors (F12)
- Verify form data is being submitted correctly
- Check Flask console for server errors
- Ensure database has proper foreign key constraints


#### 3. Database Errors

**Symptoms**: SQLite integrity errors
**Solutions**:

```bash
# Reinitialize database
rm course_management.db
python init_db.py
```


#### 4. Permission Issues

**Symptoms**: Cannot write to database file
**Solutions**:

```bash
# Fix file permissions (Unix/macOS)
chmod 664 course_management.db
chmod 755 .

# On Windows, ensure the user has write permissions to the directory
```


### Performance Optimization

#### For Low-Resource Systems

```python
# Use lighter AI model in summarizer.py
summarizer = OllamaSummarizer(model="phi3:mini")
```


#### For Better AI Performance

```python
# Use more powerful model
summarizer = OllamaSummarizer(model="llama3:70b")
```


### Debug Mode

Enable detailed error messages:

```python
# In app.py
app.run(debug=True)
```


## 🤝 Contributing

We welcome contributions to improve the Course Management System!

### Getting Started

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Add tests if applicable
5. Commit: `git commit -m 'Add amazing feature'`
6. Push: `git push origin feature/amazing-feature`
7. Open a Pull Request

### Development Guidelines

- Follow PEP 8 for Python code style
- Use meaningful commit messages
- Update documentation for new features
- Test thoroughly before submitting


### Areas for Contribution

- 📊 **Analytics Dashboard**: Add charts and reporting features
- 🔐 **Authentication**: Implement user login and role-based access
- 📱 **Mobile App**: Create companion mobile application
- 🌐 **Internationalization**: Add multi-language support
- 🔍 **Search**: Implement full-text search capabilities
- 📧 **Notifications**: Add email/SMS notifications
- 🎓 **Grading System**: Implement assignment and grading features


## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### MIT License Summary

- ✅ Commercial use
- ✅ Modification
- ✅ Distribution
- ✅ Private use
- ❌ Liability
- ❌ Warranty


## 🙏 Acknowledgments

- **Flask Community** - For the excellent web framework
- **Ollama Team** - For making local AI accessible
- **Bootstrap Team** - For the responsive UI framework
- **SQLite Team** - For the reliable embedded database


## 📞 Support

If you encounter any issues or have questions:

1. **Check the Troubleshooting section** above
2. **Search existing issues** in the repository
3. **Create a new issue** with detailed information:
    - Steps to reproduce
    - Expected behavior
    - Actual behavior
    - System information (OS, Python version, etc.)

## 🚀 Future Enhancements

- [ ] User authentication and authorization
- [ ] Advanced reporting and analytics
- [ ] Bulk operations for students and courses
- [ ] Integration with external learning management systems
- [ ] Advanced AI features (question generation, content recommendations)
- [ ] Mobile-responsive progressive web app (PWA)
- [ ] Real-time notifications and messaging
- [ ] Advanced search and filtering capabilities


