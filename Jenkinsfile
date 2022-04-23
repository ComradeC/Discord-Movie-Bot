pipeline {
    agent any

    stages {
        stage('Setup') {
            steps {
                script {
                    sh 'pip install -r requirements.txt'
                }
            }
        }
    }
}