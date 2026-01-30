
'''
Bugs Found During Testing   



Incorrect data type in schemas.pet for the name field
In schemas.py, the name property of the pet schema was defined as integer.
However, the API responses return name as a string value(e.g. "ranger", "snowball").
This mismatch caused JSON schema validation failures and required correcting the schema to use type: "string".

Inconsistent response shape from / pets/{id} endpoint
The / pets/1 endpoint can return a list of pet objects instead of a single pet object in some cases.
Tests and schemas expect a single object, so this inconsistent response structure can break validation and tests.
Test logic had to defensively handle both list and object responses.

Hard dependency on the local server being running
All tests rely on the local Flask server at http: // localhost: 5000.
If the server is not started before running tests, every test fails with a connection error(ConnectionRefusedError).
There is no built-in check or automatic startup for the server, which makes the test suite sensitive to environment/setup order.
'''