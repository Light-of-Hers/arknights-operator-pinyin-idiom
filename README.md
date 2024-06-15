# 明日方舟干员名字首字拼音组合成语

Motivation 来自于 NGA 的一个贴子 https://ngabbs.com/read.php?tid=40538426 

![alt text](./media/-klbw3Q19i-4wwjZfT1kS8c-1ti.jpg)

想配个~~带苏苏洛的~~有趣的队伍，但苦于有限的语文积累，便直接跑程序枚举。

- 成语数据 [idiom.json](./idiom.json) 来自 https://github.com/pwxcoo/chinese-xinhua/blob/master/data/idiom.json ，是从中华字典和新华字典数据库中收集的。其中每一条数据的 "word" 属性就是成语本身，"pinyin" 属性是用空格分隔的带音调的拼音（不过这里面有些成语拼音标注似乎有问题，实现上改用 [pypinyin](https://github.com/mozillazg/python-pinyin) 库来做注音）。
- 干员数据 [character_table.json](./character_table.json) 来自解包数据 https://github.com/Kengxxiao/ArknightsGameData/blob/master/zh_CN/gamedata/excel/character_table.json ，截至"生路"SideStory。不过这里面包含了所有的玩家可操控单位，包括各种装置、召唤物以及集成战略的临时招募干员，比对了一下玩家的可获取干员似乎满足 "displayNumber" 不为 null（反正筛选出来刚好 331 个……）。可以用 [pypinyin](https://github.com/mozillazg/python-pinyin) 库来获得干员名字首字的拼音，不过一些多音字需要手动筛选注音。
- 输出的结果会对同星级的干员进行排序，其中1~5星干员按拼音升序排序，6星干员按 [1v1强度榜](https://vote.ltsc.vip/) 来排（"巴别塔"、"慈悲灯塔"、"生路"的新干员里面还没有，就自己随便找几个位置插进去了，详见 [tier_6_1v1_ranking.csv](./tier_6_1v1_ranking.csv)）。本来想用狼榜来排，但是1v1榜直接在网页复制粘贴太方便了，而且也更符合大部分玩家的使用体验。
- 输出结果保存在 [idiom_to_spell_and_operators.csv](./idiom_to_spell_and_operators.csv) 和 [spell_to_operators_and_idioms.csv](./spell_to_operators_and_idioms.csv)，前者记录满足条件的成语所匹配的干员，后者记录各个干员可以匹配的满足条件的成语。这两个结果也保存到了在线文档中: https://kdocs.cn/l/ckgUL3U9Qjn9 。


## 复现方法

下载该仓库：
```bash
git clone https://github.com/Light-of-Hers/arknights-operator-pinyin-idiom.git
cd arknights-operator-pinyin-idiom
```

安装必要的 python 库：
```bash
python3 -m pip install --user pypinyin tqdm
```

生成干员数据：
```bash
python3 gen_operator_table.py
``` 
输出数据保存在 [operator_table.json](./operator_table.json)，需要自己手动去除其中的一部分多音字的多余注音（首字是多音字的干员都排在前面）。仓库中保存的是已经去除多余注音的结果。

生成结果：
```python
python3 gen_results.py
```
输出结果保存在 [idiom_to_spell_and_operators.csv](./idiom_to_spell_and_operators.csv) 和 [spell_to_operators_and_idioms.csv](./spell_to_operators_and_idioms.csv)，前者记录满足条件的成语所匹配的干员，后者记录各个干员可以匹配的满足条件的成语。

