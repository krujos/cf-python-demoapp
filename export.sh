export VCAP_SERVICES='{
  "lifecycle-sb": [
   {
    "credentials": {
     "password": "postgres",
     "uri": "jdbc:postgresql://52.0.106.208:5432/testdb",
     "username": "postgres"
    },
    "label": "lifecycle-sb",
    "name": "lifecycle-test",
    "plan": "prod",
    "tags": []
   }
  ]
 }'