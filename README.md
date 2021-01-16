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
---

## Important Advices

### Documentation

To generate documentation simply run the following commands with the server on:
```
$ npm install -g @2fd/graphdoc # to install the generator
$ graphdoc -e http://localhost:5000/graphql -o ./doc/schema
```

## Routing

To process requests we decided to use a technology named __GraphQL__ using the __graphene__ package for python. With this we can perform fast query answers to this API returning only the data the user requests.

To run, simply run
```
python api.py
```

and access the graphql interface on http://localhost:5600/graphql .

### Available Querys

#### Sum of invoices
```
query {
    sum_invoices(nif: "...", ...)
}
```
- nif -> String, required;
- delta -> String, optional (default "D");
- window_start -> String, optional (default None);
- window_end -> String, optional (default None).

#### Invoices per category
```
query {
    n_invoices_category(nif: "...", ...)
}
```
- nif: String, required;
- delta: String, optional (default "M");
- is_count: Boolean, optional (default True);
- category: String, optional (default None);
- window_start -> String, optional (default None);
- window_end -> String, optional (default None).

#### Invoices per client
```
query {
    n_invoices_client(nif: "...", ...)
}
```
- nif: String, required;
- delta: String, optional (default "M");
- is_count: Boolean, optional (default True);
- client_nif: String, optional (default None);
- window_start -> String, optional (default None);
- window_end -> String, optional (default None).

#### Predict invoices
```
query {
    predict_future(nif: "...", ...)
}
```
- nif: String, required;
- time: Int, required;
- delta: String, optional (default "M");
- method: String, "simple" or "advanced" (default "simple").

#### Categorize invoices
```
query {
    categorize_invoices(overwrite: true, invoices: "...")
}
```
- invoices: JSONString, required.
- overwrite: Boolean, optional (default False).

Example for the __invoices__ field (must be converted to a string before sending):
```
{
    "list": [
        {
        "nif":"1234",
        "company_seller_name":"Razoes para Adultos",
        "total_value":130,
        "doc_emission_date": "2020-12-22"
        },
        ...
    ]
}
```
The model has an expiration date of __15 days__ before needing to be trained again on the whole data of the user. If this happens during a request, it might take between __5 to 15__ seconds to finish (depending on the machine). After trained, it is stored inside a local BD running on this docker service.

---

For more info head over to the more technical documentation [here](./doc/schema/index.html).
---
---

Delta explained
```
M -> monthly data
Q -> quarterly data
Y -> yearly data
2BQS -> biannual data
```

