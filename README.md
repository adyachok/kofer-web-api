# WEB-API


![alt text](img/scientist-ice-cart.png "Logo")


### Description
Web service provides API endpoint for interaction with data-science models and
scripts (called *runner* in the system). 

The service allows to the user to list available models, create an inference 
task, execute this task and check for results. 

**DISCLAIMER** Web service is the integral part of ZZ project, but because the 
project is build using **service choreography architecture pattern** there are 
no strong, tight relations in it. This means that every part of ZZ can be 
modified - removed - rewritten accordingly to the needs of customer.


### Main components
- **models** - this folder contains classes, which represent the main entities 
 in the service. Mostly all of them inherit from 
 [faust.Record](https://faust.readthedocs.io/en/latest/reference/faust.models.record.html).
 The Record class is used for serialization/deserialization of Python objects.
 - **app** - is the main entry point
 - **config** - contains all configuration settings/logic.
 - **agents** - that's the place where all the job is done. File contains logic
 to listen on events in Kafka channels.
 There are next channels:
    1. **model-metadata-updates** - stream of model metadata. On every model
    deployment service expect to find event in this stream. Event contains all 
    important model metadata.
    2. **model-task-do / model-tasks-done** - streams to send a model inference 
    task (event) and receive result event back.
    3. **runner-update** - stream of runner updates.
 - **repositories** - contains persistence logic
 - **views** - contains API endpoints description
    


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

### Debugging

We created instance of [Kafdrop](https://github.com/obsidiandynamics/kafdrop) with
the aim to facilitate debugging process. The running example instance can be found
in [BIX ZZ project](https://kafdrop-zz-test.22ad.bi-x.openshiftapps.com/)

Kafdrop has reach interface which helps a lot in tracking messages / events.

![alt text][kafdrop]

[kafdrop]: img/kafdrop.png "Title"

Yoiu can easily trace / read all messages in any topic:

![alt text][kafdrop_read]

[kafdrop_read]: img/kafdrop%202.png "Title"


### Known caveats

1. Please, import your project modules starting from the **'src'** folder. 
This is the folder which is specified as a root folder for the project 
modules autodiscovery.

In case, when some part of functionality is not working as expected, and you 
are sure in the correct implementation of functionality - 
please, __check you imports__.


### Questions
For questions, please, reach *andras.gyacsok@boehringer-ingelheim.com*