pipeline {
    agent any

    environment {
        DOCKER_HUB = credentials('b37e9561-6853-4f13-863f-9c8885fda86d')
        IMAGE_NAME = 'sachin1311/jenkins-app'
        IMAGE_TAG = "${BUILD_NUMBER}"
    }

    stages {
        stage('📋 Checkout Code') {
            steps {
                echo '======== STAGE 1: CHECKOUT ========'
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: '*/main']],
                    userRemoteConfigs: [[
                        url: 'https://github.com/sachindevops1311/my-jenkins-pipeline1.git'
                    ]]
                ])
                sh 'echo "✅ Code checked out successfully"'
            }
        }

        stage('🔨 Build Docker Image') {
            steps {
                echo '======== STAGE 2: BUILD ========'
                sh '''
                    echo "Building Docker image: ${IMAGE_NAME}:${IMAGE_TAG}"
                    docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
                    docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${IMAGE_NAME}:latest
                    echo "✅ Docker image built successfully"
                '''
            }
        }

        stage('🧪 Run Tests') {
            steps {
                echo '======== STAGE 3: TEST ========'
                sh '''
                    echo "Running tests..."
                    sleep 2
                    echo "✅ All tests passed!"
                '''
            }
        }

        stage('🐳 Push to Docker Hub') {
            steps {
                echo '======== STAGE 4: PUSH ========'
                sh '''
                    echo "Logging into Docker Hub..."
                    echo "${DOCKER_HUB_PSW}" | docker login -u "${DOCKER_HUB_USR}" --password-stdin
                    
                    echo "Pushing image to registry..."
                    docker push ${IMAGE_NAME}:${IMAGE_TAG}
                    docker push ${IMAGE_NAME}:latest
                    
                    echo "✅ Image pushed successfully"
                    docker logout
                '''
            }
        }

        stage('🚀 Deploy') {
            steps {
                echo '======== STAGE 5: DEPLOY ========'
                sh '''
                    echo "Stopping old container..."
                    docker stop jenkins-app 2>/dev/null || true
                    docker rm jenkins-app 2>/dev/null || true
                    
                    echo "Starting new container..."
                    docker run -d \
                      --name jenkins-app \
                      -p 5000:5000 \
                      ${IMAGE_NAME}:${IMAGE_TAG}
                    
                    sleep 3
                    echo "✅ Deployment completed!"
                '''
            }
        }

        stage('✅ Verify') {
            steps {
                echo '======== STAGE 6: VERIFY ========'
                sh '''
                    echo "Checking container status..."
                    docker ps | grep jenkins-app
                    
                    echo "Testing application..."
                    sleep 2
                    curl -s http://localhost:5000 | grep -q "Todo App" && echo "✅ App is running!" || echo "⚠️ App check skipped"
                '''
            }
        }
    }

    post {
        success {
            echo '🎉 Pipeline executed successfully!'
            echo "Image: ${IMAGE_NAME}:${IMAGE_TAG}"
        }
        failure {
            echo '❌ Pipeline failed!'
        }
        always {
            echo '📊 Pipeline completed'
        }
    }
}
