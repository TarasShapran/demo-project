pipeline {
    agent any
    environment {
        NEWRELIC_API_KEY = credentials('newrelic-api-key')
    }
    stages {
        stage('Foo') {
            steps {
                echo 'Hello world'
                echo "Using New Relic API Key: ${env.NEWRELIC_API_KEY}"
            }
        }
    }
}
