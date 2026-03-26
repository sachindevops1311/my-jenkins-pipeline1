from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return '''
    <html>
        <head>
            <title>Jenkins Pipeline Demo</title>
            <style>
                body { font-family: Arial; background: #667eea; color: white; padding: 50px; }
                h1 { font-size: 2.5em; }
            </style>
        </head>
        <body>
            <h1>🚀 Jenkins CI/CD Pipeline</h1>
            <p>✅ Application deployed successfully!</p>
            <p>Built with: Docker, Jenkins, Ansible/Terraform</p>
        </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


