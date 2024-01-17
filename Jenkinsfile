pipeline {
    agent 'Built-In Node'
    stages {
        stage("verify tooling"){
            steps {
                sh '''
                    docker version
                    docker info
                    docker compose version
                    curl --version
                    jd --version
                '''
            }
        }
    }
}