# まえがき {.unnumbered}
このドキュメントは、NXP社のLPCマイクロコントローラ3種でNXPのI^2^CインタフェースIC
**`SC18IM700`** をエミュレートしつつ拡張もするプログラム群
___TinyI2Cプロジェクト___ を解説する本です。

筆者が仕事で同じスレーブアドレスのI^2^Cデバイスを複数同時に（といっても4個程度）
PCから操作する必要があったことから、USBなどとI^2^Cバスの相互通信が可能なICを
探していました。その時に見つけたのが **`SC18IM700`** でした。いろいろあって
サンプルを入手もした[^mbed_fest] のですが、必要なバスが1ポート分しかないので
別の方法を考えることにしました。

**`SC18IM700`** のコマンド体系が使いやすかったので一部をそのまま用いつつ、
例によってmbed^TM^対応マイコンを使おうと考え、 **`LPC824`** シリーズマイコンが
I^2^Cマスタ機能を _4基_ 搭載しているということから条件が一致しました。

この本は プロジェクトの概要説明とコマンドセット/Pythonライブラリ
の解説をします。いまのところ特にオチは用意してません~~がまたも６０ページ前後の
超大作になりそうです~~ 。
<!-- mbed^TM^ LPC1768 / LPC824 / LPC11U35に移植した話、TinyI2C基板の回路図、
それぞれのピン配置図ギャラリー、GUI -->

<#include "1.0_tinyI2Cabstract.md">
<#include "2.0_Commands.md">
<#include "3.0_PythonAPI.md">
<#include "9.1_RevHistory.md">

<!--  -->
[^mbed_fest]: 2014年のmbed祭りのいずれかで懇親会のおみやげにサンプルブックを入手したとかだったような