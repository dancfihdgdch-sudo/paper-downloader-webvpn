# Paper Downloader via WebVPN

自动通过学校 WebVPN 下载学术论文的工具。

## 功能特性

✅ 通过 WebVPN 登录认证  
✅ 支持 DOI 论文查询  
✅ 自动下载 PDF  
✅ ���持 YIIGLE 医学数据库  
✅ 重试机制与错误处理  
✅ 环境变量配置  

## 安装

### 1. 克隆仓库

```bash
git clone https://github.com/dancfihdgdch-sudo/paper-downloader-webvpn.git
cd paper-downloader-webvpn
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置凭证

```bash
# 复制示例配置文件
cp .env.example .env

# 编辑 .env 文件，添加你的学号和密码
# WEBVPN_USERNAME=your_student_id
# WEBVPN_PASSWORD=your_password
```

**重要**: 不要将含有真实凭证的 `.env` 文件上传到 GitHub！

## 使用方法

### 方式 1: 交互式输入

```bash
python doi_downloader.py
```

然后输入 DOI：
```
Enter DOI (e.g., 10.3760/cma.j.cn121094-20241101-00500): 10.3760/cma.j.cn121094-20241101-00500
```

### 示例

```bash
$ python doi_downloader.py
============================================================
Paper Downloader via WebVPN
============================================================

Enter DOI (e.g., 10.3760/cma.j.cn121094-20241101-00500): 10.3760/cma.j.cn121094-20241101-00500
[*] Attempting to login to WebVPN...
[+] WebVPN login successful!
[*] Resolving DOI: 10.3760/cma.j.cn121094-20241101-00500
[+] DOI resolved to: https://zhldwszybzz.yiigle.com/m/CN121094202602/...
[*] Downloading paper from: https://zhldwszybzz.yiigle.com/...
[+] Paper downloaded successfully!
[+] Saved to: ./papers/paper_00500.pdf

============================================================
Done!
============================================================
```

## 配置说明

### .env 文件

```ini
# WebVPN 配置
WEBVPN_URL=https://webvpn.hebmu.edu.cn
WEBVPN_USERNAME=your_student_id          # 你的学号
WEBVPN_PASSWORD=your_password            # 你的密码

# 下载配置
DOWNLOAD_DIR=./papers                   # 论文保存目录
TIMEOUT=30                              # 请求超时时间（秒）
RETRY_TIMES=3                           # 下载重试次数
```

## 文件说明

| 文件 | 说明 |
|------|------|
| `doi_downloader.py` | 主下载脚本 |
| `config.py` | 配置管理 |
| `requirements.txt` | Python 依赖 |
| `.env.example` | 环境变量模板 |
| `README.md` | 使用文档 |

## 支持的数据库

- ✅ YIIGLE（中文医学数据库）
- ✅ DOI 直接解析
- 🔄 更多数据库支持开发中...

## 常见问题

### Q: 为什么登录失败？
A: 检查 `.env` 文件中的学号和密码是否正确。

### Q: 下载很慢怎么办？
A: 这可能是网络或服务器的问题。可以调整 `TIMEOUT` 和 `RETRY_TIMES` 参数。

### Q: 如何添加更多数据库支持？
A: 在 `DOIDownloader` 类中添加新方法，例如 `download_from_sciencedirect()`。

## 注意事项

⚠️ **请勿滥用**  
- 仅用于个人学习和研究
- 遵守学校 WebVPN 使用政策
- 尊重论文版权

⚠️ **安全建议**  
- 不要将 `.env` 文件上传到 GitHub
- 定期更改 WebVPN 密码
- 在公共计算机上使用前清除凭证

## 许可证

MIT License

## 贡献

欢迎提交 Issues 和 Pull Requests！

## 更新日志

### v0.1.0 (2026-06-01)
- ✨ 初始版本
- 支持 WebVPN 登录
- 支持 DOI 论文下载
- 支持 YIIGLE 数据库
