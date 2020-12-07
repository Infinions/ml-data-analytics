# ML-Work
Machine Learning work on various aspects of the project.

## Environment Setup
Create a python 3.8 environment and activate it
```
$ python3 -m venv /path/to/new/virtual environment
$ source /path/to/new/virtual environment/bin/activate
```

Install the requirements and you're good to go!
```
$ pip install -r requirements.txt
```

To exit the environment just run
```
$ deactivate
```

## Supported Routes

Delta explained
```
M -> monthly data
Q -> quarterly data
Y -> yearly data
2BQS -> biannual data
```

### Sum of invoices

GET /sum_invoices
```
delta -> type of division for the time
nif   -> nif from the company
```


### Number of invoices per category

GET /n_invoices_category
```
delta -> type of division for the time
nif   -> nif from the company
is_count -> true if desires to receive countings instead of raw summings
```

### Number of invoices per client

GET /n_invoices_client
```
delta -> type of division for the time
nif   -> nif from the company
is_count -> true if desires to receive countings instead of raw summings
```