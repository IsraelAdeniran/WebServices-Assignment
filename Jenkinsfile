// Web Services Assignment - Jenkins Pipeline
// Student: B00157067

pipeline {
    agent any

    environment {
        MONGO_URI = credentials('MONGO_URI')
    }

    stages {

        // Pull the latest code from GitHub
        stage('Clone') {
            steps {
                git branch: 'main', url: 'https://github.com/IsraelAdeniran/WebServices-Assignment'
            }
        }

        // Build the Docker image
        stage('Build') {
            steps {
                sh 'docker build -t webservices-app .'
            }
        }

        // Run the Docker container with credentials passed securely
        stage('Run') {
            steps {
                sh 'docker run -d -p 8000:8000 --name webservices-container -e MONGO_URI=$MONGO_URI -e DB_NAME=productsDB webservices-app'
                sh 'sleep 10'
            }
        }

        // Run Newman tests
        stage('Test') {
            steps {
                sh 'newman run tests/collection.json'
            }
        }

        // Stop and remove the container
        stage('Stop') {
            steps {
                sh 'docker stop webservices-container'
                sh 'docker rm webservices-container'
            }
        }

        // Generate README.txt and zip everything
        stage('Package') {
            steps {
                sh '''echo "Web Services Assignment API
Endpoints:
- GET  /getSingleProduct/{product_id} - Returns a single product by ID
- GET  /getAll - Returns all products
- POST /addNew - Adds a new product (ProductID, Name, UnitPrice, StockQuantity, Description)
- DELETE /deleteOne/{product_id} - Deletes a product by ID
- GET  /startsWith/{letter} - Returns products starting with a letter
- GET  /paginate?start_id=1001&end_id=1010 - Returns up to 10 products between IDs
- GET  /convert/{product_id} - Returns product price converted to EUR
- GET  /metrics - Prometheus monitoring metrics
- GET  /docs - FastAPI Swagger documentation
Build date: $(date)" > README.txt'''
                sh 'zip -r complete-$(date +"%Y-%m-%d_%H-%M-%S").zip . -x "*.git*" -x ".venv/*" -x "venv/*"'
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: '*.zip', fingerprint: true
        }
    }
}