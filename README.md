# 悪魔城ドラキュラ 音楽館

悪魔城ドラキュラ（Castlevania）シリーズの楽曲を、物語の時系列順に作品ごとにまとめたファンサイトです。

- 作品ごとの曲一覧（YouTube Music へのリンク）とプレイリスト
- 各作品の主人公・あらすじ・Wikipedia へのリンク
- 年表と、主人公の相関図

## GitHub Pages で公開する

1. リポジトリの **Settings → Pages** を開く
2. **Source** を「Deploy from a branch」にし、公開したいブランチ（`main` など）と `/ (root)` を選んで保存
3. 数分後に `https://<ユーザー名>.github.io/castlevania/` で表示されます

ビルド工程は不要です（`index.html` と `assets/` をそのまま配信します）。

## 内容を編集する

| ファイル | 内容 |
| --- | --- |
| `data/tracks.json` | 作品ごとのプレイリスト ID と曲（曲名・動画 ID・時間） |
| `tools/build.py` | 作品の説明・年表・相関図の定義と、`index.html` の生成 |
| `assets/style.css` | デザイン |
| `assets/favicon.svg` ほか | favicon と、SNS 共有用の画像 `og-image.png`（`tools/og-image.html` を 1200×630 で撮影したもの） |

編集後に次を実行すると `index.html` が再生成されます（Python 3 のみ、追加ライブラリ不要）。

```bash
python3 tools/build.py
```

公開先の URL を変える場合は、`tools/build.py` 冒頭の `SITE_URL` も変更してください（SNS 共有用の画像は絶対 URL で指定しているため）。

## 注意

非公式のファンサイトです。「悪魔城ドラキュラ」「Castlevania」は株式会社コナミデジタルエンタテインメントの商標・著作物です。
音源は含まず、YouTube Music 上の公開プレイリスト・動画へリンクしています。
