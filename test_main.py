from fastapi.testclient import TestClient
import pytest
from main import app, Item

client = TestClient(app)


class TestItem:

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        # Add an item to the list
        item = Item(text="Test", is_done=False)
        response = client.post("/items/", json=item.model_dump())
        assert response.status_code == 200

        yield

        # Delete the item
        response = client.delete(f"/items/{0}")

    def test_mark_item_as_done(self):
        response = client.patch(f"/items/{0}/is_done")
        assert response.status_code == 200
        assert response.json()["is_done"] == True

    def test_update_item(self):
        updated_item = Item(text="Updated", is_done=True)
        response = client.put(f"/items/{0}", json=updated_item.model_dump())
        assert response.status_code == 200
        assert response.json() == updated_item.model_dump()

    def test_delete_item(self):
        response = client.delete(f"/items/{0}")
        assert response.status_code == 200
        assert response.json() == {"message": f"Item {0} has been deleted."}

    def test_get_item(self):
        response = client.get(f"/items/{0}")
        assert response.status_code == 200
        assert response.json() == {"text": "Test", "is_done": False}

    def test_list_items(self):
        item_second = Item(text="Test 2", is_done=True)
        response = client.post("/items/", json=item_second.model_dump())
        assert response.status_code == 200

        response = client.get("/items/")
        assert response.status_code == 200
        assert response.json() == [
            {"text": "Test", "is_done": False},
            {"text": "Test 2", "is_done": True},
        ]
