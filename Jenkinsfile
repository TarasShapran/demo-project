pipeline {
    agent any
    environment {
        AWS_REGION = 'us-east-1' // вкажіть потрібний регіон
    }
    stages {
        stage('Set AWS Credentials') {
            steps {
                withCredentials([string(credentialsId: 'ROOT_PASSWORD', variable: 'secret')]) {
                    script {
                        def creds = readJSON text: secret
                        env.AWS_ACCESS_KEY_ID = creds['MYSQL_ROOT_PASSWORD']
                    }
                }
            }
        }
        stage('Execute AWS Command') {
            steps {
                sh "aws sts get-caller-identity" // виконайте будь-яку необхідну команду
            }
        }

        stage('Show secret') {
            steps {
                echo "Using New Relic API Key: ${env.AWS_REGION}"
                echo "Using New Relic API Key: ${env.AWS_ACCESS_KEY_ID}"
            }
        }
    }
}