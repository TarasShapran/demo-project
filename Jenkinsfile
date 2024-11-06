def opts = [
  parameters([])
]

properties(opts)

pipeline {
    agent any
    environment {
        SECRET_KEY = credentials('aws-access-key-id')
        DEBUG = credentials('aws-secret-access-key')
        MYSQL_DATABASE = 'dockerapp'
        MYSQL_USER='qwe'
        MYSQL_PASSWORD='qwe'
        MYSQL_ROOT_PASSWORD='qwe'
        MYSQL_HOST='db'
        MYSQL_PORT=3306
        AWS_S3_REGION_NAME='qwe'
        AWS_STORAGE_BUCKET_NAME='car_images'
        AWS_ACCESS_KEY_ID='qwe'
        AWS_SECRET_ACCESS_KEY='qwe'
        EMAIL_HOST='qwe'
        EMAIL_HOST_USER='qwe'
        EMAIL_HOST_PASSWORD='qwe'
        EMAIL_PORT=587
    }
    stages {
        stage('Build Docker Images') {
            steps {
                // Збираємо образи Docker за допомогою Docker Compose
                sh 'docker-compose build'
            }
        }

        stage('Archive Project') {
            steps {
                // Створюємо архів проекту
                sh 'tar -czf demo-project.tar.gz *'
                archiveArtifacts artifacts: 'demo-project.tar.gz', allowEmptyArchive: false
            }
        }

        stage('Upload to S3') {
            steps {
                // Завантажуємо архів на S3
                sh '''
                aws s3 cp demo-project.tar.gz s3://${S3_BUCKET}/demo-project.tar.gz
                '''
            }
        }

        stage('Deploy to Elastic Beanstalk') {
            steps {
                // Налаштування деплою на Elastic Beanstalk за допомогою AWS CLI
                sh '''
                eb init -p docker your-eb-environment --region us-east-1
                eb deploy
                '''
            }
        }
    }
}