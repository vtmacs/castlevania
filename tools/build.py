#!/usr/bin/env python3
"""index.html を生成する。  使い方: python3 tools/build.py

曲データは data/tracks.json、作品の説明・年表・相関図はこのファイル内で定義している。
"""
import json
from html import escape as e
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
TRACKS = json.loads((ROOT / "data" / "tracks.json").read_text(encoding="utf-8"))

# 公開先の URL。OGP 画像などは絶対 URL が必要なので、公開先を変えたらここも変える。
SITE_URL = "https://vtmacs.github.io/castlevania/"
SITE_TITLE = "悪魔城ドラキュラ 音楽館 | Castlevania Music Archive"
SITE_DESC = ("悪魔城ドラキュラ（Castlevania）シリーズの楽曲を、物語の時系列順に作品ごとにまとめたファンサイト。"
             "YouTube Music のプレイリスト、あらすじ、主人公の相関図つき。")

WIKI = "https://ja.wikipedia.org/wiki/"
YTM_PL = "https://music.youtube.com/playlist?list="
YTM_W = "https://music.youtube.com/watch?v="


def wiki(title):
    return WIKI + quote(title.replace(" ", "_"))


def wiki_url(g):
    return g.get("wiki_url") or wiki(g["wiki"])


# 物語の時系列順。side=True は公式年表で外伝扱いの作品。
GAMES = [
    dict(id="loi", year="1094年", title="キャッスルヴァニア", en="Castlevania: Lament of Innocence",
         platform="PlayStation 2 / 2003年", hero="レオン・ベルモンド", wiki="キャッスルヴァニア (PlayStation 2)",
         story="十字軍の時代。騎士レオンは、吸血鬼ヴァルターにさらわれた婚約者サラを救うため、爵位と剣を捨てて単身「永遠の夜」の森へ向かう。"
               "錬金術師リナルドから授かった鞭で城を攻略するが、すべては親友マティアスの仕組んだ計略だった。"
               "人を捨て吸血鬼となったマティアス（後のドラキュラ）に、レオンは一族が夜を狩り続けることを誓う。聖鞭ヴァンパイアキラーと宿命の始まりの物語。"),
    dict(id="cv3", year="1476年", title="悪魔城伝説", en="Castlevania III: Dracula's Curse",
         platform="ファミリーコンピュータ / 1989年", hero="ラルフ・C・ベルモンド", wiki="悪魔城伝説",
         story="15世紀のワラキア。ドラキュラ伯爵が魔物の軍勢を率いてヨーロッパを闇に沈めようとしていた。"
               "人ならぬ力ゆえに人々から恐れられ隠れ住んでいたベルモンド家のラルフが、教会の求めに応じて立ち上がる。"
               "海賊グラント、魔法使いサイファ、そしてドラキュラの息子アルカードのいずれかを仲間に、悪魔城を目指す。"),
    dict(id="cod", year="1479年", title="悪魔城ドラキュラ 闇の呪印", en="Castlevania: Curse of Darkness",
         platform="PlayStation 2 / 2005年", hero="ヘクター", wiki="悪魔城ドラキュラ 闇の呪印",
         story="ラルフがドラキュラを倒してから3年。伯爵が遺した呪いは今も大地を蝕んでいた。"
               "かつてドラキュラに仕えた悪魔精錬士ヘクターは、人として静かに暮らしていたが、愛するロザリーを魔女として処刑に追い込んだかつての同僚アイザックへの復讐のため、"
               "捨てたはずの悪魔精錬の力を再び手にする。旅の途中では伝説のハンター、ラルフとも刃を交える。"),
    dict(id="bc", year="1499年", title="Castlevania: Belmont's Curse", en="キャッスルヴァニア ベルモンドカース",
         platform="Nintendo Switch / PlayStation 5 / Xbox Series X|S / PC / 2026年", hero="ローズ・ベルモンド",
         wiki_url="https://en.wikipedia.org/wiki/Castlevania:_Belmont%27s_Curse", wiki_label="Wikipedia（英語版）",
         links=[("公式サイト", "https://www.konami.com/games/castlevania/belmonts_curse/jp/ja/")],
         story="『悪魔城伝説』から23年後の1499年。フランスの首都パリは、突如現れた魔物の群れに襲われていた。"
               "聖鞭ヴァンパイアキラーを持つドラキュラ殺しの英雄トレバー・ベルモンド（『悪魔城伝説』のラルフ）、その娘ローズは、"
               "災厄の元凶を突き止めるため街の探索と魔物の討伐を始め、やがてその裏にある闇の陰謀に巻き込まれていく。"
               "倒したボスを不思議なタロットカードに封じ、「アルカナ」として力を借りるのが特徴。デス、メデューサ、カーミラに加え、ジャンヌ・ダルクも立ちはだかる。"
               "KONAMI・Evil Empire・Motion Twin による探索型2Dアクションで、音楽は ASADI。"),
    dict(id="adv", year="1576年", title="ドラキュラ伝説", en="Castlevania: The Adventure",
         platform="ゲームボーイ / 1989年", hero="クリストファー・ベルモンド", wiki="ドラキュラ伝説",
         story="ラルフの戦いから100年。再び蘇ったドラキュラを討つため、ベルモンド家のクリストファーが悪魔城に挑む。"
               "激闘の末に伯爵は倒れたかに見えたが、霧に姿を変えて密かに生き延びていた。"),
    dict(id="br", year="1591年", title="ドラキュラ伝説II", en="Castlevania II: Belmont's Revenge",
         platform="ゲームボーイ / 1991年", hero="クリストファー・ベルモンド", wiki="ドラキュラ伝説II",
         story="前作から15年。成人の儀を迎えたクリストファーの息子ソレイユが、力を取り戻そうとするドラキュラに心を操られ、姿を消す。"
               "クリストファーは突如現れた4つの城を攻略し、息子を取り戻してドラキュラとの決着をつける。"),
    dict(id="cv1", year="1691年", title="悪魔城ドラキュラ", en="Castlevania",
         platform="ファミリーコンピュータ ディスクシステム / 1986年", hero="シモン・ベルモンド", wiki="悪魔城ドラキュラ",
         story="100年に一度、キリストの力が弱まる時に蘇るというドラキュラ。邪教徒の儀式によって伯爵が復活し、トランシルヴァニアは再び恐怖に包まれる。"
               "シモン・ベルモンドは父祖伝来の鞭を手に、ただ一人で悪魔城へ乗り込む。シリーズの原点。",
         extra=[("chron", "悪魔城年代記 悪魔城ドラキュラ（X68000版リメイクの公式サントラ）", "悪魔城ドラキュラ (X68000版)")]),
    dict(id="scv4", year="1691年", title="悪魔城ドラキュラ（スーパーファミコン版）", en="Super Castlevania IV",
         platform="スーパーファミコン / 1991年", hero="シモン・ベルモンド", wiki="悪魔城ドラキュラ (スーパーファミコン版)",
         story="初代『悪魔城ドラキュラ』と同じ、シモンによるドラキュラ討伐を新たに描き直した作品。"
               "8方向に振れる鞭と、重厚で幻想的なサウンドが特徴。「シモン・ベルモンドのテーマ」はここで生まれた。"),
    dict(id="sq", year="1698年", title="ドラキュラII 呪いの封印", en="Castlevania II: Simon's Quest",
         platform="ファミリーコンピュータ ディスクシステム / 1987年", hero="シモン・ベルモンド", wiki="ドラキュラII 呪いの封印",
         story="ドラキュラを倒して7年。シモンの体は、戦いの際に受けた呪いによって蝕まれていた。"
               "呪いを解く方法はただ一つ、各地の館に散らばったドラキュラの5つの遺骸を集め、悪魔城の跡で焼き払うこと。"
               "名曲「Bloody Tears（血の涙）」の初出作。"),
    dict(id="hod", year="1748年", title="キャッスルヴァニア 白夜の協奏曲", en="Castlevania: Harmony of Dissonance",
         platform="ゲームボーイアドバンス / 2002年", hero="ジュスト・ベルモンド", wiki="キャッスルヴァニア 白夜の協奏曲",
         story="シモンの戦いから50年。孫のジュストのもとに、修行の旅に出ていた親友マクシームが傷だらけで戻り、幼なじみのリディーがさらわれたと告げる。"
               "二人は霧の中に現れた謎の城へ向かう。城には表と裏の二つの姿があり、その成り立ちにはマクシームが集めたドラキュラの遺骸が関わっていた。"),
    dict(id="rob", year="1792年", title="悪魔城ドラキュラX 血の輪廻", en="Castlevania: Rondo of Blood",
         platform="PCエンジン SUPER CD-ROM² / 1993年", hero="リヒター・ベルモンド", wiki="悪魔城ドラキュラX 血の輪廻",
         story="暗黒神官シャフトの手でドラキュラが復活。伯爵はベルモンドの末裔リヒターをおびき寄せるため、恋人アネットや少女マリアたちをさらう。"
               "リヒターは彼女たちを救うため悪魔城へ。救出したマリアはもう一人の主人公として共に戦う。",
         note="曲は『悪魔城ドラキュラ Xクロニクル オリジナルサウンドトラック』に収録されたPCエンジン版音源。"),
    dict(id="sotn", year="1797年", title="悪魔城ドラキュラX 月下の夜想曲", en="Castlevania: Symphony of the Night",
         platform="PlayStation / 1997年", hero="アルカード", wiki="悪魔城ドラキュラX 月下の夜想曲",
         story="ドラキュラを倒したリヒターが、ある満月の夜に忽然と姿を消す。時を同じくして、100年に一度しか現れないはずの悪魔城が再び出現。"
               "自らの血を呪い眠りについていたドラキュラの息子アルカードが目覚め、城へ向かう。"
               "リヒターを捜すマリアと出会い、操られた彼を救い出したアルカードは、逆さ城の最奥で父と対峙する。"),
    dict(id="ooe", year="19世紀", title="悪魔城ドラキュラ 奪われた刻印", en="Castlevania: Order of Ecclesia",
         platform="ニンテンドーDS / 2008年", hero="シャノア", wiki="悪魔城ドラキュラ 奪われた刻印",
         story="ベルモンド一族が表舞台から姿を消した時代。ドラキュラに対抗する術を研究する組織の一つ「エクレシア」のシャノアは、"
               "究極の印術「ドミナス」を宿す儀式の最中に兄弟子アルバスにそれを奪われ、記憶と感情を失ってしまう。"
               "アルバスを追う旅の果てに、彼女は組織の長バーロウの真の目的を知る。"),
    dict(id="cotm", year="1830年", title="悪魔城ドラキュラ Circle of the Moon", en="Castlevania: Circle of the Moon",
         platform="ゲームボーイアドバンス / 2001年", hero="ネイサン・グレーブズ", wiki="悪魔城ドラキュラ サークル オブ ザ ムーン", side=True,
         story="オーストリアの古城で、ドラキュラの信奉者カーミラが伯爵復活の儀式を執り行う。"
               "阻止に駆けつけたヴァンパイアハンターのモーリス、その息子ヒュー、弟子のネイサンだったが、師は捕らえられ、二人は城の地下へ落とされてしまう。"
               "ネイサンは師を救うため、ライバル心を燃やすヒューとぶつかりながら城を登る。"),
    dict(id="cv64", year="1852年", title="悪魔城ドラキュラ黙示録", en="Castlevania (Nintendo 64)",
         platform="NINTENDO64 / 1999年", hero="ラインハルト・シュナイダー / キャリー・ヴェルナンデス", wiki="悪魔城ドラキュラ黙示録", side=True,
         story="19世紀半ば、ドラキュラ復活の兆しがトランシルヴァニアを覆う。ベルモンドの血を引く青年ラインハルトと、"
               "ヴェルナンデスの力を受け継ぐ少女キャリーが、それぞれの理由で悪魔城へ向かう。シリーズ初の3Dアクション。"
               "8年前（1844年）を描く前日譚『黙示録外伝』では獣人コーネルが主人公となる。"),
    dict(id="bl", year="1917年", title="バンパイアキラー", en="Castlevania: Bloodlines",
         platform="メガドライブ / 1994年", hero="ジョニー・モリス / エリック・リカード", wiki="バンパイアキラー",
         story="第一次世界大戦のさなか、ドラキュラの姪エリザベート・バートリーが伯爵の完全復活を目論む。"
               "鞭を受け継いだモリス家のジョニーと、槍の使い手である親友エリックが、ヨーロッパ各地を巡ってその野望に立ち向かう。"
               "ジョニーは小説『吸血鬼ドラキュラ』のキンシー・モリスの息子という設定。"),
    dict(id="por", year="1944年", title="悪魔城ドラキュラ ギャラリー オブ ラビリンス", en="Castlevania: Portrait of Ruin",
         platform="ニンテンドーDS / 2006年", hero="ジョナサン・モリス / シャーロット・オーリン", wiki="悪魔城ドラキュラ ギャラリー オブ ラビリンス",
         story="第二次世界大戦で失われた無数の魂の嘆きが、悪魔城を呼び覚ます。城を支配するのは吸血鬼の画家ブローネル。"
               "ジョニーの息子ジョナサンと、幼なじみの魔法使いシャーロットは、城内に飾られた絵画の中の世界を巡りながら城主を追う。"
               "ジョナサンは父が語らなかった鞭の真の力と、その代償に向き合うことになる。",
         note="表には実際のゲーム内で流れる「ゲーム用アレンジ曲」版を掲載。"),
    dict(id="aos", year="2035年", title="キャッスルヴァニア 暁月の円舞曲", en="Castlevania: Aria of Sorrow",
         platform="ゲームボーイアドバンス / 2003年", hero="来須 蒼真", wiki="キャッスルヴァニア 〜暁月の円舞曲〜",
         story="1999年、ドラキュラはユリウス・ベルモンドたちによって完全に滅ぼされ、悪魔城は日食の中に封印された。"
               "それから36年後の皆既日食の日。白馬神社を訪れた高校生の蒼真と幼なじみの弥那は、日食の中の悪魔城へ引き込まれる。"
               "倒した魔物の魂を支配する力に目覚めた蒼真は、やがて自分こそがドラキュラの生まれ変わりであることを知る。"),
    dict(id="dos", year="2036年", title="悪魔城ドラキュラ 蒼月の十字架", en="Castlevania: Dawn of Sorrow",
         platform="ニンテンドーDS / 2005年", hero="来須 蒼真", wiki="悪魔城ドラキュラ 蒼月の十字架",
         story="前作から1年。魔王の不在を憂い、新たな魔王を生み出そうとする教団の教主セリア・フォルトゥナが蒼真の前に現れる。"
               "魔王候補たちとの戦いに巻き込まれた蒼真は、ユリウス、ヨーコ、有角らと共に教団の城へ乗り込み、自らの内に眠る闇と再び向き合う。"),
]

# 正史とは別の世界を描くリブート三部作（物語順）
LOS = [
    dict(id="los1", year="1047年", title="キャッスルヴァニア ロード オブ シャドウ", en="Castlevania: Lords of Shadow",
         platform="PlayStation 3 / Xbox 360 / 2010年", hero="ガブリエル・ベルモンド", wiki="キャッスルヴァニア ロード オブ シャドウ",
         story="天と地のつながりが断たれ、魔物がはびこる11世紀のヨーロッパ。「光の兄弟団」の騎士ガブリエルは、何者かに殺された妻マリーを蘇らせる望みを胸に、"
               "世界を覆う闇の源である三人の「影の王（ロード オブ シャドウ）」を倒す旅に出る。"
               "死者をも蘇らせるという「神の仮面」を追う戦いの果てに、彼は残酷な真実を知る。後日談で彼は吸血鬼となり、自らをドラキュラと名乗る。"),
    dict(id="mof", year="11〜12世紀", title="キャッスルヴァニア ロード オブ シャドウ 宿命の魔鏡", en="Castlevania: Lords of Shadow – Mirror of Fate",
         platform="ニンテンドー3DS / 2013年", hero="シモン・ベルモンド / アルカード / トレバー・ベルモンド", wiki="キャッスルヴァニア ロード オブ シャドウ 宿命の魔鏡",
         story="前作と『2』の間をつなぐ、ベルモンド三代の物語。ガブリエルの息子トレバーは、魔王ドラキュラとなった父を討つため城へ向かうが敗れ、やがてアルカードとして蘇る。"
               "数十年後、両親を奪われ復讐を誓うトレバーの息子シモンが城に乗り込み、正体を明かさぬアルカードと共にドラキュラへ挑む。"
               "三人の章を時間をさかのぼる順に遊ぶことで、一族の宿命の全体像が明らかになる。"),
    dict(id="los2", year="現代", title="悪魔城ドラキュラ ロード オブ シャドウ2", en="Castlevania: Lords of Shadow 2",
         platform="PlayStation 3 / Xbox 360 / 2014年", hero="ドラキュラ（ガブリエル・ベルモンド）", wiki="悪魔城ドラキュラ ロード オブ シャドウ2",
         story="長い眠りから目覚めたドラキュラは、力を失い衰えた姿で現代の大都市にいた。"
               "かつての宿敵ゾベックは、復活が迫るサタンを阻止すれば、望み続けた「不死からの解放」を与えると持ちかける。"
               "現代の街と記憶の中の城を行き来しながら力を取り戻すドラキュラ。その裏では、息子アルカードと交わした遠大な計画が動いていた。"),
]

# Netflix のアニメシリーズ
ANIME = [
    dict(id="anime1", year="15世紀", title="悪魔城ドラキュラ -キャッスルヴァニア-", en="Castlevania (Netflix)",
         platform="Netflix / 2017〜2021年（全4シーズン・32話）", when="配信",
         hero="トレバー・ベルモンド / サイファ・ベルナデス / アルカード", wiki="悪魔城ドラキュラ -キャッスルヴァニア-",
         story="『悪魔城伝説』を原案にしたアニメシリーズ。医術を学ぶ人間の女性リサを愛したドラキュラは、彼女が魔女として火刑に処されたことで人類への復讐を誓い、"
               "ワラキアに魔物の軍勢を解き放つ。教会に追放され落ちぶれていたベルモンド家最後の生き残りトレバーは、魔法を操る「語り部」のサイファ、"
               "そして父を止めようとするドラキュラの息子アルカードと手を組む。"
               "後半のシーズンでは『闇の呪印』のヘクターやアイザック、カーミラたちの物語も描かれる。音楽はトレバー・モリス。",
         note="プレイリストはシーズン1のサウンドトラックです。"),
    dict(id="noc", year="1792年", title="悪魔城ドラキュラ -キャッスルヴァニア-: 月夜のノクターン", en="Castlevania: Nocturne",
         platform="Netflix / 2023〜2025年（全2シーズン・16話）", when="配信",
         hero="リヒター・ベルモンド / マリア・ラーネッド / アネット", wiki="悪魔城ドラキュラ -キャッスルヴァニア-: 月夜のノクターン",
         story="前シリーズから約300年後、フランス革命のさなかを舞台にした続編。『血の輪廻』と『月下の夜想曲』を原案とする。"
               "幼い頃に目の前で母を吸血鬼に殺されたリヒター・ベルモンドは、革命を志すマリア、カリブから海を渡ってきたアネットたちと共に、"
               "貴族と結んだ吸血鬼たち、そして太陽を呑み込むという「吸血鬼の救世主」エルジェーベト・バートリに立ち向かう。"
               "主題曲には『血の輪廻』の「乾坤の血族（Divine Bloodlines）」が使われている。音楽はトレバー・モリスとトレイ・トイ。",
         note="プレイリストはシーズン1のアルバムです。シーズン2はアルバム単位のプレイリストが見つからなかったため、曲ごとのリンクのみ掲載しています。"),
]

# シリーズを代表する2曲の歴代バージョン集
FAVS = [
    dict(id="fav_bt", title="血の涙", en="Bloody Tears", first="初出：ドラキュラII 呪いの封印（1987年）",
         story="『ドラキュラII 呪いの封印』で昼のフィールドに流れる曲として生まれ、以後ほとんどの作品でアレンジされ続けているシリーズの代名詞。"
               "パイプオルガン風の前奏から疾走するメロディへ移る構成は、ファミコン音源から最新作のオーケストラまで形を変えて受け継がれている。"
               "ディスクシステム版の原曲から、スーパーファミコン版、血の輪廻、蒼月の十字架、ジャッジメント、Dead Cells コラボ、最新作 Belmont's Curse までを年代順に並べた。",
         note="ファンが年代順にまとめたプレイリストに基づく一覧です（夜の曲「Monster Dance」は除外）。最後の Belmont's Curse 版はプレイリストに無いため個別リンクで追加しています。"),
    dict(id="fav_vk", title="Vampire Killer", en="ヴァンパイアキラー", first="初出：悪魔城ドラキュラ（1986年）",
         story="初代『悪魔城ドラキュラ』のステージ1で流れる、シリーズ最初の一曲。聖鞭と同じ名を持ち、「血の涙」「Beginning」と並んでシリーズ三大名曲に数えられる。"
               "悪魔城伝説の「Déjà Vu」、白夜の協奏曲の「VK2K2」のように名前を変えて登場することも多い。"
               "ファミコン版・MSX2版の原曲から、X68000版、血の輪廻、Circle of the Moon、ジャッジメント、スマブラ、Dead Cells コラボまでを年代順に並べた。",
         note="ファンが年代順にまとめたプレイリストに基づく一覧です。"),
]

# 時系列の外にあるクロスオーバー作品（プレイリストのみ紹介）
BONUS = [
    ("悪魔城ドラキュラ Harmony of Despair ORIGINAL SOUNDTRACK SELECTION", "歴代主人公が集う協力アクションのサントラ", "PLGB_aEXQbubuEC8lIpV0T9S2GHPaN_bAg"),
    ("悪魔城ドラキュラ ジャッジメント オリジナルサウンドトラック", "歴代キャラクターが戦う対戦アクション。名曲のアレンジが多数", "PL_pS9cejkQH1eYHGmYL3tF5sup2-mydA_"),
    ("悪魔城ドラキュラ Xクロニクル オリジナルサウンドトラック", "『血の輪廻』のPSPリメイク版。リメイク音源とアレンジを収録", "PLq5sPB7Px6yH7RYhGCIJEXfVjZtCcp3_r"),
]


# ---------------------------------------------------------------- 相関図 (SVG)
def diagram():
    W, NW, NH, RH, TOP = 1060, 250, 54, 100, 70
    X = dict(L=175, C=530, R=885)
    out = []

    def y(r):
        return TOP + r * RH

    def node(col, r, name, sub, cls):
        cx, cy = X[col], y(r)
        out.append(f'<g class="n {cls}"><rect x="{cx-NW/2}" y="{cy-NH/2}" width="{NW}" height="{NH}" rx="8"/>'
                   f'<text class="nm" x="{cx}" y="{cy-4}">{e(name)}</text>'
                   f'<text class="sb" x="{cx}" y="{cy+15}">{e(sub)}</text></g>')

    def label(x, yy, text):
        w = len(text) * 12.5 + 14
        out.append(f'<g class="lb"><rect x="{x-w/2}" y="{yy-10}" width="{w}" height="20" rx="10"/>'
                   f'<text x="{x}" y="{yy+4}">{e(text)}</text></g>')

    def vert(col, r1, r2, text, cls="e", at=None):
        x = X[col]
        out.append(f'<line class="{cls}" x1="{x}" y1="{y(r1)+NH/2}" x2="{x}" y2="{y(r2)-NH/2}"/>')
        if text:
            label(x, at if at is not None else (y(r1) + y(r2)) / 2, text)

    def horiz(c1, c2, r, text, cls="e"):
        x1, x2 = X[c1] + NW / 2, X[c2] - NW / 2
        out.append(f'<line class="{cls}" x1="{x1}" y1="{y(r)}" x2="{x2}" y2="{y(r)}"/>')
        label((x1 + x2) / 2, y(r), text)

    def diag(c1, r1, c2, r2, text, cls="e"):
        x1 = X[c1] + (NW / 2 if X[c2] > X[c1] else -NW / 2)
        x2 = X[c2] + (-NW / 2 if X[c2] > X[c1] else NW / 2)
        out.append(f'<line class="{cls}" x1="{x1}" y1="{y(r1)}" x2="{x2}" y2="{y(r2)}"/>')
        label((x1 + x2) / 2, (y(r1) + y(r2)) / 2, text)

    rows = ["1094年", "1476年", "1479–99年", "1576–91年", "1691–98年", "1748年", "1792年", "1797年",
            "19世紀", "1917年", "1944年", "1999年", "2035–36年"]
    H = y(len(rows) - 1) + 150
    for i, t in enumerate(rows):
        if i % 2 == 0:
            out.append(f'<rect class="band" x="0" y="{y(i)-RH/2}" width="{W}" height="{RH}"/>')
        out.append(f'<text class="yr" x="14" y="{y(i)-RH/2+18}">{t}</text>')
    for col, t, cls in (("L", "闇の血統", "dark"), ("C", "ヴァンパイアキラーの継承者", "bel"), ("R", "仲間・協力者", "ally")):
        out.append(f'<text class="col {cls}" x="{X[col]}" y="16">{t}</text>')

    # 線を先に描いてからノードを重ねる
    vert("C", 0, 1, "子孫")
    vert("C", 1, 2, "父娘")
    vert("C", 2, 3, "子孫")
    vert("C", 3, 4, "子孫")
    vert("C", 4, 5, "孫")
    vert("C", 5, 6, "子孫")
    vert("C", 6, 8, "", "e")
    vert("C", 8, 9, "鞭を託す", "e dash")
    vert("C", 9, 10, "父子")
    vert("C", 10, 11, "鞭を返還", "e dash")
    vert("C", 11, 12, "見極め、のち共闘", "e dash")
    vert("L", 0, 1, "父子")
    vert("L", 1, 7, "同一人物（長い眠り）", "e dash", at=y(4))
    vert("L", 7, 12, "同一人物（正体を隠す）", "e dash", at=y(10))
    horiz("L", "C", 0, "親友 → 宿敵", "e foe")
    horiz("L", "C", 1, "共闘")
    horiz("C", "R", 1, "共闘 → 結婚")
    hx, hy, hx2 = X["C"] + 105, y(1) + NH / 2 + 14, X["R"] - NW / 2 - 28  # ラルフからヘクターへの折れ線
    out.append(f'<path class="e" fill="none" d="M{hx} {y(1)+NH/2} V{hy} H{hx2} V{y(2)} H{X["R"]-NW/2}"/>')
    label((hx + hx2) / 2 + 10, hy, "対決 → 共闘")
    horiz("C", "R", 3, "父子")
    horiz("C", "R", 5, "親友")
    horiz("C", "R", 6, "遠縁の義妹")
    diag("L", 7, "C", 6, "操られた彼を救う")
    horiz("C", "R", 9, "親友")
    horiz("C", "R", 10, "幼なじみ")
    horiz("L", "C", 12, "導き見守る")
    horiz("C", "R", 12, "協力")

    node("L", 0, "マティアス → ドラキュラ", "神を呪い吸血鬼となった魔王", "dark")
    node("C", 0, "レオン・ベルモンド", "一族の祖／キャッスルヴァニア", "bel")
    node("L", 1, "アルカード", "ドラキュラの息子／悪魔城伝説", "dark")
    node("C", 1, "ラルフ・C・ベルモンド", "悪魔城伝説／別名トレバー", "bel")
    node("R", 1, "サイファ・ヴェルナンデス", "魔法使い。グラントも仲間に", "ally")
    node("C", 2, "ローズ・ベルモンド", "トレバー（ラルフ）の娘／Belmont's Curse", "bel")
    node("R", 2, "ヘクター", "元ドラキュラ配下／闇の呪印", "hero")
    node("C", 3, "クリストファー・ベルモンド", "ドラキュラ伝説 I・II", "bel")
    node("R", 3, "ソレイユ・ベルモンド", "操られた息子", "ally")
    node("C", 4, "シモン・ベルモンド", "悪魔城ドラキュラ／ドラキュラII", "bel")
    node("C", 5, "ジュスト・ベルモンド", "白夜の協奏曲", "bel")
    node("R", 5, "マクシーム・キシン", "ジュストの親友でありライバル", "ally")
    node("C", 6, "リヒター・ベルモンド", "血の輪廻", "bel")
    node("R", 6, "マリア・ラーネッド", "血の輪廻／月下の夜想曲", "ally")
    node("L", 7, "アルカード", "月下の夜想曲の主人公", "hero")
    node("C", 8, "ベルモンド一族、姿を消す", "鞭はモリス家へ", "ghost")
    node("R", 8, "シャノア", "組織エクレシア／奪われた刻印", "hero")
    node("C", 9, "ジョニー・モリス", "バンパイアキラー", "mor")
    node("R", 9, "エリック・リカード", "槍の使い手", "ally")
    node("C", 10, "ジョナサン・モリス", "ギャラリー オブ ラビリンス", "mor")
    node("R", 10, "シャーロット・オーリン", "ヴェルナンデスの血を引く魔法使い", "ally")
    node("C", 11, "ユリウス・ベルモンド", "ドラキュラを完全に滅ぼす", "bel")
    node("L", 12, "有角 幻也（アルカード）", "正体を隠し蒼真を導く", "dark")
    node("C", 12, "来須 蒼真", "ドラキュラの生まれ変わり／暁月・蒼月", "hero")
    node("R", 12, "ヨーコ・ヴェルナンデス", "教会に属する魔法使い", "ally")

    by = y(12) + 62
    out.append(f'<g class="n ghost"><rect x="40" y="{by}" width="{W-80}" height="62" rx="8"/>'
               f'<text class="nm" x="{W/2}" y="{by+25}">外伝（公式年表の外）</text>'
               f'<text class="sb" x="{W/2}" y="{by+46}">1830年 ネイサン・グレーブズ（Circle of the Moon）　／　'
               f'1844年 コーネル・1852年 ラインハルト・シュナイダー、キャリー・ヴェルナンデス（黙示録）</text></g>')
    return (f'<svg viewBox="0 0 {W} {H}" role="img" aria-labelledby="dg-t" xmlns="http://www.w3.org/2000/svg">'
            f'<title id="dg-t">悪魔城ドラキュラシリーズ 主人公の相関図</title>' + "".join(out) + "</svg>")


def los_diagram():
    W, H, NW, NH = 1060, 330, 250, 54
    out = []

    def node(cx, cy, name, sub, cls):
        out.append(f'<g class="n {cls}"><rect x="{cx-NW/2}" y="{cy-NH/2}" width="{NW}" height="{NH}" rx="8"/>'
                   f'<text class="nm" x="{cx}" y="{cy-4}">{e(name)}</text>'
                   f'<text class="sb" x="{cx}" y="{cy+15}">{e(sub)}</text></g>')

    def edge(x1, y1, x2, y2, text, cls="e"):
        out.append(f'<line class="{cls}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/>')
        w = len(text) * 12.5 + 14
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        out.append(f'<g class="lb"><rect x="{mx-w/2}" y="{my-10}" width="{w}" height="20" rx="10"/>'
                   f'<text x="{mx}" y="{my+4}">{e(text)}</text></g>')

    L, C, R = 175, 530, 885
    edge(L + NW / 2, 60, C - NW / 2, 60, "宿敵 → 取引", "e foe")
    edge(C + NW / 2, 60, R - NW / 2, 60, "夫婦")
    edge(C, 60 + NH / 2, C, 165 - NH / 2, "父子")
    edge(C + NW / 2, 165, R - NW / 2, 165, "夫婦")
    edge(C, 165 + NH / 2, C, 270 - NH / 2, "父子")
    edge(L + NW / 2, 165, C - NW / 2, 165, "同一人物", "e dash")
    edge(L + NW / 2, 165 + 20, C - NW / 2, 270, "正体を隠して共闘")
    node(L, 60, "ゾベック", "影の王の一人。すべての黒幕", "dark")
    node(C, 60, "ガブリエル・ベルモンド", "のちのドラキュラ／LoS・LoS2", "hero")
    node(R, 60, "マリー・ベルモンド", "殺された妻。夫を導く", "ally")
    node(L, 165, "アルカード", "蘇ったトレバー／宿命の魔鏡・LoS2", "dark")
    node(C, 165, "トレバー・ベルモンド", "父を知らずに育つ／宿命の魔鏡", "bel")
    node(R, 165, "サイファ・ベルモンド", "トレバーの妻", "ally")
    node(C, 270, "シモン・ベルモンド", "両親の仇を追う／宿命の魔鏡", "bel")
    return (f'<svg viewBox="0 0 {W} {H}" role="img" aria-labelledby="ldg-t" xmlns="http://www.w3.org/2000/svg">'
            f'<title id="ldg-t">Lords of Shadow シリーズの相関図</title>' + "".join(out) + "</svg>")


# ---------------------------------------------------------------- HTML
def track_table(key, artist=False):
    d = TRACKS[key]
    pid = d["playlistId"]
    rows = ""
    for i, t in enumerate(d["tracks"], 1):
        if t.get("group"):
            rows += f'<tr class="grp"><th colspan="3" scope="colgroup">{e(t["group"])}</th></tr>'
        href = YTM_W + t["videoId"] + ("" if t.get("noList") else "&amp;list=" + pid)
        who = f'<td class="who">{e(t["artist"])}</td>' if artist else ""
        rows += (f'<tr><td class="num">{i}</td>'
                 f'<td><a href="{href}" target="_blank" rel="noopener">{e(t["title"])}</a></td>{who}'
                 f'<td class="dur">{e(t["duration"])}</td></tr>')
    who_h = '<th class="who">アーティスト／投稿者</th>' if artist else ""
    return (f'<div class="tw"><table><thead><tr><th class="num">#</th><th>曲名（クリックで YouTube Music を開く）</th>{who_h}'
            f'<th class="dur">時間</th></tr></thead><tbody>{rows}</tbody></table></div>')


def game_card(g):
    d = TRACKS[g["id"]]
    badge = ('<span class="badge off">公式音源</span>' if d["official"]
             else '<span class="badge com">ファン作成プレイリスト</span>')
    side = '<span class="badge side">外伝</span>' if g.get("side") else ""
    extra = "".join(
        f'<a class="btn ghost" href="{YTM_PL}{TRACKS[k]["playlistId"]}" target="_blank" rel="noopener">▶ {e(label)}</a>'
        for k, label, _ in g.get("extra", []))
    note = f'<p class="note">※ {e(g["note"])}</p>' if g.get("note") else ""
    more = "".join(f'<a class="btn ghost" href="{e(url)}" target="_blank" rel="noopener">{e(label)}</a>'
                   for label, url in g.get("links", []))
    return f'''
<article class="game" id="{g["id"]}">
  <header>
    <div class="year">{e(g["year"])}</div>
    <div>
      <h3>{e(g["title"])} {side}</h3>
      <p class="en">{e(g["en"])}</p>
    </div>
  </header>
  <dl>
    <dt>主人公</dt><dd>{e(g["hero"])}</dd>
    <dt>{e(g.get("when", "発売"))}</dt><dd>{e(g["platform"])}</dd>
  </dl>
  <p class="story">{e(g["story"])}</p>
  <div class="links">
    <a class="btn" href="{YTM_PL}{d["playlistId"]}" target="_blank" rel="noopener">▶ プレイリストを YouTube Music で開く</a>
    {extra}
    <a class="btn ghost" href="{wiki_url(g)}" target="_blank" rel="noopener">{e(g.get("wiki_label", "Wikipedia"))}</a>
    {more}
  </div>
  <details>
    <summary><span>曲一覧（{len(d["tracks"])}曲）</span> {badge}</summary>
    {note}
    {track_table(g["id"])}
  </details>
</article>'''


def fav_card(g):
    d = TRACKS[g["id"]]
    return f'''
<article class="game fav" id="{g["id"]}">
  <header>
    <div>
      <h3>{e(g["title"])}</h3>
      <p class="en">{e(g["en"])}　<span class="first">{e(g["first"])}</span></p>
    </div>
  </header>
  <p class="story">{e(g["story"])}</p>
  <div class="links">
    <a class="btn" href="{YTM_PL}{d["playlistId"]}" target="_blank" rel="noopener">▶ 歴代バージョンのプレイリストを開く</a>
  </div>
  <details>
    <summary><span>バージョン一覧（{len(d["tracks"])}曲）</span> <span class="badge com">ファン作成プレイリスト</span></summary>
    <p class="note">※ {e(g["note"])}</p>
    {track_table(g["id"], artist=True)}
  </details>
</article>'''


def page():
    total = sum(len(TRACKS[g["id"]]["tracks"]) for g in GAMES + LOS + ANIME)
    tl = "".join(
        f'<tr><td class="y">{e(g["year"])}</td>'
        f'<td><a href="#{g["id"]}">{e(g["title"])}</a>{" <span class=\"badge side\">外伝</span>" if g.get("side") else ""}</td>'
        f'<td>{e(g["hero"])}</td>'
        f'<td class="c">{len(TRACKS[g["id"]]["tracks"])}</td>'
        f'<td><a href="{wiki_url(g)}" target="_blank" rel="noopener">{e(g.get("wiki_label", "Wikipedia"))}</a></td></tr>'
        + ('<tr class="ev"><td class="y">1999年</td><td colspan="4">ユリウス・ベルモンドらがドラキュラを完全に滅ぼす（ゲーム化されていない出来事）</td></tr>'
           if g["id"] == "por" else "")
        for g in GAMES)
    bonus = "".join(
        f'<li><a href="{YTM_PL}{pid}" target="_blank" rel="noopener">{e(t)}</a><span>{e(desc)}</span></li>'
        for t, desc, pid in BONUS)
    cards = "".join(game_card(g) for g in GAMES)
    los_cards = "".join(game_card(g) for g in LOS)
    anime_cards = "".join(game_card(g) for g in ANIME)
    fav_cards = "".join(fav_card(g) for g in FAVS)
    return f'''<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{SITE_TITLE}</title>
<meta name="description" content="{SITE_DESC}">
<link rel="canonical" href="{SITE_URL}">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="icon" href="assets/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
<meta name="theme-color" content="#0c090d">
<meta property="og:type" content="website">
<meta property="og:site_name" content="悪魔城ドラキュラ 音楽館">
<meta property="og:title" content="{SITE_TITLE}">
<meta property="og:description" content="{SITE_DESC}">
<meta property="og:url" content="{SITE_URL}">
<meta property="og:image" content="{SITE_URL}assets/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="悪魔城ドラキュラ 音楽館 — Castlevania Music Archive">
<meta property="og:locale" content="ja_JP">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{SITE_TITLE}">
<meta name="twitter:description" content="{SITE_DESC}">
<meta name="twitter:image" content="{SITE_URL}assets/og-image.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700&amp;family=Shippori+Mincho:wght@500;700&amp;display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<header class="hero">
  <p class="kicker">Castlevania Music Archive</p>
  <h1><span>悪魔城ドラキュラ</span> <span>音楽館</span></h1>
  <p class="lead">千年にわたるベルモンド一族とドラキュラの戦いを、音楽でたどる。<br>
  {len(GAMES) + len(LOS) + len(ANIME)}作品・{total}曲を物語の時系列順にまとめました。</p>
  <nav>
    <a href="#timeline">年表</a>
    <a href="#relations">相関図</a>
    <a href="#favorites">血の涙 / Vampire Killer</a>
    <a href="#games">作品別の楽曲</a>
    <a href="#los">Lords of Shadow</a>
    <a href="#anime">アニメ版</a>
    <a href="#bonus">番外編</a>
  </nav>
</header>

<main>
<section id="timeline">
  <h2>年表</h2>
  <p class="sec-lead">作品名をクリックすると、あらすじと曲一覧へ移動します。</p>
  <div class="tw"><table class="tl">
    <thead><tr><th>物語の年代</th><th>作品</th><th>主人公</th><th class="c">曲数</th><th>詳細</th></tr></thead>
    <tbody>{tl}</tbody>
  </table></div>
  <p class="note">シリーズ全体については <a href="{wiki("悪魔城ドラキュラシリーズ")}" target="_blank" rel="noopener">Wikipedia「悪魔城ドラキュラシリーズ」</a> を参照。年代は公式年表に基づきます。「外伝」は公式年表から外れている作品です。</p>
</section>

<section id="relations">
  <h2>主人公の相関図</h2>
  <p class="sec-lead">聖鞭ヴァンパイアキラーの継承を軸に、各作品の主人公と関係者を並べています。<span class="legend">
    <span><i class="k bel"></i>ベルモンド一族</span> <span><i class="k mor"></i>モリス家</span> <span><i class="k hero"></i>その他の主人公</span> <span><i class="k dark"></i>ドラキュラの血統</span> <span><i class="k ally"></i>仲間</span></span></p>
  <div class="dg">{diagram()}</div>
</section>

<section id="favorites">
  <h2>二大名曲コレクション</h2>
  <p class="sec-lead">シリーズを象徴する「血の涙（Bloody Tears）」と「Vampire Killer」。作品ごとに姿を変える歴代バージョンだけを集めました。</p>
  {fav_cards}
</section>

<section id="games">
  <h2>作品別の楽曲</h2>
  <p class="sec-lead">「曲一覧」を開くと各曲へのリンクが表示されます。</p>
  <div class="filter"><input id="q" type="search" placeholder="曲名で検索（例: Vampire Killer、血の涙、幻想的舞曲）" aria-label="曲名で検索"><span id="qn"></span></div>
  {cards}
</section>

<section id="los">
  <h2>Lords of Shadow シリーズ</h2>
  <p class="sec-lead">2010年に始まったリブート三部作。上の年表とはつながらない別の世界の物語で、ベルモンドの祖ガブリエル自身がドラキュラになる過程を描きます。音楽はオスカル・アラウホによるフルオーケストラ。</p>
  <div class="dg">{los_diagram()}</div>
  <div class="los-cards">{los_cards}</div>
</section>

<section id="anime">
  <h2>アニメ版（Netflix）</h2>
  <p class="sec-lead">ゲームを原案にした Netflix のアニメシリーズ。登場人物や出来事はゲームの年表を下敷きにしつつ、独自の解釈で描かれています。</p>
  {anime_cards}
</section>

<section id="bonus">
  <h2>番外編</h2>
  <p class="sec-lead">時系列の外にあるクロスオーバー作品やリメイクのサウンドトラック。</p>
  <ul class="bonus">{bonus}</ul>
</section>
</main>

<footer>
  <p>非公式のファンサイトです。「悪魔城ドラキュラ」「Castlevania」は株式会社コナミデジタルエンタテインメントの商標・著作物です。</p>
  <p>楽曲は YouTube Music 上の公開プレイリストへのリンクで、音源そのものは本サイトに含まれません。「公式音源」はコナミが配信するトラック、「ファン作成プレイリスト」は公式配信が見つからなかった作品のものです。</p>
</footer>

<script>
(function () {{
  var q = document.getElementById('q'), qn = document.getElementById('qn');
  var games = [].slice.call(document.querySelectorAll('.game'));
  q.addEventListener('input', function () {{
    var s = q.value.trim().toLowerCase(), hits = 0;
    games.forEach(function (g) {{
      var n = 0;
      [].forEach.call(g.querySelectorAll('tbody tr:not(.grp)'), function (tr) {{
        var ok = !s || tr.textContent.toLowerCase().indexOf(s) !== -1;
        tr.hidden = !ok; if (ok) n++;
      }});
      [].forEach.call(g.querySelectorAll('tr.grp'), function (tr) {{ tr.hidden = !!s; }});
      g.hidden = !!s && n === 0;
      g.querySelector('details').open = !!s && n > 0;
      if (s) hits += n;
    }});
    qn.textContent = s ? hits + ' 曲' : '';
  }});
}})();
</script>
</body>
</html>
'''


if __name__ == "__main__":
    (ROOT / "index.html").write_text(page(), encoding="utf-8")
    print("wrote index.html")
