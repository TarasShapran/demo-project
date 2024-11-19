pipeline {
    agent any
    environment {
        SECRET_KEY = credentials('SECRET_KEY')
        MYSQL_DATABASE = credentials('MYSQL_DATABASE_NAME')
        MYSQL_USER = credentials('MYSQL_USER')
        MYSQL_PASSWORD = credentials('MYSQL_PASSWORD')
        MYSQL_ROOT_PASSWORD = credentials('MYSQL_ROOT_PASSWORD')
        MYSQL_HOST = credentials('MYSQL_HOST')
        MYSQL_PORT = credentials('MYSQL_PORT')

        AWS_S3_REGION_NAME = credentials('AWS_S3_REGION_NAME') // замініть на фактичний регіон
        AWS_STORAGE_BUCKET_NAME = credentials('AWS_STORAGE_BUCKET_NAME')
        AWS_ACCESS_KEY_ID = credentials('AWS_ACCESS_KEY_ID')
        AWS_SECRET_ACCESS_KEY = credentials('AWS_SECRET_ACCESS_KEY')

        EMAIL_HOST = 'smtp.example.com' // замініть на фактичний хост
        EMAIL_HOST_USER = credentials('EMAIL_HOST_USER')
        EMAIL_HOST_PASSWORD = credentials('EMAIL_HOST_PASSWORD')
        EMAIL_PORT = 587

        AWS_ACCOUNT_ID = credentials('AWS_ACCOUNT_ID') // замініть на фактичний ID акаунта
        AWS_DEFAULT_REGION = credentials('AWS_DEFAULT_REGION') // замініть на фактичний регіон
        ECR_REPOSITORY = credentials('ECR_REPOSITORY')
        IMAGE_TAG = 'latest'
        S3_BUCKET = credentials('AWS_STORAGE_BUCKET_NAME')// замініть на фактичне ім'я S3 бакету
        EB_APPLICATION_NAME = credentials('EB_APPLICATION_NAME') // замініть на назву Elastic Beanstalk додатку
        EB_ENVIRONMENT_NAME = credentials('EB_ENVIRONMENT_NAME') // замініть на назву середовища Elastic Beanstalk
    }
    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'master', url: 'https://github.com/TarasShapran/demo-project.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com/${ECR_REPOSITORY}:${IMAGE_TAG}")
                }
            }
        }

        stage('Push to ECR') {
            steps {
                script {
                    withAWS(credentials: 'aws-jenkins', region: "${AWS_DEFAULT_REGION}") {
                        sh "aws ecr get-login-password --region ${AWS_DEFAULT_REGION} | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com"
                        sh "docker tag ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com/${ECR_REPOSITORY}:${IMAGE_TAG} ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com/${ECR_REPOSITORY}:latest"
                        sh "docker push ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com/${ECR_REPOSITORY}:latest"
                    }
                }
            }
        }

        stage('Deploy to Elastic Beanstalk') {
            steps {
                script {
                    sh "zip -r deployment-package.zip Dockerrun.aws.json"
                    withAWS(credentials: 'aws-jenkins', region: "${AWS_DEFAULT_REGION}") {
                        sh "aws s3 cp deployment-package.zip s3://${S3_BUCKET}/${EB_APPLICATION_NAME}-${IMAGE_TAG}.zip"
                        sh "aws elasticbeanstalk create-application-version --application-name ${EB_APPLICATION_NAME} --version-label ${IMAGE_TAG} --source-bundle S3Bucket=${S3_BUCKET},S3Key=${EB_APPLICATION_NAME}-${IMAGE_TAG}.zip"
                        sh "aws elasticbeanstalk update-environment --application-name ${EB_APPLICATION_NAME} --environment-name ${EB_ENVIRONMENT_NAME} --version-label ${IMAGE_TAG}"
                    }
                }
            }
        }
    }
}
