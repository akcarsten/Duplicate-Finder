pipeline {
    agent any

    triggers {
        cron('*/5 * * * *')
    }
    options {
        skipDefaultCheckout(true)
        // Keep the 10 most recent builds
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timestamps()
    }
    environment {
      PATH="/var/lib/jenkins/miniconda3/bin:$PATH"
      // CONFLUENCE_PAGE_CREDS = credentials('confluence-creds')
      // PAGE_ID = credentials('confluence-page-id')
    }

    stages {

        stage ("Code pull"){
            steps{
                checkout scm
            }
        }
        stage('Build environment') {
            steps {
                sh '''conda create --yes -n ${BUILD_TAG} python=3.8
                      source activate ${BUILD_TAG}
                      pip install -r requirements.txt
                    '''
            }
        }
        stage('Test environment') {
            steps {
                echo "Test coverage"
                sh  ''' source activate ${BUILD_TAG}
                        coverage run -m unittest
                        python -m coverage xml -o reports/coverage.xml
                    '''
                echo "Style check"
                sh  ''' source activate ${BUILD_TAG}
                        pylint test_detect_duplicates.py ./Duplicates/Duplicates.py || true
                    '''
            }
            
            post {
                always {
                    //cobertura coberturaReportFile: 'reports/coverage.xml'
                }
            }
    
            
        }

    stage('Unit tests') {
          steps {
              sh  ''' source activate ${BUILD_TAG}
                      py.test --junitxml reports/unit_tests.xml test_detect_duplicates.py
                  '''
          }
          post {
              always {
                  // Archive unit tests for the future
                  junit allowEmptyResults: true, testResults: 'reports/unit_tests.xml'
              }
          }
    }

            }
    post {
        always {
            sh 'conda remove --yes -n ${BUILD_TAG} --all'
        }
        failure {
            echo "Send e-mail, when failed"
        }
    }
}
