[![Build Status](https://travis-ci.org/csfulop/learn_rest_by_example.svg?branch=master)](https://travis-ci.org/csfulop/learn_rest_by_example)
[![codecov](https://codecov.io/gh/csfulop/learn_rest_by_example/branch/master/graph/badge.svg)](https://codecov.io/gh/csfulop/learn_rest_by_example)
[![Requirements Status](https://requires.io/github/csfulop/learn_rest_by_example/requirements.svg?branch=master)](https://requires.io/github/csfulop/learn_rest_by_example/requirements/?branch=master)

# Learn REST by example

Simple phonebook app to learn about RESTful app development and a lot of related technologies
(some of them are quite general and not RESTful related, but still are needed and are useful knowledge):

* how to develop basic RESTful API with Python 3 / Pecan
* how to build python projects: setup.py / PBR / tox / py.test
* how to use different testing levels in your project: unit / functional / blackbox
* how to setup CI for the project: GitHub / Travis-CI / codecov / ...
* how to dockerize the app and how to test the dockerized app

## Try it

You can try the latest version with docker.

Pull and start the docker image:
```
$ docker run --rm -p 8080:8080 -d --name learn_rest_by_example csfulop/learn_rest_by_example
```
Because it stores entries in memory, your phonebook is empty after start up:
```
$ curl http://localhost:8080/phonebook
[]
```
You can add new entries:
```
$ curl http://localhost:8080/phonebook -X POST --data '{"name":"Alice","phone":"1234"}'
{"id": "9504ff00-c070-4e24-b3a0-56230ea616cf", "name": "Alice", "phone": "1234"}
```
You can see in the response that the entry got an id.
Which you can use to query a given entry:
```
$ curl http://localhost:8080/phonebook/9504ff00-c070-4e24-b3a0-56230ea616cf
{"id": "9504ff00-c070-4e24-b3a0-56230ea616cf", "name": "Alice", "phone": "1234"}
```
You can use JSON merge patch to modify entries:
```
$ curl http://localhost:8080/phonebook/9504ff00-c070-4e24-b3a0-56230ea616cf -X PATCH --data '{"phone":"4567","mobile":"5555"}'
{"id": "9504ff00-c070-4e24-b3a0-56230ea616cf", "name": "Alice", "phone": "4567", "mobile": "5555"}
```
If you don't need it anymore you can delete entries:
```
$ curl http://localhost:8080/phonebook/9504ff00-c070-4e24-b3a0-56230ea616cf -X DELETE
```
And finally stop the container with:
```
$ docker stop learn_rest_by_example
```

## How to continue?

The learning possibilites are almost endless. You can tweak the project into many different directions:

* create a fancy UI for your RESTful service
* reuse the business logic and learn other frameworks: Django, Flask, ...
* or even learn and do it in other programming languages: Java: Jersey, Spring Boot / Node.js: Express / ...
* learn about testing: BDD with Cucumber, performance testing with JMeter, ...
* instead of the simple in-memory backend use real databases: MongoDB, MariaDB, ...
* learn about software architecture best practices. 
  For example: create independent business logic which can be reused with different REST frameworks / databases
* how to deploy your app into different environments: AWS, OpenStack, ...
* how to create cloud native applications: put it into docker container(s) and run on kubernetes cluster, etc...
* security: setup https, ssl for secure communication, OAuth2 for authorization
* ...
  