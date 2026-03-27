from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

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

# ─────────────────────────────────────────────
# ROUTES
# ─────────────────────────────────────────────
@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
        <head>
            <title>✅ Todo App build by sachin - Jenkins CI/CD</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                * { margin: 0; padding: 0; box-sizing: border-box; }
                body {
                    font-family: Arial, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    padding: 20px;
                }
                .container {
                    background: white;
                    padding: 40px;
                    border-radius: 15px;
                    box-shadow: 0 10px 40px rgba(0,0,0,0.2);
                    max-width: 600px;
                    width: 100%;
                }
                h1 {
                    color: #333;
                    margin-bottom: 10px;
                    font-size: 2.5em;
                    text-align: center;
                }
                .subtitle {
                    color: #666;
                    text-align: center;
                    margin-bottom: 30px;
                    font-size: 0.95em;
                }
                .input-group {
                    display: flex;
                    gap: 10px;
                    margin-bottom: 30px;
                }
                input {
                    flex: 1;
                    padding: 12px 15px;
                    border: 2px solid #ddd;
                    border-radius: 8px;
                    font-size: 1em;
                }
                input:focus {
                    outline: none;
                    border-color: #667eea;
                }
                button {
                    padding: 12px 25px;
                    background: #667eea;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    cursor: pointer;
                    font-size: 1em;
                    font-weight: bold;
                }
                button:hover {
                    background: #764ba2;
                }
                .stats {
                    display: flex;
                    justify-content: space-around;
                    margin-bottom: 25px;
                    padding: 15px;
                    background: #f5f5f5;
                    border-radius: 8px;
                }
                .stat {
                    text-align: center;
                }
                .stat-number {
                    font-size: 1.8em;
                    font-weight: bold;
                    color: #667eea;
                }
                .stat-label {
                    color: #666;
                    font-size: 0.9em;
                }
                ul {
                    list-style: none;
                }
                li {
                    display: flex;
                    align-items: center;
                    gap: 12px;
                    padding: 15px;
                    background: #f9f9f9;
                    margin-bottom: 10px;
                    border-radius: 8px;
                    border-left: 4px solid #667eea;
                }
                input[type="checkbox"] {
                    width: 20px;
                    height: 20px;
                    cursor: pointer;
                }
                .todo-text {
                    flex: 1;
                    color: #333;
                    font-size: 1em;
                }
                li.completed .todo-text {
                    text-decoration: line-through;
                    color: #999;
                }
                .delete-btn {
                    background: #ff6b6b;
                    padding: 8px 12px;
                    font-size: 0.8em;
                    border-radius: 5px;
                }
                .delete-btn:hover {
                    background: #ff5252;
                }
                .empty {
                    text-align: center;
                    padding: 40px;
                    color: #999;
                }
                .footer {
                    text-align: center;
                    margin-top: 30px;
                    color: #999;
                    font-size: 0.85em;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>✅ Todo App</h1>
                <p class="subtitle">Deployed via Jenkins • Docker • AWS EC2</p>
                
                <div class="input-group">
                    <input type="text" id="todoInput" placeholder="Add a new task..." />
                    <button onclick="addTodo()">Add</button>
                </div>

                <div class="stats">
                    <div class="stat">
                        <div class="stat-number" id="totalCount">0</div>
                        <div class="stat-label">Total</div>
                    </div>
                    <div class="stat">
                        <div class="stat-number" id="activeCount">0</div>
                        <div class="stat-label">Active</div>
                    </div>
                    <div class="stat">
                        <div class="stat-number" id="doneCount">0</div>
                        <div class="stat-label">Done</div>
                    </div>
                </div>

                <ul id="todoList"></ul>

                <div class="footer">
                    🚀 Jenkins CI/CD Pipeline • 🐳 Docker • ☁️ AWS
                </div>
            </div>

            <script>
                let todos = [];

                async function loadTodos() {
                    const res = await fetch('/todos');
                    todos = await res.json();
                    render();
                }

                async function addTodo() {
                    const input = document.getElementById('todoInput');
                    const text = input.value.trim();
                    if (!text) return;

                    const res = await fetch('/todos', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ text })
                    });

                    todos.push(await res.json());
                    input.value = '';
                    render();
                }

                async function toggleTodo(id) {
                    const res = await fetch(`/todos/${id}`, { method: 'PUT' });
                    const updated = await res.json();
                    todos = todos.map(t => t.id === id ? updated : t);
                    render();
                }

                async function deleteTodo(id) {
                    await fetch(`/todos/${id}`, { method: 'DELETE' });
                    todos = todos.filter(t => t.id !== id);
                    render();
                }

                function render() {
                    const list = document.getElementById('todoList');
                    document.getElementById('totalCount').textContent = todos.length;
                    document.getElementById('activeCount').textContent = todos.filter(t => !t.completed).length;
                    document.getElementById('doneCount').textContent = todos.filter(t => t.completed).length;

                    if (todos.length === 0) {
                        list.innerHTML = '<div class="empty">📝 No tasks yet. Add one above!</div>';
                        return;
                    }

                    list.innerHTML = todos.map(t => `
                        <li class="${t.completed ? 'completed' : ''}">
                            <input type="checkbox" ${t.completed ? 'checked' : ''} 
                                   onchange="toggleTodo(${t.id})">
                            <span class="todo-text">${t.text}</span>
                            <button class="delete-btn" onclick="deleteTodo(${t.id})">Delete</button>
                        </li>
                    `).join('');
                }

                document.getElementById('todoInput').addEventListener('keypress', (e) => {
                    if (e.key === 'Enter') addTodo();
                });

                loadTodos();
            </script>
        </body>
    </html>
    ''', 200

@app.route('/todos', methods=['GET'])
def get_todos():
    return jsonify(load_todos())

@app.route('/todos', methods=['POST'])
def add_todo():
    todos = load_todos()
    data = request.get_json()
    todo = {
        'id': len(todos) + 1,
        'text': data.get('text', ''),
        'completed': False
    }
    todos.append(todo)
    save_todos(todos)
    return jsonify(todo)

@app.route('/todos/<int:todo_id>', methods=['PUT'])
def toggle_todo(todo_id):
    todos = load_todos()
    for todo in todos:
        if todo['id'] == todo_id:
            todo['completed'] = not todo['completed']
            save_todos(todos)
            return jsonify(todo)
    return jsonify({'error': 'Not found'}), 404

@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    todos = load_todos()
    todos = [t for t in todos if t['id'] != todo_id]
    save_todos(todos)
    return jsonify({'success': True})

@app.route('/health')
def health():
    return jsonify({'status': 'ok'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
