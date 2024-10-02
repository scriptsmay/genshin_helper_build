pipeline {
  agent {
    docker {
      reuseNode 'true'
      registryUrl 'https://coding-public-docker.pkg.coding.net'
      image 'public/docker/python:3.11-2022'
    }

  }
  stages {
    stage('检出') {
      steps {
        checkout([
          $class: 'GitSCM',
          branches: [[name: GIT_BUILD_REF]],
          userRemoteConfigs: [[
            url: GIT_REPO_URL,
            credentialsId: CREDENTIALS_ID
          ]]])
        }
      }
      stage('在python环境中跑test.py') {
        steps {
          script {
            // docker.image('python:3.12').inside('-e TZ=Asia/Shanghai') {
              //     sh 'python3 -V'
              //     echo '构建中...'
              //     sh '''echo "打印环境变量:"
// cat config.json
// '''
              //     sh 'python3 test.py'
              //     echo '构建完成.'
              //   }
              echo '先注释掉代码'
            }

            script {
              echo 'hello CODING'
              sh 'python3 test.py'
              echo '测试完成.'
            }

          }
        }
      }
    }