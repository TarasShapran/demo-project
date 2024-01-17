def opts = [
  parameters([])
]

properties(opts)

pipeline {
    agent any
    stages {
    stage('Build Docker db') {
            steps {
                script {
                    // Build the specific container from Docker Compose
                    sh 'docker-compose -f docker-compose.yml build db'
                }
            }
        }

    stage('Build Docker app') {
            steps {
                script {
                    // Build the specific container from Docker Compose
                    sh 'docker-compose build app'
                }
            }
        }

    stage('Build Docker web') {
            steps {
                script {
                    // Build the specific container from Docker Compose
                    sh 'docker-compose -f /docker-compose.yml build web'
                }
            }
        }

    stage('Build Docker celery') {
            steps {
                script {
                    // Build the specific container from Docker Compose
                    sh 'docker-compose -f /docker-compose.yml build celery'
                }
            }
        }

    stage('Build Docker redis') {
            steps {
                script {
                    // Build the specific container from Docker Compose
                    sh 'docker-compose build redis'
                }
            }
        }

    stage('Build Docker flower') {
            steps {
                script {
                    // Build the specific container from Docker Compose
                    sh 'docker-compose build flower'
                }
            }
        }
    }
}