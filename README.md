# polyomino

ポリオミノの敷き詰め問題を解く。

ブログを書いた。
[ポリオミノの敷き詰め問題をDancingLinksとKnuth's Algorithm Xを使って解く - matsu7874のブログ](https://matsu7874.hatenablog.com/entry/2018/07/15/200000)

## ポリオミノの敷き詰め問題とは

こういうやつ。

* [Amazon | 明治ミルクチョコレートパズル ピュア(甘め) | 立体パズル | おもちゃ](https://amzn.to/2LfraiR)
* [Amazon | プラパズル テトロミノ | 立体パズル | おもちゃ](https://amzn.to/2uB1J4f)

## Knuth's Algorithm Xの分かりやすい解説ページ

上記のポリオミノの敷き詰め問題はexact cover problemという問題で、これはKnuth's Algorithm Xで効率よく全探索できる。

* [Knuth's Algorithm XとDancing Linksの解説 - TopCoderとJ言語と時々F#](http://d.hatena.ne.jp/JAPLJ/20090902/1251901464)
* [Knuth's Algorithm X - Wikipedia](https://en.wikipedia.org/wiki/Knuth%27s_Algorithm_X)

## 2次元の問題

入力は下記の形式で与えられる

```txt
敷き詰め領域のYサイズ 敷き詰め領域のXサイズ

Y行X列の敷き詰め領域
-が空白
oが既に埋まっている箇所

ポリオミノの個数

ポリオミノの情報
Yサイズ　Xサイズ　名前
Y行X列のポリオミノの形状
```

```txt
3 3
---
---
---
3
2 3 A
ooo
o..
2 2 B
oo
o.
1 2 C
oo
```

ポリオミノは回転、裏返しを可能と考える。
