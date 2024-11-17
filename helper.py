checkpoint_path = "checkpoint.txt"


def write_checkpoint(checkpoint_id):
    print(f"0 | Writing | {checkpoint_id} -> {checkpoint_path}")
    with open(checkpoint_path, "w") as f:
        f.write(str(checkpoint_id))


def read_checkpoint():
    try:
        with open(checkpoint_path, "r") as f:
            checkpoint = int(f.read())
            return checkpoint
    except Exception:
        return 20580498  # This is the id for the kubernetes repository


def save_repo(url):
    with open("out.txt", "a+") as f:
        f.write("".join([url, "\n"]))


def audit_repo(url):
    with open("audit.txt", "a+") as f:
        f.write("".join([url, "\n"]))
