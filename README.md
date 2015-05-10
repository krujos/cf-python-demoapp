#Example python flask app for Cloud Foundry

Example cf pushable python app that reads from vcap services and talks to postgres. I built this for a talk about service brokers, so `lifecycle-db` is the name of a service that gets exposed. `export.sh` lets you test locally before pushing. It's tied to a table produced by `generator.py`