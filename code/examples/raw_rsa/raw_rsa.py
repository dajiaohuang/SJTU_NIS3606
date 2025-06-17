import rsa
from typing import BinaryIO
import pickle

class RawRsa:
    """Raw RSA implementation for testing."""
    
    def __init__(self, n: int, e: int, d: int):
        """Initialize with RSA parameters."""
        self.n = n  # modulus
        self.e = e  # public exponent
        self.d = d  # private exponent
    
    @classmethod
    def new(cls, bits: int) -> 'RawRsa':
        """Generate new RSA key pair with given bit length."""
        pub_key, priv_key = rsa.newkeys(bits)
        return cls(pub_key.n, pub_key.e, priv_key.d)
    
    def raw_encrypt(self, message: int) -> int:
        """Raw RSA encryption: message^e mod n."""
        return pow(message, self.e, self.n)
    
    def raw_decrypt(self, cipher: int) -> int:
        """Raw RSA decryption: cipher^d mod n."""
        return pow(cipher, self.d, self.n)
    
    def save(self, filename: str) -> None:
        """Save RSA parameters to file."""
        with open(filename, 'wb') as f:
            pickle.dump((self.n, self.e, self.d), f)
    
    @classmethod
    def load(cls, filename: str) -> 'RawRsa':
        """Load RSA parameters from file."""
        with open(filename, 'rb') as f:
            n, e, d = pickle.load(f)
        return cls(n, e, d) 