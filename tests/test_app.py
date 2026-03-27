import sys
import os
sys.path.insert(0, '..')

# Enable test mode
os.environ['TEST_MODE'] = 'true'

from app import app

def test_health():
    """Test health check endpoint"""
    client = app.test_client()
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json['status'] == 'ok'
    print("✅ Health check test passed!")

def test_login_redirect():
    """Test that login redirects"""
    client = app.test_client()
    response = client.get('/login', follow_redirects=False)
    assert response.status_code == 302 or response.status_code == 200
    print("✅ Login test passed!")

def test_index():
    """Test home page with auth"""
    client = app.test_client()
    
    with client:
        response = client.get('/')
        assert response.status_code == 200
        assert b'Todo App' in response.data
        assert b'Keycloak' in response.data
        print("✅ Index page test passed!")

def test_todo_api():
    """Test todo API endpoints"""
    client = app.test_client()
    
    with client:
        # Access home page first (to set session)
        client.get('/')
        
        # Test getting todos
        response = client.get('/todos')
        assert response.status_code == 200
        assert isinstance(response.json, list)
        print("✅ GET /todos test passed!")
        
        # Test adding todo
        response = client.post('/todos',
            json={'text': 'Test task', 'priority': 'high'},
            content_type='application/json'
        )
        assert response.status_code == 200
        todo = response.json
        assert todo['text'] == 'Test task'
        assert todo['priority'] == 'high'
        print("✅ POST /todos test passed!")
        
        # Test toggling todo
        todo_id = todo['id']
        response = client.put(f'/todos/{todo_id}')
        assert response.status_code == 200
        assert response.json['completed'] == True
        print("✅ PUT /todos/{id} test passed!")
        
        # Test deleting todo
        response = client.delete(f'/todos/{todo_id}')
        assert response.status_code == 200
        print("✅ DELETE /todos/{id} test passed!")

def test_all():
    """Run all tests"""
    print("\n🧪 Running Todo App Tests...\n")
    try:
        test_health()
        test_login_redirect()
        test_index()
        test_todo_api()
        print("\n✅ ALL TESTS PASSED!\n")
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}\n")
        raise

if __name__ == '__main__':
    test_all()


Werkzeug==2.3.0
