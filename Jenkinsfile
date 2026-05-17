pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "hkprogrammer/venomous-ia-api"
        IMAGE_TAG = "prod-latest"

        K8S_ENV_FILE = "k8s/env/prod.env"
        K8S_RENDERED_DIR = "k8s-rendered"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Docker Build') {
            steps {
                sh '''
                    docker build -t ${DOCKER_IMAGE}:${IMAGE_TAG} .
                '''
            }
        }

        stage('Run Tests Inside Image') {
            steps {
                sh '''
                    docker run --rm ${DOCKER_IMAGE}:${IMAGE_TAG} python -m pytest
                '''
            }
        }

        stage('Docker Push') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USERNAME',
                    passwordVariable: 'DOCKER_PASSWORD'
                )]) {
                    sh '''
                        echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
                        docker push ${DOCKER_IMAGE}:${IMAGE_TAG}
                    '''
                }
            }
        }

        stage('Render Kubernetes Manifests') {
            steps {
                sh '''
                    rm -rf ${K8S_RENDERED_DIR}
                    mkdir -p ${K8S_RENDERED_DIR}

                    set -a
                    . ${K8S_ENV_FILE}
                    export IMAGE_TAG=${IMAGE_TAG}
                    set +a

                    render_file() {
                        input_file=$1
                        output_file=$2

                        sed \
                          -e "s|\\${APP_ENV}|${APP_ENV}|g" \
                          -e "s|\\${K8S_NAMESPACE}|${K8S_NAMESPACE}|g" \
                          -e "s|\\${K8S_DEPLOYMENT}|${K8S_DEPLOYMENT}|g" \
                          -e "s|\\${K8S_SERVICE}|${K8S_SERVICE}|g" \
                          -e "s|\\${K8S_CONTAINER}|${K8S_CONTAINER}|g" \
                          -e "s|\\${INGRESS_HOST}|${INGRESS_HOST}|g" \
                          -e "s|\\${REPLICAS}|${REPLICAS}|g" \
                          -e "s|\\${MAX_SURGE}|${MAX_SURGE}|g" \
                          -e "s|\\${MAX_UNAVAILABLE}|${MAX_UNAVAILABLE}|g" \
                          -e "s|\\${CPU_REQUEST}|${CPU_REQUEST}|g" \
                          -e "s|\\${MEMORY_REQUEST}|${MEMORY_REQUEST}|g" \
                          -e "s|\\${CPU_LIMIT}|${CPU_LIMIT}|g" \
                          -e "s|\\${MEMORY_LIMIT}|${MEMORY_LIMIT}|g" \
                          -e "s|\\${IMAGE_TAG}|${IMAGE_TAG}|g" \
                          "$input_file" > "$output_file"
                    }

                    render_file k8s/venomous-ia-configmap.yaml ${K8S_RENDERED_DIR}/configmap.yaml
                    render_file k8s/venomous-ia-secret.yaml ${K8S_RENDERED_DIR}/secret.yaml
                    render_file k8s/venomous-ia-deployment.yaml ${K8S_RENDERED_DIR}/deployment.yaml
                    render_file k8s/venomous-ia-service.yaml ${K8S_RENDERED_DIR}/service.yaml
                    render_file k8s/venomous-ia-ingress.yaml ${K8S_RENDERED_DIR}/ingress.yaml

                    echo "Arquivos renderizados:"
                    ls -la ${K8S_RENDERED_DIR}
                '''
            }
        }

        stage('Deploy Kubernetes') {
            steps {
                sh '''
                    set -a
                    . ${K8S_ENV_FILE}
                    set +a

                    kubectl get namespace ${K8S_NAMESPACE} || kubectl create namespace ${K8S_NAMESPACE}

                    kubectl apply -f ${K8S_RENDERED_DIR}/configmap.yaml
                    kubectl apply -f ${K8S_RENDERED_DIR}/secret.yaml
                    kubectl apply -f ${K8S_RENDERED_DIR}/deployment.yaml
                    kubectl apply -f ${K8S_RENDERED_DIR}/service.yaml
                    kubectl apply -f ${K8S_RENDERED_DIR}/ingress.yaml

                    kubectl rollout status deployment/${K8S_DEPLOYMENT} \
                      -n ${K8S_NAMESPACE} \
                      --timeout=300s
                '''
            }
        }
    }

    post {
        always {
            sh 'docker logout || true'
        }

        success {
            echo 'Deploy do venomous-ia-api realizado com sucesso.'
        }

        failure {
            echo 'Falha no pipeline do venomous-ia-api.'
        }
    }
}