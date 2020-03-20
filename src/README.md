# WEB-API

### Installation
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

1. Please, import your project modules starting from the **'src'** folder. This is the folder which is specified as a root folder for the project modules autodiscovery.
In case, when some part of functionality is not working as expected, and you are sure in the correct implementation of functionality - please, __check you imports__.