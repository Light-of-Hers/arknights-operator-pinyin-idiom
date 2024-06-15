import re
import json
import csv
from collections import defaultdict, namedtuple
from typing import List
import tqdm
import pypinyin as ppy

Operator = namedtuple("Operator", ["tier", "rank", "spell", "name"])


class keydefaultdict(defaultdict):
    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)
        else:
            ret = self[key] = self.default_factory(key)
            return ret


def _get_spell_unmaker():
    spell_marks_pat = re.compile(r"([āáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜ])")
    spell_marks_map = {
        "ā": "a",
        "á": "a",
        "ǎ": "a",
        "à": "a",
        "ē": "e",
        "é": "e",
        "ě": "e",
        "è": "e",
        "ī": "i",
        "í": "i",
        "ǐ": "i",
        "ì": "i",
        "ō": "o",
        "ó": "o",
        "ǒ": "o",
        "ò": "o",
        "ū": "u",
        "ú": "u",
        "ǔ": "u",
        "ù": "u",
        # "ǖ": "ü",
        # "ǘ": "ü",
        # "ǚ": "ü",
        # "ǜ": "ü",
        "ǖ": "v",
        "ǘ": "v",
        "ǚ": "v",
        "ǜ": "v",
    }
    f_subst = lambda m: spell_marks_map[m.group(0)]
    return keydefaultdict(lambda pinyin_str: spell_marks_pat.sub(f_subst, pinyin_str))


def _get_spell2opts():
    rank = defaultdict(lambda: 114514)
    with open("./tier_6_1v1_ranking.csv", "r") as fp:
        for row in csv.reader(fp, delimiter="\t"):
            rank[row[2]] = float(row[1])
    spell2opts = defaultdict(list)
    with open("./operator_table.json", "r") as fp:
        for name, tier, spell in json.load(fp):
            spell = spell[0]
            # 星级降序，排名升序，拼音升序，名字升序
            opt = Operator(-tier, rank[name], spell, name)
            spell2opts[spell].append(opt)
    ret = defaultdict(list)
    for spell, opts in spell2opts.items():
        tier2opts: List[List[Operator]] = [[] for _ in range(6)]
        for opt in opts:
            tier2opts[opt.tier + 6].append(opt)
        ret[spell] = [" ".join(opt.name for opt in sorted(opts)) for opts in tier2opts]
    return ret


def main():
    spell_unmarker = _get_spell_unmaker()
    spell2opts = _get_spell2opts()
    spell2idioms = defaultdict(list)
    with open("./idiom.json", "r") as fp:
        idioms = json.load(fp)
    csv_rows = [("编号", "成语", "拼音", *(f"{x}星干员" for x in range(6, 0, -1)))]
    cnt = 1
    for idm in tqdm.tqdm(idioms):
        word: str = idm["word"]
        # marked_spells: List[str] = idm["pinyin"].split()
        marked_spells: List[str] = [c[0] for c in ppy.pinyin(word)]
        spells: List[str] = [spell_unmarker[spell] for spell in marked_spells]
        opts_lst: List[List[Operator]] = [spell2opts[spell] for spell in spells]
        if any(len(opts) <= 0 for opts in opts_lst):
            continue
        for i, opts in enumerate(opts_lst):
            csv_rows.append(
                (cnt if i == 0 else "", word if i == 0 else "", marked_spells[i], *opts)
            )
        for spell in set(spells):
            spell2idioms[spell].append(word)
        cnt += 1

    with open("./idiom_to_spell_and_operators.csv", "w", encoding="utf-8-sig") as fp:
        csv.writer(fp, delimiter=",").writerows(csv_rows)

    csv_rows = [("拼音", *(f"{x}星干员" for x in range(6, 0, -1)), "成语")]
    for spell, opts in sorted(spell2opts.items(), key=lambda t: t[0]):
        if len(opts) > 0:
            csv_rows.append((spell, *opts, " ".join(spell2idioms[spell])))
    with open("./spell_to_operators_and_idioms.csv", "w", encoding="utf-8-sig") as fp:
        csv.writer(fp, delimiter=",").writerows(csv_rows)


if __name__ == "__main__":
    main()
