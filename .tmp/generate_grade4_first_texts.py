"""Generate grade 4 first semester English textbook source JSON.

Purpose:
- Convert the user's pasted Unit 1-8 English textbook text into the site's
  structured `english-textbook-page.v1` JSON format.
- Add Chinese translations because the pasted source only provided English.
- Keep complete English sentences as individual TTS chunks where practical.

This is an intermediate task artifact for the 2026-08-20 site update.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "content" / "english" / "texts" / "grade-4-first.json"


def c(english: str, translation: str) -> dict:
    return {"english": english, "translation": translation}


def line(english: str, translation: str, speaker: str | None = None) -> dict:
    item = {"chunks": [c(english, translation)]}
    if speaker:
        item["speaker"] = speaker
    return item


def chunks(items: list[tuple[str, str]], speaker: str | None = None) -> dict:
    item = {"chunks": [c(english, translation) for english, translation in items]}
    if speaker:
        item["speaker"] = speaker
    return item


def section(heading: str, lines: list[dict]) -> dict:
    return {"heading": heading, "lines": lines}


data = {
    "schema": "english-textbook-page.v1",
    "page_title": "广州英语四年级上册课文朗读",
    "description": "Unit 1-8 | 英文逐句朗读 | 中文译文点击显示",
    "kicker": "四年级 · 上学期 · 课文",
    "title": "广州英语四年级上册课文朗读",
    "summary": "Unit 1-8 | Get Started 与 Close Reading 主要内容 | 中文译文点击显示",
    "stats": {
        "unit_label": "Unit 1-8",
        "item_suffix": "句/项",
    },
    "output": "subjects/english/grade-4/first/texts/index.html",
    "source_notes": [
        "Created on 2026-08-20 from user-pasted Unit 1-8 English text.",
        "The source provided English only; Chinese translations were generated during site integration.",
        "Unit titles were inferred from source task titles and content themes.",
    ],
    "units": [
        {
            "id": "unit-1",
            "label": "Unit 1",
            "title": "Welcome to My Home",
            "sections": [
                section(
                    "Get Started · Task A",
                    [
                        line("Welcome!", "欢迎！", "A"),
                        line("Come on in, please.", "请进来吧。", "A"),
                        line("These are for you.", "这些是给你的。", "B"),
                        chunks(
                            [
                                ("Thank you!", "谢谢你！"),
                                ("What beautiful flowers!", "多么漂亮的花啊！"),
                            ],
                            "A",
                        ),
                        line("I'm glad you like them.", "我很高兴你喜欢它们。", "B"),
                        line("Have a seat, please.", "请坐。", "A"),
                        line("Can I get you a drink?", "我可以给你拿点喝的吗？", "A"),
                        chunks(
                            [
                                ("Thanks.", "谢谢。"),
                                ("Water is fine.", "水就可以。"),
                            ],
                            "B",
                        ),
                        line("Can I use the bathroom?", "我可以用一下洗手间吗？", "B"),
                        chunks(
                            [
                                ("Sure!", "当然！"),
                                ("The bathroom is over there.", "洗手间在那边。"),
                            ],
                            "A",
                        ),
                        chunks(
                            [
                                ("Oh!", "哦！"),
                                ("Baby Sam!", "小宝宝山姆！"),
                                ("May I have a look?", "我可以看一看吗？"),
                            ],
                            "B",
                        ),
                        chunks(
                            [
                                ("Sure!", "当然！"),
                                ("Go ahead.", "请吧。"),
                            ],
                            "A",
                        ),
                    ],
                ),
                section(
                    "Close Reading · Task A",
                    [
                        line("Hi, Aiwen.", "嗨，艾文。", "Nikki"),
                        chunks(
                            [
                                ("Welcome, Nikki!", "欢迎你，尼基！"),
                                ("Come on in, please.", "请进来吧。"),
                            ],
                            "Aiwen",
                        ),
                        line("These are for you.", "这些是给你的。", "Nikki"),
                        line("Can I get you a drink?", "我可以给你拿点喝的吗？", "Aiwen"),
                        chunks(
                            [
                                ("Oh, yes, please.", "哦，好的，请给我一点。"),
                                ("Thanks.", "谢谢。"),
                            ],
                            "Nikki",
                        ),
                        line("Water or tea?", "水还是茶？", "Aiwen"),
                        chunks(
                            [
                                ("A cup of tea, please.", "请给我一杯茶。"),
                                ("Your home looks nice.", "你的家看起来很漂亮。"),
                            ],
                            "Nikki",
                        ),
                        line("Let me show you around.", "让我带你参观一下。", "Aiwen"),
                        line("Great!", "太好了！", "Nikki"),
                        line("This is my mum.", "这是我妈妈。", "Aiwen"),
                        chunks(
                            [
                                ("Nice to meet you!", "很高兴见到你！"),
                                ("Are you Nikki?", "你是尼基吗？"),
                            ],
                            "Mum",
                        ),
                        chunks(
                            [
                                ("Yes, I am.", "是的，我是。"),
                                ("Nice to meet you, too.", "我也很高兴见到你。"),
                            ],
                            "Nikki",
                        ),
                    ],
                ),
            ],
        },
        {
            "id": "unit-2",
            "label": "Unit 2",
            "title": "What Should You Do?",
            "sections": [
                section(
                    "Get Started · Task A",
                    [
                        line("Have a seat, please.", "请坐。", "A"),
                        line("Thank you.", "谢谢你。", "B"),
                        line("Would you like some rice?", "你想要一些米饭吗？", "A"),
                        chunks(
                            [
                                ("No, thanks.", "不用了，谢谢。"),
                                ("I'm good.", "我够了。"),
                            ],
                            "B",
                        ),
                        line("Can I have some more soup, please?", "我可以再喝一些汤吗？", "C"),
                        line("The food is so good.", "饭菜太好吃了。", "A"),
                        line("I'm glad you like it.", "我很高兴你喜欢。", "B"),
                        line("Could you please pass me the tissues?", "请你把纸巾递给我好吗？", "A"),
                        line("Here you are.", "给你。", "B"),
                    ],
                ),
                section(
                    "Close Reading · Task A · What Should You Do?",
                    [
                        line("It's dinner time.", "现在是晚餐时间。"),
                        line("You're at a friend's house.", "你在朋友家里。"),
                        line(
                            'If you like the food, you can say, "The food is great!"',
                            "如果你喜欢这些食物，你可以说：“饭菜很棒！”",
                        ),
                        line(
                            'If you feel full, kindly say, "No, thank you. I\'m good."',
                            "如果你觉得饱了，要有礼貌地说：“不用了，谢谢。我够了。”",
                        ),
                        line(
                            'If you can\'t get something, ask someone, "Could you please pass me the ...?"',
                            "如果你拿不到某样东西，可以问别人：“请你把……递给我好吗？”",
                        ),
                        line(
                            "If you drop your spoon on the floor, don't worry.",
                            "如果你把勺子掉在地上，不要担心。",
                        ),
                        line(
                            'Pick it up and say, "Excuse me. May I get a new spoon, please?"',
                            "把它捡起来，然后说：“打扰一下，我可以拿一把新的勺子吗？”",
                        ),
                        line(
                            'At the end of the dinner, always say, "Thank you!"',
                            "晚餐结束时，一定要说：“谢谢！”",
                        ),
                    ],
                ),
            ],
        },
        {
            "id": "unit-3",
            "label": "Unit 3",
            "title": "Cooking Noodles",
            "sections": [
                section(
                    "Get Started · Task A · Cooking Noodles",
                    [
                        line("First, wash the greens.", "首先，洗青菜。"),
                        line("Next, add some water.", "接着，加一些水。"),
                        line("Then, add the noodles.", "然后，加入面条。"),
                        line("Then, stir the noodles.", "然后，搅拌面条。"),
                        line("Then, add the greens.", "然后，加入青菜。"),
                        line("Last, enjoy!", "最后，享用吧！"),
                    ],
                ),
                section(
                    "Close Reading · Task A · How to Cook Dumplings",
                    [
                        line("First, add water into a pot.", "首先，往锅里加水。"),
                        line("Wait for the water to boil.", "等水烧开。"),
                        line("Next, add the dumplings.", "接着，加入饺子。"),
                        line("Be careful with the hot water!", "小心热水！"),
                        line("Then, stir the dumplings with a spoon.", "然后，用勺子搅动饺子。"),
                        line(
                            "When the dumplings come up to the top, add some cold water.",
                            "当饺子浮到水面时，加入一些冷水。",
                        ),
                        line("Wait until they come up again.", "等它们再次浮上来。"),
                        line("Then, take them out.", "然后，把它们捞出来。"),
                        line("Remember to turn off the stove!", "记得关掉炉子！"),
                        line("Time to eat!", "该吃啦！"),
                    ],
                ),
            ],
        },
        {
            "id": "unit-4",
            "label": "Unit 4",
            "title": "Doing Chores",
            "sections": [
                section(
                    "Get Started · Task A · Doing Chores",
                    [
                        line("First, take out the rubbish.", "首先，把垃圾拿出去。"),
                        line("Then, clear the table.", "然后，收拾桌子。"),
                        line("Next, wash the dishes.", "接着，洗碗。"),
                        line("Then, put away the dishes.", "然后，把碗碟收好。"),
                        line("Then, clean the table.", "然后，擦桌子。"),
                        line("Last, sweep the floor.", "最后，扫地。"),
                    ],
                ),
                section(
                    "Close Reading · Task A",
                    [
                        chunks(
                            [
                                ("Lucas, the kitchen looks dirty.", "卢卡斯，厨房看起来很脏。"),
                                ("How do we clean it up?", "我们怎么把它打扫干净呢？"),
                            ],
                            "Aiwen",
                        ),
                        line(
                            "Well, maybe we can wash the dishes first, and then take the rubbish out.",
                            "嗯，也许我们可以先洗碗，然后把垃圾拿出去。",
                            "Lucas",
                        ),
                        chunks(
                            [
                                ("Our rubbish bin is full.", "我们的垃圾桶满了。"),
                                ("How about we take out the rubbish first?", "我们先把垃圾拿出去怎么样？"),
                            ],
                            "Aiwen",
                        ),
                        chunks(
                            [
                                ("Cool.", "好啊。"),
                                ("Then, we can clear the table and wash the dishes next.", "然后，我们接着可以收拾桌子、洗碗。"),
                            ],
                            "Lucas",
                        ),
                        chunks(
                            [
                                ("Great!", "太好了！"),
                                ("We can sweep the floor at the end.", "最后我们可以扫地。"),
                                ("Let's get to work.", "我们开始干活吧。"),
                            ],
                            "Aiwen",
                        ),
                    ],
                ),
            ],
        },
        {
            "id": "unit-5",
            "label": "Unit 5",
            "title": "Kindness Is Everywhere",
            "sections": [
                section(
                    "Get Started · Task A · Kindness Is Everywhere",
                    [
                        line('smile and say "hi" to others', "微笑并向别人说“嗨”"),
                        line("hold the door open for others", "为别人扶着门"),
                        line("cheer up a friend", "让朋友高兴起来"),
                        line("give a helping hand", "伸出援手"),
                        line("be ready to help", "乐于助人"),
                        line("ask others to join in", "邀请别人加入"),
                        chunks(
                            [
                                ("Mulan is kind.", "木兰很善良。"),
                                ("She likes to give a helping hand.", "她喜欢伸出援手。"),
                            ],
                            "A",
                        ),
                    ],
                ),
                section(
                    "Close Reading · Task A",
                    [
                        chunks(
                            [
                                ("Mr Young, thank you so much for having us over.", "杨先生，非常感谢您邀请我们来做客。"),
                                ("I really like the food.", "我真的很喜欢这些食物。"),
                            ],
                            "A",
                        ),
                        chunks(
                            [
                                ("You're welcome.", "不客气。"),
                                ("It was kind of you to ask Alice to join you for lunch.", "你们邀请爱丽丝一起吃午饭，真是太友善了。"),
                            ],
                            "Mr Young",
                        ),
                        chunks(
                            [
                                ("Alice is so nice.", "爱丽丝真好。"),
                                ("She's kind to us, too.", "她对我们也很友善。"),
                            ],
                            "B",
                        ),
                        line(
                            "Yes, she always says nice things and gets on well with everyone.",
                            "是的，她总是说友善的话，并且和每个人都相处得很好。",
                            "C",
                        ),
                        line("She cheers me up when I'm sad.", "我难过的时候，她会让我高兴起来。", "D"),
                        line("And she's always ready to help!", "而且她总是乐于帮忙！", "E"),
                        chunks(
                            [
                                ("Haha!", "哈哈！"),
                                ("Alice talks a lot about you guys, too!", "爱丽丝也经常说起你们！"),
                                ("You guys make her happy.", "你们让她很开心。"),
                            ],
                            "Mr Young",
                        ),
                    ],
                ),
            ],
        },
        {
            "id": "unit-6",
            "label": "Unit 6",
            "title": "Ways to Love Your Family",
            "sections": [
                section(
                    "Get Started · Task A · Ways to Love Your Family",
                    [
                        line("say nice words", "说好听的话"),
                        line("give a gift", "送礼物"),
                        line("spend one-on-one time", "一对一相处"),
                        line("help out", "帮忙"),
                        line("buy a birthday cake", "买生日蛋糕"),
                        line("read a book", "读一本书"),
                        line("cook together", "一起做饭"),
                        line("cook birthday noodles", "做生日面"),
                        line("take a walk", "散步"),
                        line('say "Happy birthday!"', "说“生日快乐！”"),
                        line("How does Aiwen say nice words?", "艾文怎样说好听的话？", "A"),
                        line('She says, "Happy birthday!"', "她说：“生日快乐！”", "B"),
                    ],
                ),
                section(
                    "Close Reading · Task A",
                    [
                        chunks(
                            [
                                ("My grandma's birthday is next Sunday.", "我奶奶的生日是下周日。"),
                                ("She likes to cook for me and makes me laugh all the time.", "她喜欢给我做饭，还总是逗我笑。"),
                                ("I want to show her my love.", "我想表达我对她的爱。"),
                                ("What can I do?", "我能做什么呢？"),
                            ],
                            "Aiwen",
                        ),
                        chunks(
                            [
                                ("Does she like cake?", "她喜欢蛋糕吗？"),
                                ("You can buy her a birthday cake.", "你可以买一个生日蛋糕给她。"),
                            ],
                            "Yuting",
                        ),
                        line("Well, she doesn't like it that much.", "嗯，她不太喜欢蛋糕。", "Aiwen"),
                        line(
                            "Hmm ... Maybe you can help out in the kitchen and cook with her!",
                            "嗯……也许你可以在厨房帮忙，和她一起做饭！",
                            "Yuting",
                        ),
                        chunks(
                            [
                                ("Buy a cookbook for her.", "给她买一本食谱书。"),
                                ("Surprise her!", "给她一个惊喜！"),
                            ],
                            "Sam",
                        ),
                        line(
                            "You can tell her a funny story and make her laugh.",
                            "你可以给她讲一个有趣的故事，让她笑起来。",
                            "Haoran",
                        ),
                        line(
                            "Why don't you cook her something or draw her a nice picture?",
                            "你为什么不给她做点吃的，或者给她画一幅漂亮的画呢？",
                            "James",
                        ),
                    ],
                ),
            ],
        },
        {
            "id": "unit-7",
            "label": "Unit 7",
            "title": "Jobs and Work Time",
            "sections": [
                section(
                    "Get Started · Task A · Jobs and Work Time",
                    [
                        chunks(
                            [
                                ("Mr Zhang is a teacher.", "张先生是一名老师。"),
                                ("He works from 8:00 to 16:30.", "他的工作时间是从八点到十六点三十分。"),
                            ]
                        ),
                        chunks(
                            [
                                ("Ms Zhou is a cook.", "周女士是一名厨师。"),
                                ("She works from 6:30 to 15:00.", "她的工作时间是从六点三十分到十五点。"),
                            ]
                        ),
                        chunks(
                            [
                                ("Mr Fu is a worker.", "傅先生是一名工人。"),
                                ("He works from 9:00 to 18:00.", "他的工作时间是从九点到十八点。"),
                            ]
                        ),
                        chunks(
                            [
                                ("Mr Yuan is a waiter.", "袁先生是一名服务员。"),
                                ("He works from 14:00 to 22:00.", "他的工作时间是从十四点到二十二点。"),
                            ]
                        ),
                        chunks(
                            [
                                ("Mr Gao is an IT worker.", "高先生是一名 IT 工作人员。"),
                                ("He works from 10:00 to 19:00.", "他的工作时间是从十点到十九点。"),
                            ]
                        ),
                        chunks(
                            [
                                ("Miss Wang is a doctor.", "王小姐是一名医生。"),
                                ("She works from 8:00 to 17:00.", "她的工作时间是从八点到十七点。"),
                            ]
                        ),
                        chunks(
                            [
                                ("Mr Luo is a gardener.", "罗先生是一名园丁。"),
                                ("He works from 6:00 to 14:00.", "他的工作时间是从六点到十四点。"),
                            ]
                        ),
                        chunks(
                            [
                                ("Mrs Chen is a cleaner.", "陈太太是一名清洁工。"),
                                ("She works from 9:00 to 16:00.", "她的工作时间是从九点到十六点。"),
                            ]
                        ),
                        chunks(
                            [
                                ("Mr Wei is a taxi driver.", "魏先生是一名出租车司机。"),
                                ("He works from 5:30 to 14:30.", "他的工作时间是从五点三十分到十四点三十分。"),
                            ]
                        ),
                        chunks(
                            [
                                ("Mr Gao is an IT worker.", "高先生是一名 IT 工作人员。"),
                                ("He goes to work at 10 in the morning.", "他早上十点去上班。"),
                                ("He comes home at 7 in the evening.", "他晚上七点回家。"),
                            ],
                            "A",
                        ),
                    ],
                ),
                section(
                    "Close Reading · Task A · Aiwen's Family",
                    [
                        line("My dad is a bus driver.", "我爸爸是一名公交车司机。"),
                        line(
                            "He usually goes to work at 5 in the morning.",
                            "他通常早上五点去上班。",
                        ),
                        line("He comes home at 1 in the afternoon.", "他下午一点回家。"),
                        line(
                            "He gets ready for bed at around 10 o'clock at night.",
                            "他晚上十点左右准备睡觉。",
                        ),
                        line("My mum is a cook.", "我妈妈是一名厨师。"),
                        line("She goes to work at 5:30 in the morning.", "她早上五点半去上班。"),
                        line("She comes home at 3 in the afternoon.", "她下午三点回家。"),
                        line("She goes to bed at 10 at night.", "她晚上十点睡觉。"),
                        line("I'm a student, of course.", "当然，我是一名学生。"),
                        line(
                            "I get up at 7 and go to school at 7:30 in the morning.",
                            "我早上七点起床，七点半去上学。",
                        ),
                        line("I come home at 4 in the afternoon.", "我下午四点回家。"),
                        line("I go to bed at 9 at night.", "我晚上九点睡觉。"),
                    ],
                ),
            ],
        },
        {
            "id": "unit-8",
            "label": "Unit 8",
            "title": "Festivals",
            "sections": [
                section(
                    "Get Started · Task A · Festivals",
                    [
                        line("watch fireworks", "看烟花"),
                        line("eat mooncakes", "吃月饼"),
                        line("visit family and friends", "拜访家人和朋友"),
                        line("give out gifts", "分发礼物"),
                        line("make rice dumplings", "包粽子"),
                        line("have a big meal", "吃一顿大餐"),
                        chunks(
                            [
                                ("My favourite festival is ...", "我最喜欢的节日是……"),
                                ("On that day, we ...", "在那一天，我们……"),
                            ],
                            "A",
                        ),
                    ],
                ),
                section(
                    "Close Reading · Task A · Festival Chants",
                    [
                        line(
                            "Spring Festival is the time of year, when we meet family from far and near.",
                            "春节是一年中的这个时候，我们会和远近各地的家人相聚。",
                        ),
                        line(
                            "Come and sit, laugh and cheer, the best wishes are right here.",
                            "来坐一坐，欢笑喝彩，最美好的祝福就在这里。",
                        ),
                        line(
                            "I look back at the days we went through.",
                            "我回顾我们一起走过的日子。",
                        ),
                        line(
                            "I look forward to new things to do.",
                            "我期待要去做的新事情。",
                        ),
                        line(
                            "Gifts are part of the New Year, too.",
                            "礼物也是新年的一部分。",
                        ),
                        line(
                            "Hope all your dreams do come true.",
                            "希望你所有的梦想都能成真。",
                        ),
                    ],
                ),
            ],
        },
    ],
}


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    total = sum(
        len(line.get("chunks") or [line])
        for unit in data["units"]
        for section in unit["sections"]
        for line in section["lines"]
    )
    print(f"WROTE {OUTPUT.relative_to(ROOT)} units={len(data['units'])} chunks={total}")


if __name__ == "__main__":
    main()
