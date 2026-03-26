from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return '''
    <html>
        <head>
            <title>Jenkins CI/CD Pipeline Demo</title>
            <style>
                * { margin: 0; padding: 0; box-sizing: border-box; }
                body {
                    font-family: Arial, sans-serif;
                    background: linear-gradient(135deg, #1a1a2e, #16213e, #0f3460);
                    color: white;
                    min-height: 100vh;
                    padding: 40px 20px;
                }
                .container { max-width: 1000px; margin: 0 auto; }

                /* HEADER */
                .header {
                    text-align: center;
                    padding: 40px;
                    background: rgba(255,255,255,0.05);
                    border-radius: 20px;
                    margin-bottom: 30px;
                    border: 1px solid rgba(255,255,255,0.1);
                }
                .header h1 { font-size: 2.8em; margin-bottom: 10px; }
                .header p  { font-size: 1.2em; color: #a0aec0; }
                .badge {
                    display: inline-block;
                    background: #48bb78;
                    color: white;
                    padding: 6px 16px;
                    border-radius: 20px;
                    font-size: 0.9em;
                    margin-top: 15px;
                    animation: pulse 2s infinite;
                }
                @keyframes pulse {
                    0%   { box-shadow: 0 0 0 0 rgba(72,187,120,0.7); }
                    70%  { box-shadow: 0 0 0 10px rgba(72,187,120,0); }
                    100% { box-shadow: 0 0 0 0 rgba(72,187,120,0); }
                }

                /* ABOUT */
                .about {
                    background: rgba(255,255,255,0.05);
                    border-radius: 15px;
                    padding: 30px;
                    margin-bottom: 30px;
                    border: 1px solid rgba(255,255,255,0.1);
                }
                .about h2 { font-size: 1.6em; margin-bottom: 15px; color: #63b3ed; }
                .about p  { color: #a0aec0; line-height: 1.8; font-size: 1.05em; }

                /* PIPELINE FLOW */
                .pipeline {
                    background: rgba(255,255,255,0.05);
                    border-radius: 15px;
                    padding: 30px;
                    margin-bottom: 30px;
                    border: 1px solid rgba(255,255,255,0.1);
                }
                .pipeline h2 { font-size: 1.6em; margin-bottom: 20px; color: #63b3ed; }
                .stages {
                    display: flex;
                    flex-wrap: wrap;
                    gap: 10px;
                    align-items: center;
                    justify-content: center;
                }
                .stage {
                    background: rgba(255,255,255,0.08);
                    border-radius: 12px;
                    padding: 15px 20px;
                    text-align: center;
                    min-width: 130px;
                    border: 1px solid rgba(255,255,255,0.15);
                    transition: transform 0.2s;
                }
                .stage:hover { transform: translateY(-5px); }
                .stage .icon { font-size: 2em; margin-bottom: 8px; }
                .stage .name { font-size: 0.85em; color: #a0aec0; }
                .stage .label { font-size: 0.95em; font-weight: bold; }
                .arrow { font-size: 1.5em; color: #63b3ed; }

                /* TECH STACK */
                .tech {
                    background: rgba(255,255,255,0.05);
                    border-radius: 15px;
                    padding: 30px;
                    margin-bottom: 30px;
                    border: 1px solid rgba(255,255,255,0.1);
                }
                .tech h2 { font-size: 1.6em; margin-bottom: 20px; color: #63b3ed; }
                .tech-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 15px;
                }
                .tech-card {
                    background: rgba(255,255,255,0.08);
                    border-radius: 12px;
                    padding: 20px;
                    border-left: 4px solid;
                    transition: transform 0.2s;
                }
                .tech-card:hover { transform: translateY(-3px); }
                .tech-card.jenkins { border-color: #f6ad55; }
                .tech-card.docker  { border-color: #63b3ed; }
                .tech-card.ansible { border-color: #fc8181; }
                .tech-card.github  { border-color: #68d391; }
                .tech-card.flask   { border-color: #b794f4; }
                .tech-card.aws     { border-color: #fbd38d; }
                .tech-card .t-icon { font-size: 2em; margin-bottom: 10px; }
                .tech-card h3      { font-size: 1.1em; margin-bottom: 8px; }
                .tech-card p       { font-size: 0.85em; color: #a0aec0; line-height: 1.6; }

                /* HOW IT WORKS */
                .how {
                    background: rgba(255,255,255,0.05);
                    border-radius: 15px;
                    padding: 30px;
                    margin-bottom: 30px;
                    border: 1px solid rgba(255,255,255,0.1);
                }
                .how h2 { font-size: 1.6em; margin-bottom: 20px; color: #63b3ed; }
                .steps  { list-style: none; }
                .steps li {
                    display: flex;
                    align-items: flex-start;
                    gap: 15px;
                    padding: 15px 0;
                    border-bottom: 1px solid rgba(255,255,255,0.05);
                }
                .steps li:last-child { border-bottom: none; }
                .step-num {
                    background: #63b3ed;
                    color: white;
                    width: 32px;
                    height: 32px;
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-weight: bold;
                    flex-shrink: 0;
                    font-size: 0.9em;
                }
                .step-content h4 { margin-bottom: 4px; font-size: 1em; }
                .step-content p  { color: #a0aec0; font-size: 0.9em; line-height: 1.6; }

                /* FOOTER */
                .footer {
                    text-align: center;
                    padding: 20px;
                    color: #a0aec0;
                    font-size: 0.9em;
                }
            </style>
        </head>
        <body>
            <div class="container">

                <!-- HEADER -->
                <div class="header">
                    <h1>🚀 Jenkins CI/CD Pipeline</h1>
                    <p>Automated Build, Test & Deploy using DevOps Tools</p>
                    <div class="badge">✅ Application Deployed Successfully</div>
                </div>

                <!-- ABOUT PROJECT -->
                <div class="about">
                    <h2>📖 About This Project</h2>
                    <p>
                        This project demonstrates a fully automated <strong>CI/CD pipeline</strong> built using
                        industry-standard DevOps tools. The pipeline automatically pulls the latest code from
                        GitHub, builds a Docker image, runs automated tests, pushes the image to Docker Hub,
                        and deploys the application using Ansible — all triggered by a single click in Jenkins.
                        The entire application runs on <strong>AWS EC2</strong>, containerized with <strong>Docker</strong>.
                    </p>
                </div>

                <!-- PIPELINE FLOW -->
                <div class="pipeline">
                    <h2>🔄 CI/CD Pipeline Flow</h2>
                    <div class="stages">
                        <div class="stage">
                            <div class="icon">📋</div>
                            <div class="label">Checkout</div>
                            <div class="name">Pull from GitHub</div>
                        </div>
                        <div class="arrow">→</div>
                        <div class="stage">
                            <div class="icon">🔨</div>
                            <div class="label">Build</div>
                            <div class="name">Docker Image</div>
                        </div>
                        <div class="arrow">→</div>
                        <div class="stage">
                            <div class="icon">🧪</div>
                            <div class="label">Test</div>
                            <div class="name">PyTest Suite</div>
                        </div>
                        <div class="arrow">→</div>
                        <div class="stage">
                            <div class="icon">🐳</div>
                            <div class="label">Push</div>
                            <div class="name">Docker Hub</div>
                        </div>
                        <div class="arrow">→</div>
                        <div class="stage">
                            <div class="icon">🚀</div>
                            <div class="label">Deploy</div>
                            <div class="name">via Ansible</div>
                        </div>
                        <div class="arrow">→</div>
                        <div class="stage">
                            <div class="icon">✅</div>
                            <div class="label">Verify</div>
                            <div class="name">Health Check</div>
                        </div>
                    </div>
                </div>

                <!-- TECH STACK -->
                <div class="tech">
                    <h2>🛠️ Technology Stack</h2>
                    <div class="tech-grid">
                        <div class="tech-card jenkins">
                            <div class="t-icon">⚙️</div>
                            <h3>Jenkins</h3>
                            <p>CI/CD automation server that orchestrates the entire pipeline from code commit to deployment.</p>
                        </div>
                        <div class="tech-card docker">
                            <div class="t-icon">🐳</div>
                            <h3>Docker</h3>
                            <p>Containerizes the Flask application ensuring consistent runs across all environments.</p>
                        </div>
                        <div class="tech-card ansible">
                            <div class="t-icon">📦</div>
                            <h3>Ansible</h3>
                            <p>Automates deployment by pulling the Docker image and running the container on the server.</p>
                        </div>
                        <div class="tech-card github">
                            <div class="t-icon">🐙</div>
                            <h3>GitHub</h3>
                            <p>Source code repository. Every push to main branch triggers the Jenkins pipeline.</p>
                        </div>
                        <div class="tech-card flask">
                            <div class="t-icon">🐍</div>
                            <h3>Python Flask</h3>
                            <p>Lightweight web framework powering this application with PyTest for automated testing.</p>
                        </div>
                        <div class="tech-card aws">
                            <div class="t-icon">☁️</div>
                            <h3>AWS EC2</h3>
                            <p>Cloud infrastructure hosting both the Jenkins server and the deployed application.</p>
                        </div>
                    </div>
                </div>

                <!-- HOW IT WORKS -->
                <div class="how">
                    <h2>⚙️ How It Works</h2>
                    <ul class="steps">
                        <li>
                            <div class="step-num">1</div>
                            <div class="step-content">
                                <h4>📋 Code Checkout</h4>
                                <p>Jenkins pulls the latest code from the GitHub repository (main branch) using Git credentials.</p>
                            </div>
                        </li>
                        <li>
                            <div class="step-num">2</div>
                            <div class="step-content">
                                <h4>🔨 Docker Image Build</h4>
                                <p>Jenkins builds a Docker image from the Dockerfile, tagging it with the build number for versioning.</p>
                            </div>
                        </li>
                        <li>
                            <div class="step-num">3</div>
                            <div class="step-content">
                                <h4>🧪 Automated Testing</h4>
                                <p>PyTest runs inside the Docker container to validate the application. Pipeline stops if any test fails.</p>
                            </div>
                        </li>
                        <li>
                            <div class="step-num">4</div>
                            <div class="step-content">
                                <h4>🐳 Push to Docker Hub</h4>
                                <p>The verified image is pushed to Docker Hub registry with both a versioned tag and latest tag.</p>
                            </div>
                        </li>
                        <li>
                            <div class="step-num">5</div>
                            <div class="step-content">
                                <h4>🚀 Deploy with Ansible</h4>
                                <p>Ansible playbook pulls the new image, stops the old container, and starts the updated one automatically.</p>
                            </div>
                        </li>
                        <li>
                            <div class="step-num">6</div>
                            <div class="step-content">
                                <h4>✅ Verify Deployment</h4>
                                <p>Pipeline checks that the container is running and shows recent logs to confirm successful deployment.</p>
                            </div>
                        </li>
                    </ul>
                </div>

                <!-- FOOTER -->
                <div class="footer">
                    <p>🚀 Built with Jenkins • Docker • Ansible • AWS EC2 • Python Flask</p>
                    <p style="margin-top: 8px;">Pipeline runs automatically on every GitHub push to main branch</p>
                </div>

            </div>
        </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
