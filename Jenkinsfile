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
                    sh 'pm2 start bot.py --name movie_bot --interpreter python3'
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