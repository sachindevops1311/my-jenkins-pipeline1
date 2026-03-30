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
Setting Up Everything on New EC2

Step 1 — Connect to New EC2
ssh -i your-key.pem ubuntu@<NEW-EC2-IP>

Step 2 — Install Docker
# Update packages
 sudo apt-get update
# Install Docker
sudo apt-get install -y docker.io
# Start Docker
sudo systemctl start docker
sudo systemctl enable docker
# Add ubuntu user to docker group
sudo usermod -aG docker ubuntu
# Apply group change
newgrp docker
# Verify
docker --version

Step 3 — Run Jenkins Container
# Create volume
docker volume create jenkins_home
# Run Jenkins
docker run -d \
  --name jenkins \
  -p 8080:8080 \
  -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  jenkins/jenkins:lts
# Verify
docker ps

Step 4 — Install Docker CLI Inside Jenkins
# Enter Jenkins container as root
docker exec -u root -it jenkins bash
# Install Docker CLI
apt-get update && apt-get install -y docker.io
# Install Ansible
apt-get update
apt-get install -y python3-pip
pip3 install ansible --break-system-packages
# Create docker group with correct GID
stat -c '%g' /var/run/docker.sock   # ← note this number

groupadd -g <GID_NUMBER> docker     # ← use number from above

# Add jenkins to docker group
usermod -aG docker jenkins
# Exit
exit

Step 5 — Restart Jenkins
docker restart jenkins
# Test docker works as jenkins user
docker exec -u jenkins -it jenkins docker ps

Step 6 — Get Jenkins Admin Password
docker exec jenkins \
  cat /var/jenkins_home/secrets/initialAdminPassword

Step 7 — Open AWS Security Group Ports
AWS Console
→ EC2
→ Security Groups
→ Inbound Rules
→ Add these rules:

Port 22   → SSH        → 0.0.0.0/0
Port 8080 → Jenkins    → 0.0.0.0/0
Port 8180 → Keycloak   → 0.0.0.0/0
Port 5000 → Todo App   → 0.0.0.0/0


Step 8 — Setup Jenkins UI
Open → http://<NEW-EC2-IP>:8080
1. Paste admin password
2. Install suggested plugins
3. Create admin user
4. Save and finish

Step 9 — Add Credentials in Jenkins
Manage Jenkins
→ Credentials
→ System
→ Global Credentials
→ Add Credentials

# Docker Hub
Kind     : Username with password
Username : sachin1311
Password : your-dockerhub-token
ID       : 
# GitHub
Kind     : Username with password
Username : sachindevops1311
Password : your-github-token
ID       : 

Step 10 — Create Pipeline Job
Jenkins
→ New Item
→ Name: my-jenkins-pipeline
→ Type: Pipeline
→ OK

→ Pipeline section:
   Definition : Pipeline script from SCM
   SCM        : Git
   URL        : https://github.com/sachindevops1311/my-jenkins-pipeline1.git
   Branch     : */main
   Script Path: Jenkinsfile
→ Save


Push to GitHub:
git add app.py
git commit -m "Update: new EC2 IP address"
git push origin main

Step 13 — Build Pipeline
Jenkins → my-jenkins-pipeline → Build Now 🚀

Full Checklist
✅ Docker installed on EC2
✅ Jenkins container running (port 8080)
✅ Docker CLI inside Jenkins
✅ Ansible inside Jenkins
✅ Docker group permissions fixed
✅ Jenkins UI configured
✅ Docker Hub credentials added
✅ GitHub credentials added
✅ Pipeline job created
✅ Keycloak running (port 8180)
✅ app.py updated with new IP
✅ Pipeline triggered → Build Now
✅ App running on port 5000

Verify Everything Works
# All containers should be running
docker ps
# Expected output:
# jenkins      → 8080  ✅
# keycloak     → 8180  ✅
# jenkins-app  → 5000  ✅
Then visit:
http://<NEW-EC2-IP>:8080  → Jenkins  🔧
http://<NEW-EC2-IP>:5000  → Todo App ✅
🎉 Everything will be running on your new EC2!
<img width="1906" height="4324" alt="image" src="https://github.com/user-attachments/assets/13df6c57-3457-48a9-b950-8b1af8f476fe" />

