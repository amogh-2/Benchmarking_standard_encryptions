from cryptography.hazmat.primitives.asymmetric import dh

# Key Generation
parameters = dh.generate_parameters(generator=2, key_size=2048)
private_key = parameters.generate_private_key()
peer_public_key = parameters.generate_private_key().public_key()

# Key Exchange
shared_key = private_key.exchange(peer_public_key)
print(f"Shared Key: {shared_key}")
