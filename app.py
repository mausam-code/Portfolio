from flask import Flask, render_template, request, jsonify
from datetime import datetime
import json

app = Flask(__name__)

# Enhanced user data with more professional information
user_data = {
    'name': 'Season',
    'title': 'Full-Stack Developer',
    'bio': 'Passionate developer focused on building full-stack solutions using Django, React, and modern tooling. I love creating efficient, scalable applications that solve real-world problems.',
    'location': 'Kathmandu, Nepal',
    'skills': [
        {'name': 'Python', 'level': 90, 'category': 'backend'},
        {'name': 'Django', 'level': 85, 'category': 'backend'},
        {'name': 'Flask', 'level': 80, 'category': 'backend'},
        {'name': 'React', 'level': 75, 'category': 'frontend'},
        {'name': 'MySQL', 'level': 80, 'category': 'database'},
        {'name': 'REST API', 'level': 85, 'category': 'backend'},
        {'name': 'GIT', 'level': 90, 'category': 'tools'}
    ],
    'experience': [
        {
            'title': 'Full-Stack Developer',
            'company': 'Tech Solutions Inc.',
            'period': '2022 - Present',
            'description': 'Developed and maintained web applications using Django and React. Collaborated with cross-functional teams to deliver high-quality software solutions.'
        },
        {
            'title': 'Junior Developer',
            'company': 'Digital Agency',
            'period': '2021 - 2022',
            'description': 'Built responsive websites and worked on various client projects. Gained experience in full-stack development and agile methodologies.'
        }
    ],
    'projects': [
        {
            'title': 'Seasonal Agro Farm',
            'description': 'Full-stack solution built with Django and React, featuring user authentication, payment integration, and admin dashboard.',
            'technologies': ['Django', 'React', 'MySQL', 'Stripe API'],
            'github': 'https://github.com/mausam-code/Portfolio',
            'demo': 'https://seasonalagrofarm.com.np',
            'image': 'ecommerce.jpg'
        },
        {
            'title': 'FOREIGN EMPLOYMENT MANAGEMENT SYSTEM',
            'description': 'Modern blogging platform with rich text editor, comment system, and social sharing features built with Flask and React.',
            'technologies': ['Flask', 'React', 'PostgreSQL', 'REST API'],
            'github': 'https://github.com/mausam-code/',
            'demo': 'https://fancydecor.qa',
            'image': 'blog.jpg'
        },
        {
            'title': 'Analytics Dashboard',
            'description': 'Data visualization dashboard with real-time analytics, interactive charts, and export functionality.',
            'technologies': ['Python', 'Django', 'MySQL', 'Chart.js'],
            'github': 'https://github.com/mausam-code/analytics-dashboard',
            'demo': 'https://jkoverseas.com.np',
            'image': 'analytics.jpg'
        }
    ],
    'education': [
        {
            'degree': 'Bachelor of Computer Science',
            'institution': 'Tribhuvan University',
            'year': '2020',
            'description': 'Specialized in software engineering and web development'
        }
    ],
    'contact': {
        'email': 'seasonsinghrajak@gmail.com',
        'phone': '+977-9841234567',
        'github': 'https://github.com/mausam-code',
        'linkedin': 'https://linkedin.com/in/seasonsinghrajak',
        'website': 'https://seasonsingh.dev'
    },
    'testimonials': [
        {
            'name': 'John Smith',
            'position': 'Senior Developer',
            'company': 'Tech Solutions Inc.',
            'message': 'Season is a dedicated developer who consistently delivers high-quality code and innovative solutions.',
            'rating': 5
        },
        {
            'name': 'Sarah Johnson',
            'position': 'Project Manager',
            'company': 'Digital Agency',
            'message': 'Working with Season was a pleasure. His technical skills and problem-solving abilities are exceptional.',
            'rating': 5
        }
    ]
}

@app.route('/')
def home():
    """Main portfolio page"""
    return render_template('profile.html', user=user_data)

@app.route('/api/contact', methods=['POST'])
def handle_contact():
    """Handle contact form submissions"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'email', 'message']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # Here you would typically save to database or send email
        # For now, just log the message
        contact_message = {
            'name': data['name'],
            'email': data['email'],
            'message': data['message'],
            'timestamp': datetime.now().isoformat()
        }
        
        # Save to a simple JSON file (in production, use a proper database)
        try:
            with open('messages.json', 'r') as f:
                messages = json.load(f)
        except FileNotFoundError:
            messages = []
        
        messages.append(contact_message)
        
        with open('messages.json', 'w') as f:
            json.dump(messages, f, indent=2)
        
        return jsonify({'success': True, 'message': 'Message sent successfully!'})
    
    except Exception as e:
        return jsonify({'error': 'Something went wrong. Please try again.'}), 500

@app.route('/api/skills')
def get_skills():
    """API endpoint to get skills data"""
    return jsonify(user_data['skills'])

@app.route('/api/projects')
def get_projects():
    """API endpoint to get projects data"""
    return jsonify(user_data['projects'])

@app.route('/download-resume')
def download_resume():
    """Download resume functionality"""
    # In a real app, you would serve the actual PDF file
    return jsonify({'message': 'Resume download feature - implement PDF serving'})



# Add some useful template filters
@app.template_filter('year')
def year_filter(date_string):
    """Extract year from date string"""
    try:
        return datetime.strptime(date_string, '%Y-%m-%d').year
    except:
        return date_string

@app.template_filter('title_case')
def title_case_filter(text):
    """Convert text to title case"""
    return text.title()

# Context processor to make user data available in all templates
@app.context_processor
def inject_user_data():
    return dict(user=user_data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)