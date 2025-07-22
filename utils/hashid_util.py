from hashids import Hashids

hashids = Hashids(min_length=6, salt='HHtasty@hufa2030AA')  # change the salt to a strong, private value

def encode_id(real_id):
    return hashids.encode(real_id)

def decode_id(encoded_id):
    decoded = hashids.decode(encoded_id)
    return decoded[0] if decoded else None