
import passwordmanager.database as database

def test_database():
    db = database.Database("tests/testdb")
    db.create_database("test_master")
    db.add_handle("test_handle", "test_password", "test_master")
    assert db.get_password("test_handle", "test_master") == "test_password", \
            "incorret password returned"

if __name__ == "__main__":
    test_database()
    print("test passed")

