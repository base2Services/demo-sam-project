@Library('gus@feature/repo-scanner') _

pipeline {

  options {
    buildDiscarder(
      logRotator(
        numToKeepStr: '10',
        artifactNumToKeepStr: '10'
      )
    )
  }

  environment {
    AWS_REGION = 'ap-southeast-2'
    PROJECT_NAME = 'demo-sam'
    SOURCE_PREFIX = "cloudformation/${env.PROJECT_NAME}"
    TEMPLATE_URL = "https://${env.SOURCE_BUCKET}.s3.amazonaws.com/${env.SOURCE_PREFIX}"
    CFN_ROLE = "arn:aws:iam::${env.DEV_ACCOUNT_ID}:role/${env.CFN_ROLE_NAME}"
  }

  agent {
    label 'docker'
  }

  stages {

    stage('secret scan') {
      steps {
        secretScan()
      }
    }

    stage('Unit tests') {
      agent {
        docker {
          image 'python:3.8'
          label 'docker'
        }
      }
      steps {
        sh 'python setup.py test'
      }
      post {
        always {
            junit 'results.xml'
        }
      }
    }

    stage('Build and package') {
      agent {
        docker {
          image 'ghcr.io/base2services/sam-cli:1.21.1'
          args '-v /var/run/docker.sock:/var/run/docker.sock'
          label 'docker'
        }
      }
      steps {
        script {
          env['SHORT_COMMIT'] = env.GIT_COMMIT.substring(0,7)
          if(env.BRANCH_NAME == 'master') {
            env['CF_VERSION'] = "${env.SHORT_COMMIT}-${env.BUILD_NUMBER}"
          } else {
            env['CF_VERSION'] = env.BRANCH_NAME
          }
        }
        sh 'sam build --use-container'
        sh "sam package --s3-bucket ${env.SOURCE_BUCKET} --s3-prefix ${env.SOURCE_PREFIX}/${env.CF_VERSION} --output-template-file template.compiled.yaml --region ${env.AWS_REGION}"
        sh "aws s3 cp template.compiled.yaml s3://${env.SOURCE_BUCKET}/${env.SOURCE_PREFIX}/${env.CF_VERSION}/template.compiled.yaml --region ${env.AWS_REGION}"
      }
    }

    stage('Deploy Dev Stack') {
      environment {
        STACK_NAME = 'dev-sam-demo'
        ENVIRONMENT = 'dev'
      }
      steps {
        createChangeSet(
          description: env.GIT_COMMIT,
          region: env.AWS_REGION,
          stackName: env.STACK_NAME,
          templateUrl: "${env.TEMPLATE_URL}/${env.CF_VERSION}/template.compiled.yaml",
          parameters: [
            'Environment': env.ENVIRONMET_NAME
          ],
          tags: [
            'CreatedBy': 'gus'
          ],
          capabilities: false,
          awsAccountId: env.DEV_ACCOUNT_ID,
          role: env.CIINABOXV2_ROLE,
          roleArn: env.CFN_ROLE
        )

        // input(
        //   message: "Execute changes ${env.DEMO_CHANGESET_DEV_CHANGESET_NAME}"
        // )

        executeChangeSet(
          region: env.AWS_REGION,
          stackName: env.STACK_NAME,
          awsAccountId: env.DEV_ACCOUNT_ID,
          role: env.CIINABOXV2_ROLE,
          serviceRole: env.CFN_ROLE
        )
      }
    }



  }

}
