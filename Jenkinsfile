
pipeline {
    agent any

    stages {

        stage('Test') {
            steps {
                echo 'Esecuzione dei test pytest...'

                
                    sh 'python3 -m pip install --break-system-packages -r requirements.txt'
                    sh 'python3 -m pytest -v'
                
            }
        }

        stage('Docker Build') {
            steps {
                echo 'Creazione dell\'immagine Docker...'

                
                    sh 'docker build -t sentiment-api:jenkins .'
                
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploy dell\'API...'

                sh '''
                    docker stop sentiment-api || true
                    docker rm sentiment-api || true

                    docker run -d \
                        --name sentiment-api \
                        --network sentiment-analysis-devops_sentiment-network \
                        -p 5000:5000 \
                        sentiment-api:jenkins
                '''
            }
        }

    }

    post {
        success {
            echo 'Pipeline completata con successo!'
        }

        failure {
            echo 'Pipeline fallita!'
        }
    }
}