pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                echo "Build ...."
                sh "docker --help"
                sh "docker --compose --build"
                sh "docker --compose --up"
            }
        }
    }
}