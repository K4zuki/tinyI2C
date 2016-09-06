---
title: NXPのICでNXPのICをエミュレートしてみた本
abstract: NXP社のLPCマイクロコントローラ3種でNXPのI^2^CインタフェースIC
    "SC18IM700" をエミュレートさせてみた
author: "KY技研 / @_K4ZUKI_"
date: C91/2016-Dec
documentclass: book
papersize: b5paper
comiket: "C91"
year: "2016"
publisher: "秋葉原キンコーズ"
# localfontdir: set during compilation
mainfont: RictyDiminished-Regular
sansfont: RictyDiminished-Regular
monofont: RictyDiminished-Regular
mainlang: Japanese
CJKoptions: BoldFont=RictyDiminished-Bold,
  ItalicFont=RictyDiminished-Oblique,
  BoldItalicFont=RictyDiminished-BoldOblique
CJKmainfont: RictyDiminished-Regular
CJKsansfont: RictyDiminished-Regular
CJKmonofont: RictyDiminished-Regular
geometry: top=30truemm,bottom=30truemm,left=20truemm,right=20truemm
keywords: keyword
secPrefix: Chapter
linkcolor: black
urlcolor: black
citecolor: black
chapter: true
listings: true
codeBlockCaptions: true
listingTitle: 'List'
listingTemplate: '---**$$listingTitle$$ $$i$$$$titleDelim$$ $$t$$**---'
...

# まえがき {.unnumbered}
このドキュメントは、NXP社のLPCマイクロコントローラ3種でNXPのI^2^CインタフェースIC
**`SC18IM700`** をエミュレートしつつ拡張もするプログラム群を解説する本です。

筆者が仕事で同じスレーブアドレスのI2Cデバイスを複数同時に（といっても4個程度）
PCから操作する必要があったことから、USBなどとI2Cバスの相互通信が可能なICを
探していました。その時に見つけたのが **`SC18IM700`** でした。いろいろあって
サンプルを入手もした[^mbed_fest] のですが、必要なバスが1ポート分しかないので
別の方法を考えることにしました。

**`SC18IM700`** のコマンド体系が使いやすかったので一部をそのまま用いつつ、
例によってmbed^TM^対応マイコンを使おうと考え、 **`LPC824`** シリーズマイコンが
I^2^Cマスタ機能を _4基_ 搭載しているということから条件が一致しました。

この本は **`SC18IM700`** ICの解説、mbed^TM^ LPC1768 / LPC824 / LPC11U35に移植した話、
それぞれのピン配置図ギャラリー、コマンドセットの解説、GUIの解説をします。
いまのところ特にオチは用意してません。

[^mbed_fest]: 2014年のmbed祭りのいずれかで懇親会のおみやげにサンプルブックを入手したとかだったような
