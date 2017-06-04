# Restful API with Mongo DB
RESTful API with Python and Flask, and MongoDB

Hello!

I followed this Miquel Grinberg's awesome Flask tutorial, and decided to extend it with NoSQL database (Mongo DB) and to create comprehensive unit tests for the whole thing. 

Miquel's great tutorial can be found from here: https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask

Unit tests are bit slow, since all the tests were made with real authentication, using login details from DB. Ideally, this kind of tests would be mocked to be faster, and these database based tests should be run less frequently. Don't mind though, idea was to just figure out how to test such a thing. 
