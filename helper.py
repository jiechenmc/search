def write_checkpoint(checkpoint_id: int, worker: int):
    print(f"0 | Writing | {checkpoint_id} -> {worker}")
    with open(f"./tmp/checkpoint-{worker}.txt", "w") as f:
        f.write(str(checkpoint_id))


def read_checkpoint(worker: int):
    try:
        with open(f"./tmp/checkpoint-{worker}.txt", "r") as f:
            checkpoint = int(f.read())
            return checkpoint
    except Exception:
        return 43723161  # This is the id for the helm repository


def save_repo(url):
    with open("./data/out.txt", "a+") as f:
        f.write("".join([url, "\n"]))


def audit_repo(url):
    with open("./data/audit.txt", "a+") as f:
        f.write("".join([url, "\n"]))
