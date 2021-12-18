# Smart Contract Crawler

A crawler that can automatically download smart contracts from Etherscan.

### How to use

1. Download an important address file from [Google Drive](https://drive.google.com/file/d/1XFmbn7RF-BwqOf0b5qkFvjOjnyYH4tgQ)
2. Place the file in this directory
3. Run `python try_vthread.py`

### Other configurations

#### Change the number of threads

```python
# just change the number in pool()
@vthread.pool(8)
```

#### Crawl Token

This crawler is based on the open API of Ethscan. Downloading smart contracts from Ethrescan is allowed only when the crawl token is provided (every account on Etherscan has a token). Therefore, if you find the token is expired, please registry an account on Etherscan and replace the token with yours in the `try_vthread.py`.