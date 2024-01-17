pipeline {
    agent 'Built-In Node'
    stages {
        stage("verify tooling"){
            steps {
                sh docker compose up --build
            }
        }
    }
}