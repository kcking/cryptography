import time
from concurrent.futures import ThreadPoolExecutor

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def encrypt_chunk(chunk: bytes):
    cipher = Cipher(
        algorithms.AES(b"a" * 32),
        modes.CTR(b"b" * 16),
        backend=default_backend(),
    )
    encryptor = cipher.encryptor()
    encryptor.update(chunk) + encryptor.finalize()


def test(n: int, threads: int):
    ptxt = b"b" * n
    chunk_size = n // threads
    chunks = [ptxt[i * chunk_size : (i + 1) * chunk_size] for i in range(threads)]

    start = time.time()
    with ThreadPoolExecutor(max_workers=threads) as executor:
        list(executor.map(encrypt_chunk, chunks))
    end_time = time.time() - start

    print(f"{n / end_time / 1e9} GB/s")


if __name__ == "__main__":
    for i in [1, 2, 4, 8, 16, 32]:
        print(f"{i} threads")
        test(2 * 2**30, i)
