pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                echo "Build ...."
                sh "docker compose up --build"
            }
        }
    }
}