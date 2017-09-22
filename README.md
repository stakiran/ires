# ires
画像リサイズを行うだけのシンプルなコマンド。Python2 と Pillow を使用。

<!-- toc -->
- [ires](#ires)
  - [Overview](#overview)
  - [Requirement](#requirement)
  - [License](#license)
  - [Author](#author)

## Overview
`python ires.py -r 50 sample.jpg sample.png` すると 50% リサイズした `sample_50.jpg` と `sample_50.png` を生成する。

簡単な画像リサイズが欲しかったのと、Pillow で簡単でリサイズできそうだったのでラッパー書いた。

## Requirement
以下環境で動作確認済

- Windows 7 (x86 Professional)
- Python 2.7
  - pillow 2.9.0

## License
[MIT License](LICENSE)

## Author
[stakiran](https://github.com/stakiran)
