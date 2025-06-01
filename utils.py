from cryptography.hazmat.primitives.asymmetric import dh

parameters = dh.generate_parameters(generator=2, key_size=2048)
param_nums = parameters.parameter_numbers()

P = param_nums.p
G = param_nums.g

key_size_bits = P.bit_length()
key_size_bytes = (key_size_bits + 7) // 8
print("P:", P)
print("G:", G)
print("P length:", key_size_bits, "bits")
