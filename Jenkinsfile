
pipeline {
    agent any

    stages {

        stage('Test') {
            steps {
                echo 'Esecuzione dei test pytest...'

                dir('/workspace') {
                    sh 'python3 -m pip install --break-system-packages -r requirements.txt'
                    sh 'python3 -m pytest -v'
                }
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