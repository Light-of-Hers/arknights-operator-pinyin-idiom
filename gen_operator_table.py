import json
import pypinyin as ppy
from string import ascii_letters, digits


def main():
    non_hanzi = ascii_letters + digits
    with open("./character_table.json", "r") as fp:
        char_tab = json.load(fp)
    tier_map = {
        ch["name"]: int(ch["rarity"].split("_")[-1])
        for ch in char_tab.values()
        if ch["displayNumber"] is not None
    }
    mapping = [
        [name, tier, ppy.pinyin(name, ppy.NORMAL, heteronym=True)[0]]
        for name, tier in tier_map.items()
        if name[0] not in non_hanzi
    ]
    # 把多音字排在前面，方便之后手动删除多余读音（不太确定的读音以官方的中文语音为准，比如“吽”的读音好像是hōu）
    mapping.sort(key=lambda t: len(t[-1]), reverse=True)
    with open("./operator_table.json", "w") as fp:
        json.dump(mapping, fp, ensure_ascii=False)


if __name__ == "__main__":
    main()
