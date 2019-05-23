# Koko Book Store API

This is an API for a simple book store. It allows customers to rent out books, return them and charges them appropriately.

More info on the API can be found in the [docs](http://35.196.160.21:8000/)

[![CircleCI](https://circleci.com/gh/dennynganga/koko_book_store/tree/master.svg?style=svg&circle-token=9ebe3998c371b29a3d007394566d9831a1033ada)](https://circleci.com/gh/dennynganga/koko_book_store/tree/master)

## Installation

-  Clone this repo. You might want to do this in a virtual environment (See [more on virtualenv](https://virtualenv.pypa.io/en/latest/))
```bash
git clone https://github.com/dennynganga/koko_book_store.git
```
- Once cloned, and virtual environment activated (if using one):
```bash
pip install -r requirements.txt
```
- Run server, and open http://127.0.0.1:8000 on your browser
```bash
python manage.py runserver
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Deployment Steps
-

## Scaling the service
 - ##### Data Layer
 For this test, a fairly simple database was used i.e SQLite. In order to be able to serve more requests efficiently in production, I'd switch to a more robust engine (preference to PostgreSQL)
 PostgreSQL supports query logging and this can be used to tell which queries are being run frequently or even which ones take long to execute. From analysing this info, we can decide which responses to **cache** (depending on business requirements) so as to decrease load on the database server.
 On the same note, I'd also bring in **Elastic Search** to provide a more scalable search. From our service, items that can be indexed include books, customers and rentals, so we can find them quicker.
 Also, as our database grows, we'd introduce a technique known as **sharding**. This is where the database is partitioned into smaller, faster parts.
 - ##### Session Storage
 Moving session storage to a faster, in-memory caching tool like redis or memcached, to avoid database hits while reading and writing session data.
 - ##### Running long computations offline
 Computations that take long to run should not be performed in the normal request-response cycle, so as to reduce page load times. In our case, an example would be sending a reminder email to a customer, or even generating a large CSV file that shows all active rentals. Such long-running tasks can be delegated to multiple workers. **Celery** (in combination with redis or rabbitmq) would come in handy in this.
 - ##### Hosting
 This involves using a load balancer that routes requests to two or more application servers. This way, increased load is well handled.