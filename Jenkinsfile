pipeline {
    agent any
    node {
    withCredentials([string(credentialsId: 'demo_project', variable: 'secret')]) {
        script {
            def creds = readJSON text: secret
            env.SECRET_KEY = creds['SECRET_KEY']
            env.MYSQL_DATABASE = creds['MYSQL_DATABASE']
            env.MYSQL_USER = creds['MYSQL_USER']
            env.MYSQL_PASSWORD = creds['MYSQL_PASSWORD']
            env.MYSQL_ROOT_PASSWORD = creds['MYSQL_ROOT_PASSWORD']
            env.MYSQL_HOST = creds['MYSQL_HOST']
            env.MYSQL_PORT = creds['MYSQL_PORT']
            env.AWS_ACCESS_KEY_ID = creds['AWS_ACCESS_KEY_ID']
            env.AWS_SECRET_ACCESS_KEY = creds['AWS_SECRET_ACCESS_KEY']
            env.EMAIL_HOST_USER = creds['EMAIL_HOST_USER']
            env.EMAIL_HOST_PASSWORD = creds['EMAIL_HOST_PASSWORD']
            env.EMAIL_PORT = creds['EMAIL_PORT']
            env.AWS_ACCOUNT_ID = creds['AWS_ACCOUNT_ID']
            env.AWS_DEFAULT_REGION = creds['AWS_DEFAULT_REGION']
        }
        sh "aws sts get-caller-identity" // or whatever
        }
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
