from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def profile():
    user = {
        'name': 'Season Singh Rajak',
        'bio': 'Passionate developer focused on building full-stack solutions using Django, React, and modern tooling.',
        'skills': ['Python','Django','Flask','React','MySQL','REST API','GIT'],
        'email': 'seasonsinghrajak@gmail.com',
        'github': 'https://github.com/mausam-code',
        'linkedin': 'https://linkedin.com/in/seasonsinghrajak' 
    }
    return render_template('profile.html', user=user)

if __name__ =='__main__':
    app.run(debug=True)