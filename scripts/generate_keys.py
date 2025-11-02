#!/usr/bin/env python3
"""
ΛΕΩΝΙΔΑΣ-AI PHALANX - Script de Generare Chei Criptografice
Generează cheile master de criptare pentru Spartan Guard și Thermopylae
"""

import os
import secrets
import hashlib
from datetime import datetime
from pathlib import Path


def generate_master_key(bits: int = 256) -> str:
    """
    Generează o cheie master criptografică.
    
    Args:
        bits: Dimensiunea cheii în biți (default: 256)
        
    Returns:
        Cheia în format hexadecimal
    """
    key_bytes = secrets.token_bytes(bits // 8)
    return key_bytes.hex()


def generate_salt(bytes_length: int = 32) -> str:
    """
    Generează un salt criptografic.
    
    Args:
        bytes_length: Dimensiunea salt-ului în bytes
        
    Returns:
        Salt-ul în format hexadecimal
    """
    salt = secrets.token_bytes(bytes_length)
    return salt.hex()


def generate_thermopylae_hash() -> str:
    """
    Generează un hash pentru verificarea protocolului Thermopylae.
    
    Returns:
        Hash-ul în format hexadecimal
    """
    random_data = secrets.token_bytes(64)
    hash_obj = hashlib.sha256(random_data)
    return hash_obj.hexdigest()


def save_keys_to_file(keys: dict, output_path: str):
    """
    Salvează cheile într-un fișier YAML.
    
    Args:
        keys: Dicționar cu cheile de salvat
        output_path: Calea către fișierul de output
    """
    import yaml
    
    # Adaugă metadata
    keys['generated_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    keys['version'] = "0.1.0"
    keys['warning'] = "KEEP THIS FILE SECRET - DO NOT COMMIT TO VERSION CONTROL"
    
    with open(output_path, 'w') as f:
        yaml.dump(keys, f, default_flow_style=False, sort_keys=False)
    
    # Setează permisiuni restrictive (doar owner poate citi/scrie)
    os.chmod(output_path, 0o600)


def main():
    """
    Funcția principală care generează toate cheile necesare.
    """
    print("🔑 ΛΕΩΝΙΔΑΣ-AI PHALANX - Cryptographic Key Generator")
    print("=" * 60)
    print()
    
    # Detectează directorul repository-ului
    script_dir = Path(__file__).parent
    repo_dir = script_dir.parent
    config_dir = repo_dir / "config"
    
    # Creează directorul config dacă nu există
    config_dir.mkdir(exist_ok=True)
    
    output_path = config_dir / "spartan_keys.yaml"
    
    # Verifică dacă fișierul există deja
    if output_path.exists():
        response = input("⚠️  spartan_keys.yaml already exists. Overwrite? (yes/no): ")
        if response.lower() not in ['yes', 'y']:
            print("❌ Key generation cancelled.")
            return
    
    print("🔐 Generating cryptographic keys...")
    print()
    
    # Generează cheile
    keys = {
        'MASTER_AES_KEY_HEX': generate_master_key(256),
        'KDF_SALT_HEX': generate_salt(32),
        'THERMOPYLAE_HASH': generate_thermopylae_hash()
    }
    
    # Afișează informații despre chei (fără a afișa cheile înseși!)
    print("✅ Generated keys:")
    print(f"   • Master AES-256 Key: {len(keys['MASTER_AES_KEY_HEX'])} characters")
    print(f"   • KDF Salt: {len(keys['KDF_SALT_HEX'])} characters")
    print(f"   • Thermopylae Hash: {len(keys['THERMOPYLAE_HASH'])} characters")
    print()
    
    # Salvează cheile
    print(f"💾 Saving keys to: {output_path}")
    save_keys_to_file(keys, str(output_path))
    
    print()
    print("=" * 60)
    print("✅ Cryptographic keys generated successfully!")
    print()
    print("⚠️  SECURITY WARNING:")
    print("   • These keys are CRITICAL for system security")
    print("   • NEVER commit spartan_keys.yaml to version control")
    print("   • NEVER share these keys with unauthorized persons")
    print("   • Store backups in a secure, encrypted location")
    print()
    print(f"   File permissions: {oct(os.stat(output_path).st_mode)[-3:]}")
    print(f"   File location: {output_path}")
    print()
    print("🛡️  ΜΟΛΩΝ ΛΑΒΕ (Molon Labe)")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Key generation interrupted by user.")
    except Exception as e:
        print(f"\n\n❌ Error during key generation: {e}")
        raise
