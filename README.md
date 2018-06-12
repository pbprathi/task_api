Deploy the applications to the swarm cluster using docker stack.

Using simple python REST api, GET, PUT , DELETE Tasks to the mysql db.Python REST API in one container and mysql in other container and hoting on swarm cluster.
code available in the app.py https://github.com/pbprathi/task_api/blob/master/app.py.

Prerequsites:

  Assuming docker swarm is setup with one master node and two worker nodes.
  
  Master and Worker nodes are having ubuntu OS.
  
  All the nodes should have docker,docker-compose installed.
  
  
Setup a docker registry
    
  Swarm consists of multiple docker engines, a registry is required to distribute images to all of them.We can use private or public registry.here iam using private registry.
    
  Start the registry service using swarm command
  
        docker service create --name registry --publish published=5000,target=5000 registry:2
    
  check whether service is deployed or not using command -- docker service ls
    
  
Create a Dockerfile and paste the content from the https://github.com/pbprathi/task_api/blob/master/Dockerfile

Create a docker-compose.yml and paste the content from the https://github.com/pbprathi/task_api/blob/master/docker-compose-stack.yml

Image for the python rest api container build using the above mentioned docker file.

Start the app with docker-compose up -d build the python REST API image and pulls the mysql image if don't have it already  and create two containers.

check the app running the command

    docker-compose ps

test the app with curl 
    
    http://localhost:5001

bring the app down, using command
    
    docker-compose down

Push the generated image to the registry using command # docker-compose push
compose file taged the local registry for the python REST API image.

Now the stack is ready to deploy

    docker stack deploy --compose-file docker-compose.yml flask-app
    
check whether all the services deployed or not using command

    docker stack services flask-app
    
Access the REST API from the out side world using 

    http://<any node IP address>:5001/tasks
    
Note : Call the below URL update the app.py hostname as flask-sql and password as password provided in the docker-compose file.
          
       http://<IP address>:5001/createdb




  

  
