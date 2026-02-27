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
                docker run -d -p ${PORT}:${PORT} --name ${CONTAINER} ${IMAGE}
                """
            }
        }

        stage('Wait for API') {
            steps {
                script {
                    sleep(10)
                }
            }
        }

        stage('Valid Inference Test') {
            steps {
                script {
                    def response = sh(
                        script: """
                        curl -s -X POST http://localhost:${PORT}/predict \
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
                        """,
                        returnStdout: true
                    ).trim()

                    echo "Valid Response: ${response}"

                    if (!response.contains("wine_quality")) {
                        error("Prediction missing in valid response")
                    }
                }
            }
        }

        stage('Invalid Input Test') {
            steps {
                script {
                    def bad = sh(
                        script: """
                        curl -s -X POST http://localhost:${PORT}/predict \
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
        success {
            echo "Inference Validation PASSED ✅"
        }
        failure {
            echo "Inference Validation FAILED ❌"
        }
    }
}