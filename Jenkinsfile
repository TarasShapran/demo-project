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
                    sh 'docker-compose -f docker-compose.yml up db'
                }
            }
        }

    stage('Build Docker app') {
            steps {
                script {
                    // Build the specific container from Docker Compose
                    sh 'docker-compose -f docker-compose.yml build app'
                    sh 'docker-compose -f docker-compose.yml up app'
                }
            }
        }

    stage('Build Docker web') {
            steps {
                script {
                    // Build the specific container from Docker Compose
                    sh 'docker-compose -f docker-compose.yml build web'
                    sh 'docker-compose -f docker-compose.yml up web'
                }
            }
        }

    stage('Build Docker celery') {
            steps {
                script {
                    // Build the specific container from Docker Compose
                    sh 'docker-compose -f docker-compose.yml build celery'
                    sh 'docker-compose -f docker-compose.yml up celery'
                }
            }
        }

    stage('Build Docker redis') {
            steps {
                script {
                    // Build the specific container from Docker Compose
                    sh 'docker-compose -f docker-compose.yml build redis'
                    sh 'docker-compose -f docker-compose.yml up redis'
                }
            }
        }

    stage('Build Docker flower') {
            steps {
                script {
                    // Build the specific container from Docker Compose
                    sh 'docker-compose -f docker-compose.yml build flower'
                    sh 'docker-compose -f docker-compose.yml up flower'
                }
            }
        }
    }
}