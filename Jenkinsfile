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
        stage('Show running processes') {
            steps {
                script {
                    sh 'pm2 list'
                }
            }
        }
    }
}