def opts = [
  parameters([])
]

properties(opts)

pipeline {
    agent any
    stages {
    stage('Install Docker Compose') {
        steps {
            script {
                // Перевірка наявності docker-compose
                def dockerComposeVersion = sh(script: 'docker-compose --version', returnStatus: true)
                if (dockerComposeVersion != 0) {
                    // Встановлення docker-compose, якщо він не знайдений
                    sh 'sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose'
                    sh 'sudo chmod +x /usr/local/bin/docker-compose'
                }
            }
        }
    }

    stage('Build Docker app') {
        steps {
            script {
                // Build the specific container from Docker Compose
                sh 'docker-compose -f docker-compose.yml build app'
            }
        }
    }

    stage('Build Docker db') {
            steps {
                script {
                    // Build the specific container from Docker Compose
                    sh 'docker-compose -f docker-compose.yml build db'
                }
            }
        }

    stage('Build Docker web') {
            steps {
                script {
                    // Build the specific container from Docker Compose
                    sh 'docker-compose -f docker-compose.yml build web'
                }
            }
        }

    stage('Build Docker celery') {
            steps {
                script {
                    // Build the specific container from Docker Compose
                    sh 'docker-compose -f docker-compose.yml build celery'
                }
            }
        }

    stage('Build Docker redis') {
            steps {
                script {
                    // Build the specific container from Docker Compose
                    sh 'docker-compose -f docker-compose.yml build redis'
                }
            }
        }

    stage('Build Docker flower') {
            steps {
                script {
                    // Build the specific container from Docker Compose
                    sh 'docker-compose -f docker-compose.yml build flower'
                }
            }
        }
    }
}