pipeline {
    agent any
    environment {
        SECRET_KEY = credentials('demoproject')
        MYSQL_DATABASE = credentials('MYSQL_DATABASE')
        MYSQL_USER = credentials('MYSQL_USER')
        MYSQL_PASSWORD = credentials('MYSQL_PASSWORD')
        MYSQL_ROOT_PASSWORD = credentials('MYSQL_ROOT_PASSWORD')
        MYSQL_HOST = credentials('MYSQL_HOST')
        MYSQL_PORT = credentials('MYSQL_PORT')
        AWS_S3_REGION_NAME = 'your-region' // замініть на фактичний регіон
        AWS_STORAGE_BUCKET_NAME = 'car_images'
        AWS_ACCESS_KEY_ID = credentials('AWS_ACCESS_KEY_ID')
        AWS_SECRET_ACCESS_KEY = credentials('AWS_SECRET_ACCESS_KEY')
        EMAIL_HOST = 'smtp.example.com' // замініть на фактичний хост
        EMAIL_HOST_USER = credentials('EMAIL_HOST_USER')
        EMAIL_HOST_PASSWORD = credentials('EMAIL_HOST_PASSWORD')
        EMAIL_PORT = 587
        AWS_ACCOUNT_ID = 'your-account-id' // замініть на фактичний ID акаунта
        AWS_DEFAULT_REGION = 'your-default-region' // замініть на фактичний регіон
        ECR_REPOSITORY = 'your-ecr-repository'
        IMAGE_TAG = 'latest'
        S3_BUCKET = 'your-s3-bucket' // замініть на фактичне ім'я S3 бакету
        EB_APPLICATION_NAME = 'your-eb-application' // замініть на назву Elastic Beanstalk додатку
        EB_ENVIRONMENT_NAME = 'your-eb-environment' // замініть на назву середовища Elastic Beanstalk
    }
    stages {
        stage('Check Secrets') {
            steps {
                script {
                    echo "DEMO_PROJECT: ${DEMO_PROJECT ? 'Loaded' : 'Not Loaded'}"
                    echo "MYSQL_DATABASE: ${MYSQL_DATABASE ? 'Loaded' : 'Not Loaded'}"
                    echo "AWS_ACCESS_KEY_ID: ${AWS_ACCESS_KEY_ID}"
                    echo "AWS_SECRET_ACCESS_KEY: ${AWS_SECRET_ACCESS_KEY}"
                    // додайте інші змінні для перевірки, якщо потрібно
                }
            }
        }

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
