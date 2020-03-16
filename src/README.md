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
