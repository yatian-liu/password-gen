# password-gen

Generate random passwords. `password_gen.py` generates passwords with each character uniformly randomly chosen from a-z, A-Z, 0-9, and symbols `~!@#$%^&*()_+` (the symbols corresponding to 0-9 on a QWERTY keyboard). `password_gen_pinyin.py` generates xkcd-style passwords, using Pinyin of 2-character words in `现代汉语常用词表（草案）.txt`。

Example usage:

```bash
$ ./password_gen.py 5 12    # Generate 5 passwords, each containing 12 random characters
$ ./password_gen_pinyin.py 3 4  # Generate 3 passwords, each containing 4 Pinyin of random 2-character Chinese words
$ ./password_gen_pinyin.py 3 4 --pinyin-and-tone # Generate 3 passwords, each containing 4 Pinyin *with tones* of random 2-character Chinese words
```
