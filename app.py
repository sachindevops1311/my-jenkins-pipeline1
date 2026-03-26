from flask import Flask, request, jsonify, redirect, session, url_for
import json
import os
import requests
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'

# ─────────────────────────────────────────────
# KEYCLOAK CONFIG — update these values
# ─────────────────────────────────────────────
KEYCLOAK_SERVER    = 'http://13.233.53.167:8180'
REALM              = 'todo-app'
CLIENT_ID          = 'todo-flask-app'
CLIENT_SECRET      = 'YOUR_CLIENT_SECRET_HERE'   # ← paste from Keycloak
REDIRECT_URI       = 'http://13.233.53.167:5000/callback'

# Keycloak URLs
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
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

# ─────────────────────────────────────────────
# AUTH ROUTES
# ─────────────────────────────────────────────
@app.route('/login')
def login():
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

    # Exchange code for token
    token_response = requests.post(TOKEN_URL, data={
        'grant_type':    'authorization_code',
        'client_id':     CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'code':          code,
        'redirect_uri':  REDIRECT_URI,
    })

    tokens = token_response.json()

    if 'access_token' not in tokens:
        return f'Token error: {tokens}', 400

    # Get user info
    userinfo = requests.get(USERINFO_URL, headers={
        'Authorization': f'Bearer {tokens["access_token"]}'
    }).json()

    # Save to session
    session['user']         = userinfo
    session['access_token'] = tokens['access_token']

    return redirect('/')

@app.route('/logout')
def logout():
    token = session.get('access_token', '')
    session.clear()
    logout_redirect = (
        f"{LOGOUT_URL}"
        f"?client_id={CLIENT_ID}"
        f"&post_logout_redirect_uri=http://13.233.53.167:5000"
    )
    return redirect(logout_redirect)

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
                .input-area {{ display: flex; gap: 10px; margin-bottom: 25px; }}
                .input-area input {{
                    flex: 1;
                    padding: 14px 18px;
                    border-radius: 12px;
                    border: 1px solid rgba(255,255,255,0.2);
                    background: rgba(255,255,255,0.08);
                    color: white;
                    font-size: 1em;
                    outline: none;
                    transition: border 0.2s;
                }}
                .input-area input::placeholder {{ color: #718096; }}
                .input-area input:focus {{ border-color: #63b3ed; }}
                .priority-select {{
                    padding: 14px 10px;
                    background: rgba(255,255,255,0.08);
                    border: 1px solid rgba(255,255,255,0.2);
                    border-radius: 12px;
                    color: white;
                    font-size: 0.85em;
                    outline: none;
                    cursor: pointer;
                }}
                .priority-select option {{ background: #1a1a2e; }}
                .input-area button {{
                    padding: 14px 22px;
                    background: #63b3ed;
                    color: white;
                    border: none;
                    border-radius: 12px;
                    font-size: 1.3em;
                    cursor: pointer;
                    transition: background 0.2s, transform 0.1s;
                }}
                .input-area button:hover {{ background: #4299e1; transform: scale(1.05); }}
                .filters {{ display: flex; gap: 8px; margin-bottom: 20px; justify-content: center; }}
                .filter-btn {{
                    padding: 7px 18px;
                    border-radius: 20px;
                    border: 1px solid rgba(255,255,255,0.2);
                    background: transparent;
                    color: #a0aec0;
                    cursor: pointer;
                    font-size: 0.85em;
                    transition: all 0.2s;
                }}
                .filter-btn.active, .filter-btn:hover {{
                    background: #63b3ed;
                    color: white;
                    border-color: #63b3ed;
                }}
                .stats {{
                    display: flex;
                    justify-content: space-between;
                    margin-bottom: 20px;
                    padding: 12px 18px;
                    background: rgba(255,255,255,0.05);
                    border-radius: 12px;
                    font-size: 0.85em;
                    color: #a0aec0;
                }}
                .stats span {{ color: white; font-weight: bold; }}
                .todo-list {{ list-style: none; }}
                .todo-item {{
                    display: flex;
                    align-items: center;
                    gap: 12px;
                    padding: 14px 16px;
                    background: rgba(255,255,255,0.05);
                    border-radius: 12px;
                    margin-bottom: 10px;
                    border: 1px solid rgba(255,255,255,0.08);
                    transition: transform 0.2s;
                    animation: slideIn 0.3s ease;
                }}
                @keyframes slideIn {{
                    from {{ opacity: 0; transform: translateY(-10px); }}
                    to   {{ opacity: 1; transform: translateY(0); }}
                }}
                .todo-item:hover {{ transform: translateX(4px); }}
                .todo-item.completed {{ opacity: 0.5; }}
                .todo-item.completed .todo-text {{ text-decoration: line-through; color: #718096; }}
                .todo-check {{
                    width: 24px; height: 24px;
                    border-radius: 50%;
                    border: 2px solid rgba(255,255,255,0.3);
                    background: transparent;
                    cursor: pointer;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    flex-shrink: 0;
                    transition: all 0.2s;
                    font-size: 0.8em;
                    color: white;
                }}
                .todo-check:hover {{ border-color: #48bb78; }}
                .todo-check.done  {{ background: #48bb78; border-color: #48bb78; }}
                .todo-text {{ flex: 1; color: white; font-size: 0.95em; }}
                .todo-priority {{
                    padding: 3px 10px;
                    border-radius: 10px;
                    font-size: 0.75em;
                    font-weight: bold;
                }}
                .priority-high   {{ background: rgba(252,129,129,0.2); color: #fc8181; }}
                .priority-medium {{ background: rgba(246,173,85,0.2);  color: #f6ad55; }}
                .priority-low    {{ background: rgba(104,211,145,0.2); color: #68d391; }}
                .delete-btn {{
                    background: transparent;
                    border: none;
                    color: #fc8181;
                    cursor: pointer;
                    font-size: 1.1em;
                    padding: 4px 8px;
                    border-radius: 8px;
                    opacity: 0;
                    transition: background 0.2s;
                }}
                .todo-item:hover .delete-btn {{ opacity: 1; }}
                .delete-btn:hover {{ background: rgba(252,129,129,0.15); }}
                .empty {{ text-align: center; padding: 40px; color: #718096; }}
                .empty .empty-icon {{ font-size: 3em; margin-bottom: 10px; }}
                .clear-btn {{
                    width: 100%;
                    margin-top: 15px;
                    padding: 12px;
                    background: rgba(252,129,129,0.1);
                    border: 1px solid rgba(252,129,129,0.3);
                    border-radius: 12px;
                    color: #fc8181;
                    cursor: pointer;
                    font-size: 0.9em;
                    transition: background 0.2s;
                }}
                .clear-btn:hover {{ background: rgba(252,129,129,0.2); }}
                .footer {{ text-align: center; margin-top: 25px; color: #4a5568; font-size: 0.8em; }}
            </style>
        </head>
        <body>
            <div class="app">
                <div class="header">
                    <h1>✅ Todo App</h1>
                    <p>Secured with Keycloak • Deployed via Jenkins</p>
                </div>

                <!-- USER BAR -->
                <div class="user-bar">
                    <div class="user-info">
                        <div class="avatar">{username[0].upper()}</div>
                        <div class="user-details">
                            <div class="name">👋 {username}</div>
                            <div class="email">{email}</div>
                        </div>
                    </div>
                    <a href="/logout" class="logout-btn">🚪 Logout</a>
                </div>

                <div class="input-area">
                    <input type="text" id="todoInput" placeholder="Add a new task..." onkeypress="handleKey(event)" />
                    <select class="priority-select" id="prioritySelect">
                        <option value="medium">🟡 Med</option>
                        <option value="high">🔴 High</option>
                        <option value="low">🟢 Low</option>
                    </select>
                    <button onclick="addTodo()">+</button>
                </div>

                <div class="filters">
                    <button class="filter-btn active" onclick="setFilter('all', this)">All</button>
                    <button class="filter-btn" onclick="setFilter('active', this)">Active</button>
                    <button class="filter-btn" onclick="setFilter('completed', this)">Completed</button>
                </div>

                <div class="stats">
                    <div>Total: <span id="totalCount">0</span></div>
                    <div>Active: <span id="activeCount">0</span></div>
                    <div>Done: <span id="doneCount">0</span></div>
                </div>

                <ul class="todo-list" id="todoList"></ul>
                <button class="clear-btn" onclick="clearCompleted()">🗑️ Clear Completed</button>

                <div class="footer">
                    🔐 Keycloak SSO • 🐳 Docker • ⚙️ Jenkins • ☁️ AWS EC2
                </div>
            </div>

            <script>
                let todos  = [];
                let filter = 'all';

                async function loadTodos() {{
                    const res = await fetch('/todos');
                    todos = await res.json();
                    render();
                }}
                async function addTodo() {{
                    const input    = document.getElementById('todoInput');
                    const priority = document.getElementById('prioritySelect').value;
                    const text     = input.value.trim();
                    if (!text) return;
                    const res  = await fetch('/todos', {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify({{ text, priority }})
                    }});
                    todos.push(await res.json());
                    input.value = '';
                    render();
                }}
                async function toggleTodo(id) {{
                    const res = await fetch(`/todos/${{id}}`, {{ method: 'PUT' }});
                    const updated = await res.json();
                    todos = todos.map(t => t.id === id ? updated : t);
                    render();
                }}
                async function deleteTodo(id) {{
                    await fetch(`/todos/${{id}}`, {{ method: 'DELETE' }});
                    todos = todos.filter(t => t.id !== id);
                    render();
                }}
                async function clearCompleted() {{
                    await fetch('/todos/completed', {{ method: 'DELETE' }});
                    todos = todos.filter(t => !t.completed);
                    render();
                }}
                function setFilter(f, btn) {{
                    filter = f;
                    document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                    btn.classList.add('active');
                    render();
                }}
                function handleKey(e) {{ if (e.key === 'Enter') addTodo(); }}
                function render() {{
                    const list     = document.getElementById('todoList');
                    const filtered = todos.filter(t => {{
                        if (filter === 'active')    return !t.completed;
                        if (filter === 'completed') return  t.completed;
                        return true;
                    }});
                    document.getElementById('totalCount').textContent  = todos.length;
                    document.getElementById('activeCount').textContent = todos.filter(t => !t.completed).length;
                    document.getElementById('doneCount').textContent   = todos.filter(t =>  t.completed).length;
                    if (filtered.length === 0) {{
                        list.innerHTML = `<div class="empty"><div class="empty-icon">📝</div><p>No tasks here!</p></div>`;
                        return;
                    }}
                    list.innerHTML = filtered.map(t => `
                        <li class="todo-item ${{t.completed ? 'completed' : ''}}">
                            <div class="todo-check ${{t.completed ? 'done' : ''}}" onclick="toggleTodo(${{t.id}})">
                                ${{t.completed ? '✓' : ''}}
                            </div>
                            <span class="todo-text">${{t.text}}</span>
                            <span class="todo-priority priority-${{t.priority}}">
                                ${{t.priority === 'high' ? '🔴 High' : t.priority === 'low' ? '🟢 Low' : '🟡 Med'}}
                            </span>
                            <button class="delete-btn" onclick="deleteTodo(${{t.id}})">✕</button>
                        </li>
                    `).join('');
                }}
                loadTodos();
            </script>
        </body>
    </html>
    '''

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
