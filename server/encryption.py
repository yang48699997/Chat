import hashlib


def hash_password_fixed(password, salt="yu_yang_hao_shu_ai"):
    combined = password + salt
    hash_object = hashlib.sha256(combined.encode('utf-8'))
    return hash_object.hexdigest()


def check_password(password, hashed_password):
    return hash_password_fixed(password) == hash_password_fixed(hashed_password)

