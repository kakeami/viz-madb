# 環境構築

## 前提

事前に下記がインストールされていることが前提です．

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.jp/compose/toc.html)
- [Git](https://git-scm.com/)

ちなみに私の環境は：

- macOS Catalina Version 10.15.7
- Docker version 20.10.7, build f0df350
- docker-compose version 1.29.2, build 5becea4c
- git version 2.29.2

です．

## 手順

### GitHubからソースコードのクローン

[本サイトのGitHubリポジトリ](https://github.com/kakeami/viz-madb)からソースコード及びMADBのデータをダウンロードしてください．
例えば，

```sh
git clone --recursive https://github.com/kakeami/viz-madb.git
```

とシェルでコマンドを打てば，`viz-madb`ディレクトリが作成され，必要なデータが全てダウンロードされます．

`--recursive`オプションを付けることで，MADB Labのデータを格納する`madb`ディレクトリも含めてクローンしています．
今後の分析では`madb`ディレクトリがあることが前提となりますので，必ず`--recursive`オプションをつけるようご注意ください．

データサイズが大きいため，しばらく時間がかかります．

### Jupyter Labの起動

`viz-madb`ディレクトリに移動し，下記のコマンドでコンテナを立ち上げてください．

```
sudo docker-compose up -d
```

ブラウザから`localhost:9998`にアクセスすると，下図のようにパスワード入力画面が表示されます．

`madb`を入力してログインしましょう．

![passwd](figs/setup/passwd.png)

下図のようにビルドを求められる場合は，`Build`をクリックしてください．

![](figs/setup/build.png)

左のエクスプローラーから，`work` > `book`の順に選択し，解析用ディレクトリに移動してください．
ノートブック（`*.ipynb`）と本サイトの対応関係をいかに示します．

```sh
.
├── appendix
│   ├── preprocess.ipynb # 前処理用
│   └── setup.md
├── charts4amounts
│   ├── bars.ipynb # 棒グラフ
│   └── heatmap.ipynb # ヒートマップ
├── charts4assocs
│   ├── 2d.ipynb # 二次元ヒストグラム
│   ├── connected.ipynb # 折れ線グラフ（二変数）
│   ├── contours.ipynb # 等高線プロット
│   ├── correlo.ipynb # コレログラム
│   ├── line.ipynb # 折れ線グラフ
│   ├── scatter.ipynb # 散布図・バブルチャート
│   └── slope.ipynb # 並行座標プロット
├── charts4dists
│   ├── box.ipynb # 箱ひげ図
│   ├── density.ipynb # 密度プロット
│   ├── hist.ipynb # ヒストグラム
│   ├── ridgeline.ipynb # リッジラインプロット
│   ├── strip.ipynb # ストリップチャート
│   └── violin.ipynb # バイオリンプロット
├── charts4props
│   ├── bars.ipynb # 棒グラフ
│   ├── mosaic.ipynb # モザイクプロット
│   ├── parallel.ipynb # パラレルセットグラフ
│   ├── pie.ipynb # 円グラフ
│   ├── stacked_den.ipynb # 積上げ密度プロット
│   └── tree.ipynb # ツリーマップ
├── eda
│   └── eda.ipynb # そもそもどんなデータを扱うの？
```

:::{note}
なお，本ページは`setup.md`と対応しています．
:::

### 前処理の実行

`appendix` > `preprocess.ipynb`に移動し，前処理を実行しましょう．

![preprocess](figs/setup/preprocess.png)

上から順番に`Shift`+`Enter`を押していけば問題なく実行できるはずです．

最終的に`viz-madb/data/preprocess/out`に下記の二つの`.csv`ファイルが出力されていたら成功です．

```
viz-madb/data/preprocess/out
├── droped_episodes.csv
└── episodes.csv
```

![output](figs/setup/output.png)

### Jupyter Labのパスワードの変更

周知のパスワードを使い回すのは危険なので，必ず変更しましょう．

`viz-madb`ディレクトリ直下にある`docker-compose.yml`の最終行がパスワードに対応します．

```yaml
version: "3"
services:
  jupyterlab:
    build:
      context: .
    volumes:
      - "./:/home/jovyan/work"
    user: root
    ports:
      - "9998:8888"
    environment:
      NB_UID: 1000
      NB_GID: 1000
      GRANT_SUDO: "yes"
    command: start.sh jupyter lab --NotebookApp.password="sha1:82d29c037295:4e7d81a84b2750b65c72483df428016aa6984b5d"
```

最後の`"sha1:82d..."`を適宜変更しましょう．
例えば`YOUR_PASS`としたい場合は，pythonで

```python
>>> from notebook.auth import passwd
>>> passwd('YOUR_PASS', 'sha1')
'sha1:f0a65743e8bb:bf98a478a320c4fd1d8431679921f51a79a29850'
```

とすればトークンを生成できます（このままコピペしないでください！）
