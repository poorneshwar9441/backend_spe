pipeline{
    environment{
        backend_registry = 'spoider/pyth'
    }

    agent any

    stages {
        stage('Stage 1: Git pull')
        {
            steps{
               git url: 'https://github.com/poorneshwar9441/scientific_calculator.git',
               branch: 'main',
               credentialsId: ''
            }
        }

       stage('Stage 2: Testing')
       {
            steps{
                script{
                    
                      sh 'python3 -m venv myenv'
                      sh 'source myenv/bin/activate'
                      sh 'pip3 install --user django'
                      sh 'pip3 install --user djangorestframework'
                      sh 'pip3 install --user django-cors-headers'
                    
                }
            }
        }

        stage('Stage 3: Building Backend Docker image') {
            

            steps {
               script{
                    steps{
                         sh '/usr/local/bin/docker build -t '+backend_registry+':v1.0 .'
                    }
                } 
              }

        }
        

     stage('Stage 4: Pushing docker images to Dockerhub') {
        steps {
           script{
        
            sh '/usr/local/bin/docker login -u "gamergrange9@gmail.com" -p "docker_user"'
            sh '/usr/local/bin/docker push ' +backend_registry +':v1.0'
           } 
        }
           
    }
        
    stage('Stage 5: Clean docker images'){
            steps{
                 sh '/usr/local/bin/docker rmi $registry:v1.0'
            }
    }

    stage('Stage 6: Ansible Deployment') {
              steps{
                 sh 'echo dummy'
              }
          
        }
    }
}