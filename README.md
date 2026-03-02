# 文件加密工具 (File Encryptor)

一个使用AES-256算法的简单而安全的文件加密工具，用Python编写。

## 功能特点

- 🔒 使用AES-256-CBC加密算法，提供高强度的文件加密
- 🎯 支持加密和解密两种操作模式
- 📁 支持大文件加密，采用分块处理方式
- 🛡️ 自动生成随机盐值和初始化向量(IV)，提高安全性
- 📱 跨平台支持，可在Windows、macOS和Linux上运行
- 📊 简洁的命令行界面，易于使用

## 技术原理

- **加密算法**: AES-256-CBC (高级加密标准，256位密钥，CBC模式)
- **密钥派生**: PBKDF2-HMAC-SHA256，100,000次迭代
- **填充方式**: PKCS7
- **文件处理**: 64KB分块加密，支持大文件
- **安全设计**: 随机生成16字节盐值和16字节IV，存储在加密文件头部

## 安装和依赖

### 系统要求

- Python 3.6 或更高版本

### 依赖安装

```bash
pip install cryptography
```

### 下载项目

```bash
git clone <repository-url>
cd FileHash
```

## 使用方法

### 基本语法

```bash
python file_encryptor.py [mode] [input_file] [output_file] [-p password]
```

### 参数说明

- `mode`: 操作模式，可选值：`encrypt`（加密）或 `decrypt`（解密）
- `input_file`: 输入文件路径
- `output_file`: 输出文件路径
- `-p, --password`: 密码（可选，如果不提供，将提示输入）

### 使用示例

#### 1. 加密文件（交互式输入密码）

```bash
python file_encryptor.py encrypt myfile.txt myfile.enc
请输入密码: 
请确认密码: 
文件已加密: myfile.txt -> myfile.enc
```

#### 2. 加密文件（命令行提供密码）

```bash
python file_encryptor.py encrypt myfile.txt myfile.enc -p MySecurePassword123!
文件已加密: myfile.txt -> myfile.enc
```

#### 3. 解密文件（交互式输入密码）

```bash
python file_encryptor.py decrypt myfile.enc myfile_decrypted.txt
请输入密码: 
文件已解密: myfile.enc -> myfile_decrypted.txt
```

#### 4. 解密文件（命令行提供密码）

```bash
python file_encryptor.py decrypt myfile.enc myfile_decrypted.txt -p MySecurePassword123!
文件已解密: myfile.enc -> myfile_decrypted.txt
```

## 安全注意事项

1. **密码安全性**: 请使用强密码（至少12位，包含大小写字母、数字和特殊字符）
2. **密码管理**: 请妥善保管密码，丢失密码将无法恢复加密文件
3. **备份**: 在加密重要文件前，请务必备份原始文件
4. **文件完整性**: 加密过程会修改文件内容，请确保原始文件的完整性
5. **输出文件**: 加密/解密操作会覆盖同名输出文件，请谨慎操作

## 文件结构

```
FileHash/
├── file_encryptor.py   # 主程序文件
├── .gitignore          # Git忽略文件
└── README.md           # 项目说明文档
```

## 许可证

本项目采用MIT许可证 - 详见LICENSE文件

## 贡献

欢迎提交Issue和Pull Request！

## 联系方式

如有问题或建议，请通过以下方式联系：

- 提交Issue到项目仓库
- 发送邮件到：[your-email@example.com]

---

**安全提示**: 加密工具仅能提供一定程度的安全保护，无法保证100%的安全性。请根据实际需求评估使用场景。