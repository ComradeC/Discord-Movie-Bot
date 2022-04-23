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
        stage('Run') {
            steps {
                script {
                    sh 'python3 bot.py'
                }
            }
        }
        stage('Show logs') {
            steps {
                script {
                    sh 'pm2 logs'
                }
            }
            post {
                failure {
                    script{
                        sh "exit 1"
                    }
                }
                unstable {
                    script{
                           sh "exit 1"
                     }
                }
            }
        }
    }
}