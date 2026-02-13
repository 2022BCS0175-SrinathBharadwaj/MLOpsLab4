pipeline {
    agent any

    environment {
        DOCKERHUB_USER = "2022bcs0175srinathbharadwaj"
        IMAGE_NAME = "2022bcs0175-wine-api"
        BEST_MSE = "9999"
    }

    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/2022BCS0175-SrinathBharadwaj/MLOpsLab4.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Train Model') {
            steps {
                sh 'python scripts/train.py'
            }
        }

        stage('Print Metrics') {
            steps {
                script {
                    def metrics = readJSON file: 'metrics.json'
                    echo "Name: Srinath Bharadwaj"
                    echo "Roll No: 2022BCS0175"
                    echo "MSE: ${metrics.mse}"
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${DOCKERHUB_USER}/${IMAGE_NAME}:latest ."
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds',
                                                  usernameVariable: 'USERNAME',
                                                  passwordVariable: 'PASSWORD')]) {

                    sh 'echo $PASSWORD | docker login -u $USERNAME --password-stdin'
                    sh "docker push ${DOCKERHUB_USER}/${IMAGE_NAME}:latest"
                }
            }
        }
    }
}
