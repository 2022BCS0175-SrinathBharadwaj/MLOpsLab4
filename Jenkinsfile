pipeline {
    agent any

    environment {
        IMAGE = "2022bcs0175srinathbharadwaj/2022bcs0175-wine-api:latest"
        CONTAINER = "wine-api-test"
        PORT = "8000"
    }

    stages {

        stage('Pull Image') {
            steps {
                sh "docker pull ${IMAGE}"
            }
        }

        stage('Run Container') {
            steps {
                sh """
                docker rm -f ${CONTAINER} || true
                docker run -d -p ${PORT}:${PORT} --name ${CONTAINER} ${IMAGE}
                """
            }
        }

        stage('Wait for API') {
            steps {
                script {
                    echo "Waiting for API to start..."
                    sleep(15)
                }
            }
        }

        stage('Valid Inference Test') {
            steps {
                script {
                    sh '''
                    curl -X POST http://host.docker.internal:8000/predict \
                    -H "Content-Type: application/json" \
                    -d '{
                        "fixed acidity": 7.4,
                        "volatile acidity": 0.7,
                        "citric acid": 0,
                        "residual sugar": 1.9,
                        "chlorides": 0.076,
                        "free sulfur dioxide": 11,
                        "total sulfur dioxide": 34,
                        "density": 0.9978,
                        "pH": 3.51,
                        "sulphates": 0.56,
                        "alcohol": 9.4
                    }'
                    '''
                }
            }
        }

        stage('Invalid Input Test') {
            steps {
                script {
                    def bad = sh(
                        script: """
                        curl -s -X POST http://host.docker.internal:${PORT}/predict \
                        -H "Content-Type: application/json" \
                        -d '{"fixed acidity":"invalid"}'
                        """,
                        returnStdout: true
                    ).trim()

                    echo "Invalid Response: ${bad}"

                    if (!bad.toLowerCase().contains("error")) {
                        error("Invalid input did not trigger error")
                    }
                }
            }
        }

        stage('Stop Container') {
            steps {
                sh """
                docker stop ${CONTAINER} || true
                docker rm ${CONTAINER} || true
                """
            }
        }
    }

    post {
        always {
            sh "docker rm -f ${CONTAINER} || true"
        }
        success {
            echo "Inference Validation PASSED ✅"
        }
        failure {
            echo "Inference Validation FAILED ❌"
        }
    }
}