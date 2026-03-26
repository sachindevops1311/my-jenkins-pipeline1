# my-jenkins-pipeline1

## Overview
Complete CI/CD pipeline with Docker, Jenkins, and Ansible deployment.

## Pipeline Stages

### 1. 📋 Checkout Code
- Clones code from GitHub
- Verifies repository structure

### 2. 🔨 Build Docker Image
- Builds Docker image from Dockerfile
- Tags with build number
- Docker image: `sachindevops1311/jenkins-app:${BUILD_NUMBER}`

### 3. 🧪 Run Tests
- Runs unit tests with pytest
- Validates application functionality

### 4. 🐳 Push to Registry
- Logs into Docker Hub
- Pushes image to registry
- Available at: docker.io/sachindevops1311/jenkins-app

### 5. 🚀 Deploy with Ansible
- Stops old container
- Pulls new image
- Starts new container
- Ensures high availability

### 6. ✅ Verify Deployment
- Health checks
- Confirms application is running
- Tests connectivity

## Prerequisites

- Jenkins with Docker installed
- Docker Hub account
- Ansible installed on deployment server
- Git repository access

## Jenkins Credentials Required

1. **dockerhub-credentials**
   - Type: Username with password
   - Docker Hub credentials

2. (Optional) SSH key for Ansible deployment

## Running the Pipeline
```bash
# Trigger from Jenkins UI
Jenkins Dashboard → Select Job → Build Now

# Monitor execution
Check Console Output for detailed logs
```

## Expected Output
```
✅ Code checked out successfully
✅ Docker image built successfully
✅ All tests passed!
✅ Image pushed successfully
✅ Deployment completed!
✅ Application is running!
```

## Troubleshooting

### Docker Login Failed
- Verify credentials in Jenkins
- Check Docker Hub account status

### Tests Failed
- Review test output in console
- Check application code

### Ansible Deployment Failed
- Verify inventory configuration
- Check server connectivity
- Ensure Ansible is installed

## Environment Variables

- `IMAGE_NAME`: Docker image name
- `IMAGE_TAG`: Build number (auto-generated)
- `REGISTRY`: Docker registry URL

## Contact

For issues or questions, contact: sachindevops1311@gmail.com
