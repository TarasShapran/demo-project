pipeline {
    agent any
    environment {
        AWS_REGION = 'us-east-1'
    }
    stages {
        stage('Set AWS Credentials') {
            steps {
                withCredentials([string(credentialsId: 'ROOT_PASSWORD', variable: 'SECRET_JSON')]) {
                    script {
                        def secretData = readJSON text: SECRET_JSON
                        env.MYSQL_ROOT_PASSWORD = secretData['MYSQL_ROOT_PASSWORD']
                        env.MYSQL_DATABASE = secretData['MYSQL_DATABASE']
                    }
                }
            }
        }
        stage('Check Secrets') {
            steps {
                echo "MYSQL_ROOT_PASSWORD: ${env.MYSQL_ROOT_PASSWORD}"
                echo "MYSQL_DATABASE: ${env.MYSQL_DATABASE}"
            }
        }
    }
}