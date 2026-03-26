import sys
sys.path.insert(0, '..')
from app import app

def test_hello():
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200
    assert b'Jenkins CI/CD Pipeline' in response.data
    print("✅ Test passed!")

if __name__ == '__main__':
    test_hello()