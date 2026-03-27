import sys
sys.path.insert(0, '..')

from app import app

def test_health():
    """Test health endpoint"""
    client = app.test_client()
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json['status'] == 'ok'
    print("✅ Health check passed!")

def test_index():
    """Test home page"""
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200
    assert b'Todo App' in response.data
    print("✅ Index page test passed!")

def test_get_todos():
    """Test getting todos"""
    client = app.test_client()
    response = client.get('/todos')
    assert response.status_code == 200
    assert isinstance(response.json, list)
    print("✅ GET /todos test passed!")

def test_add_todo():
    """Test adding a todo"""
    client = app.test_client()
    response = client.post('/todos',
        json={'text': 'Test task'},
        content_type='application/json'
    )
    assert response.status_code == 200
    todo = response.json
    assert todo['text'] == 'Test task'
    assert todo['completed'] == False
    print("✅ POST /todos test passed!")

def test_toggle_todo():
    """Test toggling a todo"""
    client = app.test_client()
    
    # Add a todo first
    add_res = client.post('/todos',
        json={'text': 'Toggle test'},
        content_type='application/json'
    )
    todo = add_res.json
    todo_id = todo['id']
    
    # Toggle it
    response = client.put(f'/todos/{todo_id}')
    assert response.status_code == 200
    assert response.json['completed'] == True
    print("✅ PUT /todos/{id} test passed!")

def test_delete_todo():
    """Test deleting a todo"""
    client = app.test_client()
    
    # Add a todo first
    add_res = client.post('/todos',
        json={'text': 'Delete test'},
        content_type='application/json'
    )
    todo_id = add_res.json['id']
    
    # Delete it
    response = client.delete(f'/todos/{todo_id}')
    assert response.status_code == 200
    assert response.json['success'] == True
    print("✅ DELETE /todos/{id} test passed!")

if __name__ == '__main__':
    print("\n🧪 Running Tests...\n")
    try:
        test_health()
        test_index()
        test_get_todos()
        test_add_todo()
        test_toggle_todo()
        test_delete_todo()
        print("\n✅ ALL TESTS PASSED!\n")
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}\n")
        raise
