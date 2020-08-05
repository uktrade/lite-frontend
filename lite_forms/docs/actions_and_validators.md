# Actions

Actions post data to the API, they they return the data back from the API plus the status code.

```
self.action = post_applications
```

```
def post_applications(request, json):
    data = post(request, APPLICATIONS_URL, json)
    return data.json(), data.status_code
```

# Validators

You may not always have an endpoint set up to handle validation of your form, for this reason it's possible to use a custom validator to do so.

```
self.action = validate_external_location_choice
```

```
def validate_external_location_choice(_request, _pk, json):
    if json.get("choice"):
        return json, HTTPStatus.OK

    return {"errors": {"choice": ["Select a choice"]}}, HTTPStatus.BAD_REQUEST
```
