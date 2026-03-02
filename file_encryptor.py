#!/usr/bin/env python3
"""
文件加密工具
使用AES-256算法加密和解密文件
"""

import os
import sys
import argparse
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import base64


def generate_key(password: str, salt: bytes) -> bytes:
    """从密码生成AES密钥"""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,  # AES-256需要32字节密钥
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())


def encrypt_file(input_file: str, output_file: str, password: str) -> None:
    """加密文件"""
    # 生成随机盐
    salt = os.urandom(16)
    # 生成随机IV
    iv = os.urandom(16)
    # 从密码生成密钥
    key = generate_key(password, salt)
    
    # 创建密码器
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    # 创建填充器
    padder = padding.PKCS7(128).padder()
    
    with open(input_file, 'rb') as f_in:
        with open(output_file, 'wb') as f_out:
            # 写入盐和IV到输出文件开头
            f_out.write(salt)
            f_out.write(iv)
            
            # 分块读取和加密文件
            while True:
                chunk = f_in.read(64 * 1024)  # 64KB块
                if not chunk:
                    break
                
                # 填充数据
                padded_chunk = padder.update(chunk)
                # 加密数据
                encrypted_chunk = encryptor.update(padded_chunk)
                # 写入加密数据
                f_out.write(encrypted_chunk)
            
            # 处理最后一块
            final_padded = padder.finalize()
            final_encrypted = encryptor.update(final_padded) + encryptor.finalize()
            f_out.write(final_encrypted)
    
    print(f"文件已加密: {input_file} -> {output_file}")


def decrypt_file(input_file: str, output_file: str, password: str) -> None:
    """解密文件"""
    with open(input_file, 'rb') as f_in:
        # 读取盐和IV
        salt = f_in.read(16)
        iv = f_in.read(16)
        
        # 从密码生成密钥
        key = generate_key(password, salt)
        
        # 创建密码器
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        
        # 创建去填充器
        unpadder = padding.PKCS7(128).unpadder()
        
        with open(output_file, 'wb') as f_out:
            # 分块读取和解密文件
            while True:
                chunk = f_in.read(64 * 1024)  # 64KB块
                if not chunk:
                    break
                
                # 解密数据
                decrypted_chunk = decryptor.update(chunk)
                # 去填充数据
                unpadded_chunk = unpadder.update(decrypted_chunk)
                # 写入解密数据
                f_out.write(unpadded_chunk)
            
            # 处理最后一块
            final_decrypted = decryptor.finalize()
            final_unpadded = unpadder.update(final_decrypted) + unpadder.finalize()
            f_out.write(final_unpadded)
    
    print(f"文件已解密: {input_file} -> {output_file}")


def main() -> None:
    """主函数"""
    parser = argparse.ArgumentParser(description='文件加密工具')
    parser.add_argument('mode', choices=['encrypt', 'decrypt'], help='操作模式: encrypt或decrypt')
    parser.add_argument('input_file', help='输入文件路径')
    parser.add_argument('output_file', help='输出文件路径')
    parser.add_argument('-p', '--password', help='密码（如果不提供，将提示输入）')
    
    args = parser.parse_args()
    
    # 获取密码
    if args.password:
        password = args.password
    else:
        from getpass import getpass
        password = getpass('请输入密码: ')
        if args.mode == 'encrypt':
            confirm_password = getpass('请确认密码: ')
            if password != confirm_password:
                print('密码不一致！')
                sys.exit(1)
    
    # 检查输入文件是否存在
    if not os.path.exists(args.input_file):
        print(f'错误: 输入文件不存在: {args.input_file}')
        sys.exit(1)
    
    try:
        if args.mode == 'encrypt':
            encrypt_file(args.input_file, args.output_file, password)
        else:
            decrypt_file(args.input_file, args.output_file, password)
    except Exception as e:
        print(f'错误: {e}')
        sys.exit(1)


if __name__ == '__main__':
    main()
