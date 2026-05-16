pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "hkprogrammer/venomous-ia-api"
        IMAGE_TAG = "prod-latest"
        K8S_ENV_FILE = "k8s/env/prod.env"
        K8S_RENDERED_DIR = "k8s-rendered"
        PYTHON_CI_IMAGE = "hkprogrammer/python-ci:3.10"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    docker run --rm \
                      -v "$PWD":/app \
                      -w /app \
                      ${PYTHON_CI_IMAGE} \
                      bash -c 'pwd && ls -la && pip install --upgrade pip && pip install -r requirements.txt && python -m pytest'
                '''
            }
        }

        stage('Docker Build') {
            steps {
                sh '''
                    docker build -t ${DOCKER_IMAGE}:${IMAGE_TAG} .
                '''
            }
        }

        stage('Docker Push') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub',
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

                    envsubst < k8s/configmap.yaml > ${K8S_RENDERED_DIR}/configmap.yaml
                    envsubst < k8s/secret.yaml > ${K8S_RENDERED_DIR}/secret.yaml
                    envsubst < k8s/deployment.yaml > ${K8S_RENDERED_DIR}/deployment.yaml
                    envsubst < k8s/service.yaml > ${K8S_RENDERED_DIR}/service.yaml
                    envsubst < k8s/ingress.yaml > ${K8S_RENDERED_DIR}/ingress.yaml
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