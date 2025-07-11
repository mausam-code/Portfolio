from flask import Flask, render_template, request, jsonify, send_from_directory
from datetime import datetime
import json
import os

app = Flask(__name__, static_folder='static')

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
            'company': 'Technology Pvt. Ltd.',
            'period': '2022 - Present',
            'description': 'Developed and maintained web applications using Django and React. Collaborated with cross-functional teams to deliver high-quality software solutions.'
        },
        {
            'title': 'Developer',
            'company': 'Digital Sansar',
            'period': '2011 - Present',
            'description': 'Built responsive websites and worked on various client projects. Gained experience in full-stack development and agile methodologies.'
        }
    ],
    'projects': [
        {
            'title': 'Seasonal Agro Farm',
            'description': "Season's Farmhouse Located in Siraha,Nepal.",
            'technologies': ['Django', 'React', 'MySQL', 'Stripe API'],
            'github': 'https://github.com/mausam-code/Agro-Farm',
            'demo': 'https://seasonalagrofarm.com.np',
            'image': 'ecommerce.jpg'
        },
        {
            'title': 'FANCY DECOR',
            'description': 'A Decoration Company Located in Doha, Qatar.',
            'technologies': ['Flask', 'React', 'PostgreSQL', 'REST API'],
            'github': 'https://github.com/mausam-code/',
            'demo': 'https://fancydecor.qa',
            'image': 'blog.jpg'
        },
        {
            'title': 'J.K OVERSEAS PVT. LTD.',
            'description': 'A Manpower Agency Situated in Kathmandu,Nepal. ',
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
            'description': 'Specialized in software development and web development'
        }
    ],
    'contact': {
        'email': 'seasonsinghrajak@gmail.com',
        'phone': '+977-9803645644',
        'github': 'https://github.com/mausam-code',
        'linkedin': 'https://linkedin.com/in/seasonsinghrajak',
        'website': 'https://season.name.np'
    },

}

@app.route('/')
def home():
    """Main portfolio page"""
    return render_template('main.html', user=user_data)

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
        messages_file = 'message.json'
        try:
            with open(messages_file, 'r') as f:
                messages = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            messages = []
        
        messages.append(contact_message)
        
        with open(messages_file, 'w') as f:
            json.dump(messages, f, indent=2)
        
        return jsonify({
            'success': True, 
            'message': 'I will get back to you soon!'
        })
    
    except Exception as e:
        app.logger.error(f"Error processing contact form: {str(e)}")
        return jsonify({
            'error': 'Something went wrong. Please try again.'
        }), 500
    
# serve static files
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

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
    # Create static directory if it doesn't exist
    if not os.path.exists('static'):
        os.makedirs('static')
    app.run(debug=True, host='0.0.0.0', port=5000)