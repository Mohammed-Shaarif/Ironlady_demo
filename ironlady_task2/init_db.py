from models import Database, Student, Course

# Initialize database
db = Database()
student_model = Student(db)
course_model = Course(db)

# Add sample data
print("Adding sample students...")
student_model.create("John Doe", "john@example.com", "123-456-7890")
student_model.create("Jane Smith", "jane@example.com", "098-765-4321")
student_model.create("Mike Johnson", "mike@example.com", "555-123-4567")

print("Adding sample courses...")
course_model.create(
    "Introduction to Python Programming",
    "Learn the fundamentals of Python programming language",
    """
    This comprehensive Python course covers:
    - Python syntax and basic programming concepts
    - Data types: strings, numbers, lists, dictionaries, tuples
    - Control structures: if statements, loops, functions
    - Object-oriented programming concepts
    - File handling and error management
    - Working with libraries and modules
    - Building simple applications
    
    Students will complete hands-on projects including:
    1. Calculator application
    2. File organizer script
    3. Simple web scraper
    4. Data analysis with pandas
    
    By the end of this course, students will be able to write efficient Python programs and understand core programming principles.
    """,
    "Dr. Sarah Wilson",
    40,
    "Beginner"
)

course_model.create(
    "Machine Learning Fundamentals",
    "Introduction to machine learning algorithms and applications",
    """
    This course provides a solid foundation in machine learning:
    - Understanding different types of machine learning
    - Supervised learning: regression and classification
    - Unsupervised learning: clustering and dimensionality reduction
    - Model evaluation and validation techniques
    - Feature engineering and data preprocessing
    - Popular algorithms: linear regression, decision trees, random forests, SVM, k-means
    - Introduction to neural networks
    - Practical implementation using scikit-learn and Python
    
    Projects include:
    1. Predicting house prices using regression
    2. Image classification with neural networks
    3. Customer segmentation using clustering
    4. Sentiment analysis of text data
    
    Prerequisites: Basic Python programming and statistics knowledge.
    """,
    "Prof. Alex Chen",
    60,
    "Intermediate"
)

course_model.create(
    "Advanced Data Structures and Algorithms",
    "Deep dive into complex data structures and algorithmic problem solving",
    """
    Advanced course covering:
    - Complex data structures: heaps, tries, graphs, balanced trees
    - Algorithm analysis and Big O notation
    - Sorting and searching algorithms
    - Dynamic programming techniques
    - Graph algorithms: BFS, DFS, shortest path, minimum spanning tree
    - String algorithms and pattern matching
    - Computational complexity theory
    - Algorithm design strategies: divide and conquer, greedy algorithms
    
    Students will solve challenging problems and implement:
    1. Custom hash table with collision handling
    2. Graph traversal algorithms for social networks
    3. Dynamic programming solutions for optimization problems
    4. String matching algorithms for text processing
    
    This course prepares students for technical interviews and advanced computer science concepts.
    """,
    "Dr. Robert Kim",
    80,
    "Advanced"
)

print("Sample data added successfully!")
print("Run 'python app.py' to start the application")
