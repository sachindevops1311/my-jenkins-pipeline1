pipeline {
    agent any

    environment {
        DOCKER_HUB   = credentials('ee0498e9-6036-4ca7-a6dd-43755111651d')
        IMAGE_NAME   = 'sachin1311/jenkins-app'
        IMAGE_TAG    = "${BUILD_NUMBER ?: 'latest'}"
        REGISTRY     = 'docker.io'
    }

    stages {

        // ─────────────────────────────────────────────
        // STAGE 1 : CHECKOUT
        // ─────────────────────────────────────────────
        stage('📋 Checkout Code') {
            steps {
                echo '======== STAGE 1: CHECKOUT ========'
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: '*/main']],
                    userRemoteConfigs: [[
                        url: 'https://github.com/sachindevops1311/my-jenkins-pipeline1.git',
                        credentialsId: 'b37e9561-6853-4f13-863f-9c8885fda86d'
                    ]]
                ])
                sh 'echo "✅ Code checked out successfully"'
                sh 'ls -la'
            }
        }

        // ─────────────────────────────────────────────
        // STAGE 2 : BUILD DOCKER IMAGE
        // ─────────────────────────────────────────────
        stage('🔨 Build Docker Image') {
            steps {
                echo '======== STAGE 2: BUILD ========'
                sh '''
                    echo "Building Docker image: ${IMAGE_NAME}:${IMAGE_TAG}"
                    docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
                    docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${IMAGE_NAME}:latest
                    echo "✅ Docker image built successfully"
                    docker images | grep jenkins-app
                '''
            }
        }

        // ─────────────────────────────────────────────
        // STAGE 3 : RUN TESTS
        // ─────────────────────────────────────────────
        stage('🧪 Run Tests') {
            steps {
                echo '======== STAGE 3: TEST ========'
                sh '''
                    echo "Running unit tests inside Docker container..."
                    docker run --rm ${IMAGE_NAME}:${IMAGE_TAG} python -m pytest tests/test_app.py -v
                    echo "✅ All tests passed!"
                '''
            }
        }

        // ─────────────────────────────────────────────
        // STAGE 4 : PUSH TO DOCKER REGISTRY
        // ─────────────────────────────────────────────
        stage('🐳 Push to Docker Registry') {
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

        // ─────────────────────────────────────────────
        // STAGE 5 : DEPLOY WITH ANSIBLE
        // ─────────────────────────────────────────────
        stage('🚀 Deploy with Ansible') {
            steps {
                echo '======== STAGE 5: DEPLOY ========'
                sh '''
                    echo "Deploying application with Ansible..."

                    # Verify ansible is available
                    ansible --version

                    # Run the deployment playbook
                    ansible-playbook -i ansible/inventory.ini ansible/deploy.yml \
                        -e "docker_image=${IMAGE_NAME}:${IMAGE_TAG}" \
                        -v

                    echo "✅ Deployment completed!"
                '''
            }
        }

        // ─────────────────────────────────────────────
        // STAGE 6 : VERIFY DEPLOYMENT
        // ─────────────────────────────────────────────
        stage('✅ Verify Deployment') {
            steps {
                echo '======== STAGE 6: VERIFY ========'
                sh '''
                    echo "Checking container status..."

                    # Check container is running
                    docker ps | grep jenkins-app && \
                    echo "✅ Container is running!" || \
                    echo "⚠️ Container not found"

                    # Show container details
                    docker ps | grep jenkins-app

                    # Show app logs
                    docker logs jenkins-app --tail 10
                '''
            }
        }

    }   // closes stages

    // ─────────────────────────────────────────────────
    // POST ACTIONS
    // ─────────────────────────────────────────────────
    post {
        success {
            echo '✅ Pipeline executed successfully!'
            echo "🎉 Application deployed: ${IMAGE_NAME}:${IMAGE_TAG}"
        }
        failure {
            echo '❌ Pipeline failed! Check the logs above for details.'
        }
        always {
            echo '📊 Pipeline completed'
            cleanWs()
        }
    }

}   // closes pipeline
