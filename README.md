# WEB-API


### Description
Web service provides API endpoint for interaction with data-science models and
scripts (called *runner* in the system). 

The service allows to the user to list available models, create an inference 
task, execute this task and check for results. 

**DISCLAIMER** Web service is the integral part of ZZ project, but because the 
project is build using **service choreography architecture pattern** there are 
no strong, tight relations in it. This means that every part of ZZ can be 
modified - removed - rewritten accordingly to the needs of customer.


### Installation


#### Run locally


To run locally application requires Kafka broker and MongoDB.

To install seamlessly **Kafka** broker we recommend 
[Kafka-docker](https://github.com/wurstmeister/kafka-docker) project. 
In the project you can find **docker-compose-single-broker.yml**

We suggest to create next alias

```bash alias kafka="docker-compose --file {PATH_TO}/kafka-docker/docker-compose-single-broker.yml up```

For MongoDB thre can be found a few images, for example 
[mongo](https://hub.docker.com/_/mongo)


#### For local and dev/prod installations

1. Set MongoDB user:


    use admin
    
    db.auth(admin_user, admin_password)
    
    db.createUser(
       {
         user: "web_api",
         pwd: "secret",
         roles: [ 
            {role: "readWrite", db: "web-api"}
          ]
       }
    )

2. Set Kafka topics:
    
        oc exec -it bus-kafka-1 -c kafka -- bin/kafka-topics.sh --bootstrap-server localhost:9092 --topic model-tasks-do --create --partitions 3 --replication-factor 3
        oc exec -it bus-kafka-1 -c kafka -- bin/kafka-topics.sh --bootstrap-server localhost:9092 --topic model-tasks-done --create --partitions 3 --replication-factor 3


### Known caveats

1. Please, import your project modules starting from the **'src'** folder. 
This is the folder which is specified as a root folder for the project 
modules autodiscovery.

In case, when some part of functionality is not working as expected, and you 
are sure in the correct implementation of functionality - 
please, __check you imports__.


### Questions
For questions, please, reach *andras.gyacsok@boehringer-ingelheim.com*