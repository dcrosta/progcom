import bcrypt

_SALT_ROUNDS=12
def mangle(pw, salt=None):
    if not salt:
        salt = bcrypt.gensalt(rounds=_SALT_ROUNDS)
    else:
        salt = salt.encode('utf-8')
    return bcrypt.hashpw(pw.encode('utf-8'), salt)


if __name__ == "__main__":
    import sys
    if len(sys.argv) == 2:
        print(mangle(sys.argv[1]))
    else:
        print("Usage: python password.py YOUR_PASSWORD")
        sys.exit(1)
