pipeline {
    agent any

    environment {
        DOCKER_HUB   = credentials('11708ce4-4145-4399-9573-3599390c1484')
        IMAGE_NAME   = 'sachin1311/jenkins-app'
        IMAGE_TAG    = "${BUILD_NUMBER ?: 'latest'}"   // FIX #6: fallback if BUILD_NUMBER is null
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
                        credentialsId: 'b460e8df-ada5-4733-bf6f-38d8db64dd26'   // FIX #4: added credentialsId for private repo
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
        // STAGE 3 : RUN TESTS  (moved before push)
        // FIX #2: tests now run INSIDE the container,
        //         not on the host Jenkins agent
        // FIX #5: test stage kept after build but before
        //         push so failures stop the pipeline early
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
        // FIX #3: removed 'pip install ansible' from
        //         every run — Ansible must be pre-installed
        //         on the agent (or use a dedicated Docker
        //         image).  Removed silent-fail '|| true'.
        // ─────────────────────────────────────────────
        stage('🚀 Deploy with Ansible') {
            steps {
                echo '======== STAGE 5: DEPLOY ========'
                sh '''
                    echo "Deploying application with Ansible..."

                    # Ansible must be pre-installed on this agent.
                    # Verify it is available before proceeding.
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
        // FIX #1: replaced bare sleep+curl with a proper
        //         retry loop so the check does not fail
        //         if the container needs a few seconds
        //         to become ready
        // ─────────────────────────────────────────────
        stage('✅ Verify Deployment') {
            steps {
                echo '======== STAGE 6: VERIFY ========'
                script {
                    // Check container is running
                    sh "docker ps | grep jenkins-app || echo '⚠️ Container not found in docker ps'"

                    // Health-check with retry — waits up to 60 s
                    timeout(time: 60, unit: 'SECONDS') {
                        waitUntil(initialRecurrencePeriod: 5000) {
                            def status = sh(
                                script: 'curl -sf http://localhost:5000',
                                returnStatus: true
                            )
                            if (status == 0) {
                                echo '✅ Application is running!'
                                return true
                            }
                            echo '⏳ Waiting for application to become ready...'
                            return false
                        }
                    }
                }
            }
        }
    }

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
}
