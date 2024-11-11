def opts = [
  parameters([])
]

properties(opts)

pipeline {
    agent any
    environment {
        SECRET_KEY = credentials('SECRET_KEY')
        MYSQL_DATABASE = credentials('MYSQL_DATABASE')
        MYSQL_USER=credentials('MYSQL_USER')
        MYSQL_PASSWORD=credentials('MYSQL_PASSWORD')
        MYSQL_ROOT_PASSWORD=credentials('MYSQL_ROOT_PASSWORD')
        MYSQL_HOST=credentials('MYSQL_HOST')
        MYSQL_PORT=credentials('MYSQL_PORT')
        AWS_S3_REGION_NAME='qwe'
        AWS_STORAGE_BUCKET_NAME='car_images'
        AWS_ACCESS_KEY_ID='qwe'
        AWS_SECRET_ACCESS_KEY='qwe'
        EMAIL_HOST='qwe'
        EMAIL_HOST_USER='qwe'
        EMAIL_HOST_PASSWORD='qwe'
        EMAIL_PORT=587
        AWS_ACCOUNT_ID='qwe'
        AWS_DEFAULT_REGION='qwe'
        ECR_REPOSITORY='qwe'
        IMAGE_TAG='qwe'
    }
    stages {
        stage('Checkout Code') {
            steps {
                // Use the Git plugin to check out code
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
                        sh "aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin public.ecr.aws/b2n3p6u5"
                        sh "docker tag ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/${ECR_REPOSITORY}:${IMAGE_TAG} public.ecr.aws/b2n3p6u5/projectcontainer:latest"
                        sh "docker push public.ecr.aws/b2n3p6u5/projectcontainer:latest"
                    }
                }
            }
        }

        stage('Deploy to Elastic Beanstalk') {
            steps {
                script {
                    // Zip the Dockerrun.aws.json for Elastic Beanstalk deployment
                    sh "zip -r deployment-package.zip Dockerrun.aws.json"


                    // Create a new application version and update the environment
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