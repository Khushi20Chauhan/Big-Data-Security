import random
import math
import sys

class RSACryptosystem:
    def __init__(self):
        self.public_key = None
        self.private_key = None
        self.last_encrypted = None
    
    def is_prime(self, n, k=5):
        """Miller-Rabin primality test."""
        if n <= 1:
            return False
        elif n <= 3:
            return True
        elif n % 2 == 0:
            return False
        
        d = n - 1
        s = 0
        while d % 2 == 0:
            d //= 2
            s += 1
        
        for _ in range(k):
            a = random.randint(2, n - 2)
            x = pow(a, d, n)
            if x == 1 or x == n - 1:
                continue
            for __ in range(s - 1):
                x = pow(x, 2, n)
                if x == n - 1:
                    break
            else:
                return False
        return True

    def generate_large_prime(self, bits=1024):
        """Generate a large prime number."""
        while True:
            num = random.getrandbits(bits)
            if num % 2 == 0:
                num += 1
            if self.is_prime(num):
                return num

    def extended_gcd(self, a, b):
        """Extended Euclidean algorithm."""
        if a == 0:
            return (b, 0, 1)
        else:
            g, y, x = self.extended_gcd(b % a, a)
            return (g, x - (b // a) * y, y)

    def modinv(self, a, m):
        """Modular inverse using extended Euclidean algorithm."""
        g, x, y = self.extended_gcd(a, m)
        if g != 1:
            raise ValueError("Modular inverse doesn't exist")
        return x % m

    def generate_keys(self, bits=2048):
        """Generate RSA public and private keys."""
        p = self.generate_large_prime(bits//2)
        q = self.generate_large_prime(bits//2)
        while p == q:
            q = self.generate_large_prime(bits//2)
        
        n = p * q
        phi = (p - 1) * (q - 1)
        
        e = 65537
        while math.gcd(e, phi) != 1:
            e = random.randint(2, phi - 1)
        
        d = self.modinv(e, phi)
        self.public_key = (n, e)
        self.private_key = (n, d)
        return self.public_key, self.private_key

    def encrypt(self, message):
        """Encrypt a message using the public key."""
        if not self.public_key:
            raise ValueError("Public key not generated")
        
        n, e = self.public_key
        msg_bytes = message.encode('utf-8')
        msg_int = int.from_bytes(msg_bytes, 'big')
        
        if msg_int >= n:
            max_length = (n.bit_length() // 8) - 1
            raise ValueError(f"Message too long (max {max_length} bytes)")
        
        ciphertext = pow(msg_int, e, n)
        self.last_encrypted = ciphertext
        return ciphertext

    def decrypt(self, ciphertext=None):
        """Decrypt a message using the private key."""
        if not self.private_key:
            raise ValueError("Private key not generated")
        
        if ciphertext is None:
            if self.last_encrypted is None:
                raise ValueError("No message to decrypt")
            ciphertext = self.last_encrypted
        
        n, d = self.private_key
        msg_int = pow(ciphertext, d, n)
        msg_bytes = msg_int.to_bytes((msg_int.bit_length() + 7) // 8, 'big')
        return msg_bytes.decode('utf-8')

def display_menu():
    """Display the main menu."""
    print("\n=== RSA Cryptosystem Simulator ===")
    print("1. Generate RSA Keys")
    print("2. Encrypt Message")
    print("3. Decrypt Last Message")
    print("4. Full Demo (Generate, Encrypt, Decrypt)")
    print("5. Exit")
    return input("Select an option (1-5): ").strip()

def main():
    rsa = RSACryptosystem()
    
    while True:
        try:
            choice = display_menu()
            
            if choice == '1':
                bits = input("Enter key size (1024, 2048, or 4096): ").strip()
                try:
                    bits = int(bits)
                    if bits not in [1024, 2048, 4096]:
                        raise ValueError
                except ValueError:
                    print("Invalid input. Using 2048 bits.")
                    bits = 2048
                
                print("\nGenerating keys... (This may take a moment)")
                pub, priv = rsa.generate_keys(bits)
                print("\nPublic Key (n, e):")
                print(pub)
                print("\nPrivate Key (n, d):")
                print(f"({priv[0]}, [REDACTED])")
            
            elif choice == '2':
                if not rsa.public_key:
                    print("Error: Generate keys first!")
                    continue
                
                message = input("\nEnter message to encrypt: ").strip()
                if not message:
                    print("Error: Message cannot be empty")
                    continue
                
                try:
                    ciphertext = rsa.encrypt(message)
                    print("\nEncryption Process:")
                    print(f"Original Message: {message}")
                    print(f"Encrypted (as number): {ciphertext}")
                except ValueError as e:
                    print(f"Error: {e}")
            
            elif choice == '3':
                if not rsa.private_key:
                    print("Error: Generate keys first!")
                    continue
                
                try:
                    decrypted = rsa.decrypt()
                    print("\nDecryption Process:")
                    print("Using stored ciphertext from last encryption")
                    print(f"Decrypted Message: {decrypted}")
                except ValueError as e:
                    print(f"Error: {e}")
            
            elif choice == '4':
                print("\nRunning Complete RSA Demo...")
                
                # Generate keys
                print("\n1. Key Generation:")
                pub, priv = rsa.generate_keys(2048)
                print(f"Public Key (n, e): {pub}")
                print(f"Private Key (n, d): ({priv[0]}, [REDACTED])")
                
                # Encrypt
                message = "This is a secret message!"
                print("\n2. Encryption:")
                print(f"Original Message: {message}")
                ciphertext = rsa.encrypt(message)
                print(f"Encrypted (as number): {ciphertext}")
                
                # Decrypt
                print("\n3. Decryption:")
                decrypted = rsa.decrypt()
                print(f"Decrypted Message: {decrypted}")
                
                # Verification
                print("\n4. Verification:")
                print("Success!" if decrypted == message else "Failure!")
            
            elif choice == '5':
                print("\nExiting program...")
                sys.exit(0)
            
            else:
                print("Invalid choice. Please enter 1-5.")
        
        except KeyboardInterrupt:
            print("\nOperation cancelled by user")
        except Exception as e:
            print(f"\nError: {e}")

if __name__ == "__main__":
    main()