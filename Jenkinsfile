def opts = [
  parameters([
    booleanParam(name: 'DEPLOY_ALL', defaultValue: false, description: 'Deploy all'),
    booleanParam(name: 'RESTART_ENV', defaultValue: false, description: 'Restart main environment'),
    booleanParam(name: 'DEPLOY_BULK_SERVERS', defaultValue: false, description: 'Deploy bulk servers')
])
]

properties(opts)

pipeline {
    environment{
        CLEAR_CACHE = true
        TESTS = true
    }
    options {
        timeout(time: 1, unit: 'HOURS')
        timestamps()
    }
    agent any

    stages {
        stage('Clone branch') {
            when {
               not { environment name: 'BUILD_NUMBER', value: '1' }
            }
            steps {
                echo "Cloning ${BRANCH_NAME}...."
                sh  """ whoami ; ssh -vvv -t eidos@10.128.0.126 << "ENDSSH"
                    ~/scripts/clone.bash ${BRANCH_NAME}"""
            }
        }
        stage('Deploy all') {
            when {
               not { environment name: 'BUILD_NUMBER', value: '1' }
               expression { params.DEPLOY_ALL }
            }
            steps {
                echo 'Deploying....'
                sh ''' ssh -t eidos@10.128.0.126 << "ENDSSH"
                    ~/scripts/deploy.bash DEV all all
                    '''
            }
        }
        stage('Python: Clear template cache') {
            when {
               not { environment name: 'BUILD_NUMBER', value: '1' }
               expression { env.CLEAR_CACHE }
            }
            steps {
                withPythonEnv('python3.7') {
                    dir("python"){
                        sh 'pip3 install --upgrade pip'
                        sh 'pip3 install --quiet -r requirements.txt'
                        sh 'python3 clear_template_cache.py DEV'
                    }
                }
            }
        }
        stage('Execute Rundeck jobs') {
            when {
               not { environment name: 'BUILD_NUMBER', value: '1' }
               expression { params.RESTART_ENV }
            }
            steps {
                script {
                    step([$class: "RundeckNotifier",
                        includeRundeckLogs: true,
                        jobId: "18de9cab-f329-437e-b595-0f543a31ee1f",
                        rundeckInstance: "CFRA",
                        shouldFailTheBuild: true,
                        shouldWaitForRundeckJob: true,
                        tailLog: true])
                }
                script {
                    step([$class: "RundeckNotifier",
                        includeRundeckLogs: true,
                        jobId: "a510398e-bb96-47e8-98b0-95ba6e1bfd32",
                        rundeckInstance: "CFRA",
                        shouldFailTheBuild: true,
                        shouldWaitForRundeckJob: true,
                        tailLog: true])
                }
            }
        }
        stage('Python: Tests') {
            when {
               not { environment name: 'BUILD_NUMBER', value: '1' }
               expression { env.TESTS }
            }
            steps {
                withPythonEnv('python3.7') {
                    dir("python"){
                        sh 'python3 test_batch_endpoints.py DEV'
                    }
                }
            }
        }
        stage('Deploy bulk servers') {
            when {
               not { environment name: 'BUILD_NUMBER', value: '1' }
               expression { params.DEPLOY_BULK_SERVERS }
            }
            steps {
                script {
                    step([$class: "RundeckNotifier",
                        includeRundeckLogs: true,
                        jobId: "2ccd7141-e958-459d-ae0e-a28c86d2a23f",
                        rundeckInstance: "CFRA",
                        shouldFailTheBuild: true,
                        shouldWaitForRundeckJob: true,
                        tailLog: true])
                }
                echo 'Deploying bulk servers...'
                sh ''' ssh -t eidos@10.128.0.126 << "ENDSSH"
                    ~/scripts/deploy.bash DEVBULK worker all
                    '''
                sh ''' ssh -t eidos@10.128.0.126 << "ENDSSH"
                    ~/scripts/deploy.bash DEVBULK core all
                    '''
                sh ''' ssh -t eidos@10.128.0.126 << "ENDSSH"
                    ~/scripts/deploy.bash DEVBULK methmras all
                    '''
                script {
                    step([$class: "RundeckNotifier",
                        includeRundeckLogs: true,
                        jobId: "53266441-f9f2-46f9-9b33-3e27eafd3bff",
                        rundeckInstance: "CFRA",
                        shouldFailTheBuild: true,
                        shouldWaitForRundeckJob: true,
                        tailLog: true])
                }
            }
        }
    }
}