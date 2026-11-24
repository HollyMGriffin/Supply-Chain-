from passwords import hash_password, verify_password, validate_new_password


def test_hash_is_salted_and_verifies():
    first = hash_password("Secret123")
    second = hash_password("Secret123")

    assert first != second
    assert first.startswith("pbkdf2_sha256$")
    assert verify_password("Secret123", first)
    assert not verify_password("wrong-password", first)


def test_verify_rejects_malformed_hash():
    assert not verify_password("anything", "not-a-hash")
    assert not verify_password("anything", None)


def test_password_length_rule():
    assert validate_new_password("short") is not None
    assert validate_new_password("long-enough") is None
