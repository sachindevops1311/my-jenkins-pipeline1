from flask import Flask, request, jsonify, redirect, session, url_for
import json
import os
import requests
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'

# Test mode - set to True to skip Keycloak during testing
TEST_MODE = os.getenv('TEST_MODE', 'false').lower() == 'true'

# ─────────────────────────────────────────────
# KEYCLOAK CONFIG
# ─────────────────────────────────────────────
KEYCLOAK_SERVER    = os.getenv('KEYCLOAK_SERVER', 'http://13.233.53.167:8180')
REALM              = 'todo-app'
CLIENT_ID          = 'todo-flask-app'
CLIENT_SECRET      = os.getenv('CLIENT_SECRET', 'YOUR_CLIENT_SECRET_HERE')
REDIRECT_URI       = os.getenv('REDIRECT_URI', 'http://13.233.53.167:5000/callback')

AUTH_URL     = f'{KEYCLOAK_SERVER}/realms/{REALM}/protocol/openid-connect/auth'
TOKEN_URL    = f'{KEYCLOAK_SERVER}/realms/{REALM}/protocol/openid-connect/token'
USERINFO_URL = f'{KEYCLOAK_SERVER}/realms/{REALM}/protocol/openid-connect/userinfo'
LOGOUT_URL   = f'{KEYCLOAK_SERVER}/realms/{REALM}/protocol/openid-connect/logout'

TODOS_FILE = '/tmp/todos.json'

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def load_todos():
    if os.path.exists(TODOS_FILE):
        with open(TODOS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_todos(todos):
    with open(TODOS_FILE, 'w') as f:
        json.dump(todos, f)

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # Skip auth in test mode
        if TEST_MODE:
            if 'user' not in session:
                session['user'] = {'preferred_username': 'testuser', 'email': 'test@example.com'}
            return f(*args, **kwargs)
        
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

# ─────────────────────────────────────────────
# AUTH ROUTES
# ─────────────────────────────────────────────
@app.route('/login')
def login():
    if TEST_MODE:
        session['user'] = {'preferred_username': 'testuser', 'email': 'test@example.com'}
        return redirect('/')
    
    auth_redirect = (
        f"{AUTH_URL}"
        f"?client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&response_type=code"
        f"&scope=openid email profile"
    )
    return redirect(auth_redirect)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    if not code:
        return 'Login failed — no code received', 400

    try:
        token_response = requests.post(TOKEN_URL, data={
            'grant_type':    'authorization_code',
            'client_id':     CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'code':          code,
            'redirect_uri':  REDIRECT_URI,
        }, timeout=5)

        tokens = token_response.json()

        if 'access_token' not in tokens:
            return f'Token error: {tokens}', 400

        userinfo = requests.get(USERINFO_URL, headers={
            'Authorization': f'Bearer {tokens["access_token"]}'
        }, timeout=5).json()

        session['user']         = userinfo
        session['access_token'] = tokens['access_token']

        return redirect('/')
    except Exception as e:
        return f'Authentication error: {str(e)}', 500

@app.route('/logout')
def logout():
    token = session.get('access_token', '')
    session.clear()
    
    if TEST_MODE:
        return redirect('/')
    
    logout_redirect = (
        f"{LOGOUT_URL}"
        f"?client_id={CLIENT_ID}"
        f"&post_logout_redirect_uri=http://13.233.53.167:5000"
    )
    return redirect(logout_redirect)

# ─────────────────────────────────────────────
# HEALTH CHECK (for testing)
# ─────────────────────────────────────────────
@app.route('/health')
def health():
    return jsonify({'status': 'ok', 'test_mode': TEST_MODE}), 200

# ─────────────────────────────────────────────
# MAIN APP ROUTE
# ─────────────────────────────────────────────
@app.route('/')
@login_required
def index():
    user = session.get('user', {})
    username = user.get('preferred_username', 'User')
    email    = user.get('email', '')

    return f'''
    <!DOCTYPE html>
    <html>
        <head>
            <title>Todo App - Jenkins CI/CD</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{
                    font-family: Arial, sans-serif;
                    background: linear-gradient(135deg, #1a1a2e, #16213e, #0f3460);
                    min-height: 100vh;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    padding: 20px;
                }}
                .app {{
                    background: rgba(255,255,255,0.05);
                    backdrop-filter: blur(10px);
                    border-radius: 20px;
                    padding: 40px;
                    width: 100%;
                    max-width: 600px;
                    border: 1px solid rgba(255,255,255,0.1);
                    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                }}
                .header {{ text-align: center; margin-bottom: 30px; }}
                .header h1 {{ color: white; font-size: 2em; margin-bottom: 5px; }}
                .header p  {{ color: #a0aec0; font-size: 0.9em; }}
                .user-bar {{
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    background: rgba(255,255,255,0.05);
                    border-radius: 12px;
                    padding: 12px 16px;
                    margin-bottom: 25px;
                    border: 1px solid rgba(255,255,255,0.1);
                }}
                .user-info {{ display: flex; align-items: center; gap: 10px; }}
                .avatar {{
                    width: 36px; height: 36px;
                    background: #63b3ed;
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-weight: bold;
                    color: white;
                    font-size: 0.9em;
                }}
                .user-details .name  {{ color: white; font-size: 0.9em; font-weight: bold; }}
                .user-details .email {{ color: #a0aec0; font-size: 0.75em; }}
                .logout-btn {{
                    padding: 8px 16px;
                    background: rgba(252,129,129,0.15);
                    border: 1px solid rgba(252,129,129,0.3);
                    border-radius: 8px;
                    color: #fc8181;
                    cursor: pointer;
                    font-size: 0.85em;
                    text-decoration: none;
                    transition: background 0.2s;
                }}
                .logout-btn:hover {{ background: rgba(252,129,129,0.3); }}
                .footer {{ text-align: center; margin-top: 25px; color: #4a5568; font-size: 0.8em; }}
            </style>
        </head>
        <body>
            <div class="app">
                <div class="header">
                    <h1>✅ Todo App</h1>
                    <p>🔐 Secured with Keycloak • 🐳 Deployed via Jenkins</p>
                </div>

                <div class="user-bar">
                    <div class="user-info">
                        <div class="avatar">{username[0].upper() if username else 'U'}</div>
                        <div class="user-details">
                            <div class="name">👋 {username}</div>
                            <div class="email">{email}</div>
                        </div>
                    </div>
                    <a href="/logout" class="logout-btn">🚪 Logout</a>
                </div>

                <div class="footer">
                    🔐 Keycloak SSO • 🐳 Docker • ⚙️ Jenkins • ☁️ AWS EC2
                </div>
            </div>
        </body>
    </html>
    ''', 200

# ─────────────────────────────────────────────
# TODO API ROUTES (protected)
# ─────────────────────────────────────────────
@app.route('/todos', methods=['GET'])
@login_required
def get_todos():
    return jsonify(load_todos())

@app.route('/todos', methods=['POST'])
@login_required
def add_todo():
    todos = load_todos()
    data  = request.get_json()
    todo  = {
        'id':        len(todos) + 1,
        'text':      data.get('text', ''),
        'completed': False,
        'priority':  data.get('priority', 'medium')
    }
    todos.append(todo)
    save_todos(todos)
    return jsonify(todo)

@app.route('/todos/<int:todo_id>', methods=['PUT'])
@login_required
def toggle_todo(todo_id):
    todos = load_todos()
    for todo in todos:
        if todo['id'] == todo_id:
            todo['completed'] = not todo['completed']
            save_todos(todos)
            return jsonify(todo)
    return jsonify({'error': 'Not found'}), 404

@app.route('/todos/<int:todo_id>', methods=['DELETE'])
@login_required
def delete_todo(todo_id):
    todos = load_todos()
    todos = [t for t in todos if t['id'] != todo_id]
    save_todos(todos)
    return jsonify({'success': True})

@app.route('/todos/completed', methods=['DELETE'])
@login_required
def clear_completed():
    todos = load_todos()
    todos = [t for t in todos if not t['completed']]
    save_todos(todos)
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
