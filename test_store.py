from jsonschema import validate
import pytest
import schemas
import api_helpers
from hamcrest import assert_that, contains_string, is_

'''
TODO: Finish this test by...
1) Creating a function to test the PATCH request /store/order/{order_id}
2) *Optional* Consider using @pytest.fixture to create unique test data for each run
2) *Optional* Consider creating an 'Order' model in schemas.py and validating it in the test
3) Validate the response codes and values
4) Validate the response message "Order and pet status updated successfully"
'''


@pytest.fixture
def new_order():
    # Setup: Create a new available pet to ensure one exists
    pet_id = 9000  # distinct ID for testing
    pet_data = {
        "id": pet_id,
        "name": "test_pet",
        "type": "dog",
        "status": "available"
    }
    # Try creating it, if it exists, that is fine (or we could use a random ID)
    # Using a random ID is safer for repeated runs without restart
    import random
    pet_id = random.randint(1000, 9999)
    pet_data['id'] = pet_id

    api_helpers.post_api_data("/pets/", pet_data)

    # Setup: Create a new order
    order_data = {
        "pet_id": pet_id
    }
    response = api_helpers.post_api_data("/store/order", order_data)
    assert response.status_code == 201

    order_json = response.json()
    validate(instance=order_json, schema=schemas.order)

    return order_json


def test_patch_order_by_id(new_order):
    order_id = new_order['id']
    test_endpoint = f"/store/order/{order_id}"

    # Update order status to 'sold'
    update_data = {
        "status": "sold"
    }

    response = api_helpers.patch_api_data(test_endpoint, update_data)
    assert response.status_code == 200
    assert response.json()[
        'message'] == "Order and pet status updated successfully"

    # Validation: Check if the pet status is now 'sold'
    pet_endpoint = f"/pets/{new_order['pet_id']}"
    pet_response = api_helpers.get_api_data(pet_endpoint)
    assert pet_response.json()['status'] == "sold"
