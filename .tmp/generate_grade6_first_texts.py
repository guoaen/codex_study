"""Intermediate generator for the 2026-07-10 grade 6 first-semester text page.

Purpose:
- Fuse two user-provided Markdown files for Guangzhou grade 6 English Unit 1-7 + Review.
- Keep source A as the main order/content source and use source B for useful wording clues.
- Write the maintainable JSON source consumed by tools/build_textbook_page.py.

This file is intentionally kept in .tmp as an auditable intermediate artifact.
"""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "content" / "english" / "texts" / "grade-6-first.json"
ENGLISH_SPLIT_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z(])")


def split_english(text: str) -> list[str]:
    return [part.strip() for part in ENGLISH_SPLIT_RE.split(text) if part.strip()]


def split_chinese(text: str) -> list[str]:
    parts: list[str] = []
    buf = ""
    i = 0
    while i < len(text):
        if text.startswith("……", i):
            buf += "……"
            i += 2
            if buf.strip() != "……" and i < len(text) and not text[i].isspace():
                parts.append(buf.strip())
                buf = ""
            continue
        ch = text[i]
        buf += ch
        i += 1
        if ch in "。！？" and i < len(text):
            parts.append(buf.strip())
            buf = ""
    if buf.strip():
        parts.append(buf.strip())
    return parts


def line(english: str, translation: str, speaker: str = "") -> dict:
    english_parts = split_english(english)
    translation_parts = split_chinese(translation)
    if len(english_parts) > 1 and len(english_parts) == len(translation_parts):
        chunks = [
            {"english": english_part, "translation": translation_part}
            for english_part, translation_part in zip(english_parts, translation_parts)
        ]
    else:
        chunks = [{"english": english, "translation": translation}]
    result = {"chunks": chunks}
    if speaker:
        result["speaker"] = speaker
    return result


def multi(speaker: str, chunks: list[tuple[str, str]]) -> dict:
    result = {"chunks": [{"english": english, "translation": translation} for english, translation in chunks]}
    if speaker:
        result["speaker"] = speaker
    return result


DATA = {
    "schema": "english-textbook-page.v1",
    "page_title": "广州英语六年级上册课文朗读",
    "description": "Unit 1-7 + Review | 英文逐句朗读 | 中文译文点击显示",
    "kicker": "六年级 · 上学期 · 课文",
    "title": "广州英语六年级上册课文朗读",
    "summary": "Unit 1-7 + Review | Get Started 与 Close Reading 主要内容 | 中文译文点击显示",
    "stats": {"unit_label": "Unit 1-7 + Review", "item_suffix": "句/项"},
    "output": "subjects/english/grade-6/first/texts/index.html",
    "source_notes": [
        "Merged on 2026-07-10 from two user-provided Markdown files.",
        "Source A controls dialogue/article order where Source B was reordered or simplified.",
        "Source B contributes useful task wording and Chinese meaning clues.",
    ],
    "units": [
        {
            "id": "unit-1",
            "label": "Unit 1",
            "title": "I Am Angry",
            "sections": [
                {
                    "heading": "Get Started · Task A",
                    "lines": [
                        line("yell and cry", "大喊大叫、哭泣", "Shouldn't do"),
                        line("shout bad words", "说脏话", "Shouldn't do"),
                        line("throw things", "乱扔东西", "Shouldn't do"),
                        line("go for a walk", "去散步冷静一下", "Should do"),
                        line("take a deep breath", "深呼吸", "Should do"),
                        line("count to ten", "数到十让自己平静", "Should do"),
                        line("... 6, 7, 8, 9, 10", "……六、七、八、九、十"),
                    ],
                },
                {
                    "heading": "Get Started · Task C",
                    "lines": [
                        line("What do you do when you are angry, Aiwen?", "艾文，你生气的时候会怎么做？", "Lucas"),
                        line("I take a deep breath.", "我会深呼吸。", "Aiwen"),
                        line("What if you are very angry?", "如果你非常生气呢？", "Lucas"),
                        multi(
                            "Aiwen",
                            [
                                ("Well, I usually go for a walk instead.", "嗯，我通常会改去散步。"),
                                ("What about you?", "你呢？"),
                            ],
                        ),
                        line("I just yell and cry!", "我就大喊大叫、哭出来！", "Lucas"),
                        line("I know how you feel, but that can hurt others.", "我理解你的感受，但那样可能会伤害别人。", "Aiwen"),
                        line("You are right. Maybe I'll try going for a walk too next time.", "你说得对。也许下次我也会试着去散步。", "Lucas"),
                    ],
                },
                {
                    "heading": "Close Reading · Task A",
                    "lines": [
                        line("Yafei, what's wrong? You look angry.", "亚飞，怎么了？你看起来很生气。", "Alice"),
                        multi(
                            "Yafei",
                            [
                                ("I am angry!", "我很生气！"),
                                ("Did you see that boy from another class?", "你看到那个别班的男孩了吗？"),
                                ("He kept making fun of me.", "他一直取笑我。"),
                                ("He made me look bad!", "他让我很难堪！"),
                            ],
                        ),
                        line("That's not nice!", "那样可不好！", "Alice"),
                        line("I really wanted to shout bad words at him!", "我真想对他说脏话！", "Yafei"),
                        multi(
                            "Alice",
                            [
                                ("Yafei, you can do better than that!", "亚飞，你可以做得比那更好！"),
                                ("Did you try taking a deep breath?", "你试过深呼吸吗？"),
                            ],
                        ),
                        line("I did, but it's not working.", "我试过了，但没用。", "Yafei"),
                        multi(
                            "Alice",
                            [
                                ("OK.", "好。"),
                                ("Let's try counting to ten.", "我们试着数到十吧。"),
                                ("We can do it together.", "我们可以一起数。"),
                                ("One, two, three ...", "一、二、三……"),
                            ],
                        ),
                        line("All right ... One, two, three ...", "好吧……一、二、三……", "Yafei"),
                        line("Go on. You are doing great!", "继续。你做得很好！", "Alice"),
                        line("... ten. I feel better now. Thanks, Alice.", "……十。我现在感觉好多了。谢谢你，爱丽丝。", "Yafei"),
                        line("No problem! Come on, let's go for a walk.", "不客气！来吧，我们去散散步。", "Alice"),
                    ],
                },
            ],
        },
        {
            "id": "unit-2",
            "label": "Unit 2",
            "title": "Talk It Out",
            "sections": [
                {
                    "heading": "Get Started · Task A",
                    "lines": [
                        line("You look like a lion!", "你看起来像一头狮子！", "Lucas"),
                        line("Lucas, can you stop it?", "卢卡斯，你能别这样了吗？", "Sam"),
                        line("Lion! Lion!", "狮子！狮子！", "Lucas"),
                        line("Lucas, stop!", "卢卡斯，住手！", "Sam"),
                        line("It's not funny!", "这不好笑！", "Sam"),
                        line("It's just a joke!", "这只是个玩笑！", "Lucas"),
                        line("Say sorry to me.", "向我道歉。", "Sam"),
                        line("Let's talk it out.", "我们把话说开吧。", "Yiming"),
                        line("Not a chance!", "没门！", "Lucas"),
                        line("have a new haircut", "理了新发型"),
                        line("make fun of ...", "取笑……"),
                        line("call ... names", "骂……，给……起难听的外号"),
                        line("yell at ...", "对……大喊"),
                        line("fight with each other", "互相打架，互相争吵"),
                        line("calm ... down", "让……冷静下来"),
                    ],
                },
                {
                    "heading": "Get Started · Task C",
                    "lines": [
                        line("Guys! Guys! Let's calm down and talk it out.", "大家！大家！我们冷静下来，把话说开吧。", "Yiming"),
                        line("Lucas called me names.", "卢卡斯骂我。", "Sam"),
                        line("What? You shouted bad words at me!", "什么？你对我说脏话了！", "Lucas"),
                        multi(
                            "Sam",
                            [
                                ("Oh, yeah?", "哦，是吗？"),
                                ("You made fun of my haircut.", "你取笑我的发型。"),
                                ("Now, everyone is laughing at me.", "现在大家都在笑我。"),
                                ("Put yourself in my shoes!", "设身处地为我想一想！"),
                            ],
                        ),
                        line("Guys, hold your horses. Please be nice.", "大家，别急。请友好一点。", "Yiming"),
                        line("Lucas, you need to say sorry to me.", "卢卡斯，你需要向我道歉。", "Sam"),
                        line("Not a chance!", "没门！", "Lucas"),
                    ],
                },
                {
                    "heading": "Close Reading · Task A",
                    "lines": [
                        line("Lucas, can we stop fighting and talk it out?", "卢卡斯，我们能不能别吵了，把话说开？", "Sam"),
                        multi(
                            "Lucas",
                            [
                                ("Sure.", "当然可以。"),
                                ("I just don't understand why you got so angry.", "我只是不明白你为什么这么生气。"),
                                ("I just made a joke!", "我只是开了个玩笑！"),
                                ("I felt so bad when you yelled at me.", "你对我大喊的时候，我感觉很难受。"),
                                ("Aren't we friends?", "我们不是朋友吗？"),
                            ],
                        ),
                        multi(
                            "Sam",
                            [
                                ("Yes, we are.", "是的，我们是朋友。"),
                                ("But I felt hurt when you made fun of my haircut and called me names.", "但你取笑我的发型、骂我的时候，我觉得受伤了。"),
                                ("And I felt even worse because everyone laughed at me.", "而且因为大家都笑我，我感觉更糟了。"),
                                ("I understand you didn't mean to hurt me, but you did.", "我知道你不是故意伤害我，但你的确伤害了我。"),
                            ],
                        ),
                        line("I really didn't mean to.", "我真的不是故意的。", "Lucas"),
                        line("I know. I'm sorry about shouting bad words at you and calling you names, too.", "我知道。我也为对你说脏话、骂你而道歉。", "Sam"),
                        line("It's okay, Sam. You were right to feel angry. I'm sorry.", "没关系，山姆。你生气是有道理的。对不起。", "Lucas"),
                        line("Let's put this behind us, all right?", "我们把这件事放下，好吗？", "Sam"),
                        line("Of course! Best friends forever!", "当然！永远的好朋友！", "Lucas"),
                    ],
                },
            ],
        },
        {
            "id": "unit-3",
            "label": "Unit 3",
            "title": "Work It Out Together",
            "sections": [
                {
                    "heading": "Get Started · Task A",
                    "lines": [
                        line("bring up the problem", "提出问题", "Step 1"),
                        line("listen to each other", "互相倾听", "Step 2"),
                        line("take turns to talk", "轮流说话", "Step 3"),
                        line("come up with ideas", "想出办法", "Step 4"),
                        line("work it out together", "一起解决问题", "Step 5"),
                        line("Dad, can I talk to you?", "爸爸，我能和你谈谈吗？", "Child"),
                        line("You might get hurt.", "你可能会受伤。", "Dad"),
                        line("I understand.", "我理解。", "Child"),
                        line("You may fall behind in school.", "你的学习可能会落后。", "Dad"),
                        line("But it will help me grow stronger.", "但它会帮助我变得更强壮。", "Child"),
                        line("Maybe I can try for a month first?", "也许我可以先试一个月？", "Child"),
                        line("Good idea!", "好主意！", "Dad"),
                        line("Thanks, Dad! I will be careful!", "谢谢爸爸！我会小心的！", "Child"),
                    ],
                },
                {
                    "heading": "Get Started · Task C",
                    "lines": [
                        line("What's wrong, Alice? You look sad.", "怎么了，爱丽丝？你看起来很难过。", "Yiming"),
                        line("I want to join the rock-climbing club at our school. But I'm worried my parents won't let me.", "我想加入学校的攀岩社团。但我担心父母不会让我参加。", "Alice"),
                        line("Why is that?", "为什么呢？", "Yiming"),
                        line("They may worry about me getting hurt.", "他们可能担心我会受伤。", "Alice"),
                        line("That makes sense. Maybe you can listen to their worries first, and then come up with an idea together.", "这有道理。也许你可以先听听他们的担心，然后一起想办法。", "Yiming"),
                        line("You are right. I'll do that. Thanks, Yiming!", "你说得对。我会这样做的。谢谢你，一鸣！", "Alice"),
                    ],
                },
                {
                    "heading": "Close Reading · Task A",
                    "lines": [
                        line("Alice's dad just got back home from work.", "爱丽丝的爸爸刚下班回家。", "Narrator"),
                        line("Hey, Dad, there's a club I ...", "嘿，爸爸，有个社团我……", "Alice"),
                        line("Can we talk about it later? I'm a little tired right now.", "我们能晚点再谈吗？我现在有点累。", "Dad"),
                        line("But ... Okay, Dad ...", "可是……好吧，爸爸……", "Alice"),
                        line("After dinner, in the living room, Alice comes in with a cup of tea.", "晚饭后，在客厅里，爱丽丝端着一杯茶进来了。", "Narrator"),
                        line("Dad, do you have a minute? I got you some tea.", "爸爸，你有时间吗？我给你泡了些茶。", "Alice"),
                        line("Thanks! What's on your mind, Alice?", "谢谢！爱丽丝，你想说什么？", "Dad"),
                        line("I'd like to join a rock-climbing club.", "我想加入一个攀岩社团。", "Alice"),
                        line("That sounds exciting, but also dangerous. Can you join when you're older?", "听起来很刺激，但也很危险。你能长大一点再参加吗？", "Dad"),
                        line("I understand your worries, Dad. But we have coaches to keep us safe.", "我理解你的担心，爸爸。但我们有教练保护我们的安全。", "Alice"),
                        line("That's good. Do you know how often they train?", "那很好。你知道他们多久训练一次吗？", "Dad"),
                        line("They train three times a week. And they have free practise every Sunday.", "他们每周训练三次。而且每个星期天都有自由练习。", "Alice"),
                        line("Is that a lot?", "那会不会太多？", "Dad"),
                        line("I can go twice a week!", "我可以每周去两次！", "Alice"),
                        line("All right.", "好吧。", "Dad"),
                        line("Great! Thanks, Dad!", "太好了！谢谢爸爸！", "Alice"),
                    ],
                },
            ],
        },
        {
            "id": "unit-4",
            "label": "Unit 4",
            "title": "Cat or Dog?",
            "sections": [
                {
                    "heading": "Get Started · Task A",
                    "lines": [
                        line("play during the night", "在夜间玩耍", "Cats"),
                        line("stay inside", "待在室内", "Cats"),
                        line("sleep during the day", "白天睡觉", "Cats"),
                        line("go for a walk", "出门散步", "Dogs"),
                        line("don't like to be alone", "不喜欢独处", "Dogs"),
                        line("lose hair", "掉毛", "Cats and dogs"),
                        line("love playing with toys", "喜欢玩玩具", "Cats and dogs"),
                    ],
                },
                {
                    "heading": "Get Started · Task C",
                    "lines": [
                        line("Nikki, what's it like to have a cat?", "妮基，养猫是什么感觉？", "Yiming"),
                        line("My cat follows me everywhere.", "我的猫到哪儿都跟着我。", "Nikki"),
                        line("Really? I thought cats liked to be alone. I also heard cats sleep during the day and play at night.", "真的吗？我以为猫喜欢独处。我还听说猫白天睡觉，晚上玩耍。", "Yiming"),
                        line("Well, my cat does sleep a lot during the day. But she wakes up to play with me when I get home from school.", "嗯，我的猫白天确实睡很多。但我放学回家时，她会醒来和我玩。", "Nikki"),
                        line("Does she eat a lot?", "她吃得多吗？", "Yiming"),
                        line("Not very much.", "不太多。", "Nikki"),
                    ],
                },
                {
                    "heading": "Close Reading · Task A",
                    "lines": [
                        multi(
                            "",
                            [
                                ("First, you need to think about space.", "首先，你需要考虑空间。"),
                                ("Cats stay inside most of the time.", "猫大部分时间待在室内。"),
                                ("However, dogs need to go for a walk at least twice a day.", "然而，狗每天至少需要出门散步两次。"),
                                ("They love going to parks!", "它们喜欢去公园！"),
                            ],
                        ),
                        multi(
                            "",
                            [
                                ("Next, dogs and cats have different habits.", "其次，狗和猫有不同的习惯。"),
                                ("Most cats like to sleep during the day and play during the night.", "大多数猫喜欢白天睡觉、夜间玩耍。"),
                                ("If you are a light sleeper, think twice before getting a cat.", "如果你睡觉很容易醒，养猫前要三思。"),
                            ],
                        ),
                        multi(
                            "",
                            [
                                ("You need to clean dogs often.", "你需要经常给狗清洁。"),
                                ("Unlike dogs, cats usually clean themselves.", "不像狗，猫通常会自己清洁自己。"),
                                ("They both love playing with toys.", "它们都喜欢玩玩具。"),
                                ("They both lose hair, too.", "它们也都会掉毛。"),
                            ],
                        ),
                        multi(
                            "",
                            [
                                ("Finally, make sure your family is OK with the idea, too!", "最后，也要确保你的家人同意这个想法！"),
                                ("Get an animal everyone will like!", "选择一种大家都会喜欢的动物！"),
                            ],
                        ),
                    ],
                },
            ],
        },
        {
            "id": "unit-5",
            "label": "Unit 5",
            "title": "Shop Smart",
            "sections": [
                {
                    "heading": "Get Started · Task A",
                    "lines": [
                        line("think about it more", "再多想一想"),
                        line("wait a few days", "等几天"),
                        line("learn about it", "了解它"),
                        line("look for a better deal", "寻找更划算的交易"),
                        line("give it a try", "试一试"),
                        line("compare and choose", "比较后再选择"),
                        line("Toys", "玩具"),
                        line("Dolls", "洋娃娃"),
                    ],
                },
                {
                    "heading": "Get Started · Task C",
                    "lines": [
                        line("Yafei, my aunt just gave me 300 yuan to get myself a gift!", "亚飞，我阿姨刚给了我三百元，让我给自己买一份礼物！", "Nikki"),
                        line("Wow! What do you plan to get?", "哇！你打算买什么？", "Yafei"),
                        line("I'm 12 now. I want to buy a bike.", "我现在十二岁了。我想买一辆自行车。", "Nikki"),
                        line("Hold your horses! Do you really need it?", "别急！你真的需要它吗？", "Yafei"),
                        line("What do you mean?", "你是什么意思？", "Nikki"),
                        line("Well, you may want to buy something, but it doesn't mean you really need it.", "嗯，你可能想买某样东西，但这并不意味着你真的需要它。", "Yafei"),
                        line("So, what should I do?", "那么，我该怎么做？", "Nikki"),
                        line("Maybe you can try it out first and think about it more.", "也许你可以先试一试，再多想一想。", "Yafei"),
                    ],
                },
                {
                    "heading": "Close Reading · Task A",
                    "lines": [
                        multi(
                            "",
                            [
                                ("First, think about it: Do I need that thing or do I just want it?", "首先，想一想：我需要那样东西，还是我只是想要它？"),
                                ("If you're not sure, wait a few days.", "如果你不确定，就等几天。"),
                                ("Then, make a decision.", "然后再做决定。"),
                            ],
                        ),
                        multi(
                            "",
                            [
                                ("Next, ask yourself: Do I need that thing right now?", "接着，问问自己：我现在就需要那样东西吗？"),
                                ("If not, you can buy it later.", "如果不需要，你可以以后再买。"),
                                ("Keep an eye out for sales, or try second-hand shops.", "留意促销，或者试试二手商店。"),
                            ],
                        ),
                        multi(
                            "",
                            [
                                ("After you make up your mind, try to learn more about it.", "下定决心后，试着多了解它。"),
                                ("Go online, ask others about it, or give it a try.", "上网查一查，问问别人，或者试用一下。"),
                            ],
                        ),
                        multi(
                            "",
                            [
                                ("Finally, compare and choose.", "最后，比较后再选择。"),
                                ("Ask yourself: Is it the best deal?", "问问自己：这是最划算的选择吗？"),
                                ("But be careful!", "但是要小心！"),
                                ('Sometimes "buy one get one free" may not be the better deal.', "有时候“买一送一”不一定更划算。"),
                                ('Check the "best before date" or BBD for short.', "检查“最佳食用日期”，简称 BBD。"),
                            ],
                        ),
                    ],
                },
            ],
        },
        {
            "id": "unit-6",
            "label": "Unit 6",
            "title": "Keep It Green",
            "sections": [
                {
                    "heading": "Get Started · Task A",
                    "lines": [
                        line("Some more, please.", "请再给我一些。"),
                        line("You can't finish it.", "你吃不完的。"),
                        line("I'm coming!", "我来了！"),
                        line("You're done?", "你吃完了？"),
                        line("You should eat fewer snacks.", "你应该少吃零食。"),
                        line("Vegetables are good for your health.", "蔬菜对你的健康有好处。"),
                        line("give too much food", "给太多食物"),
                        line("food waste", "食物浪费"),
                        line("take too much food", "拿太多食物"),
                        line("be picky about food", "挑食"),
                        line("eat snacks", "吃零食"),
                        line("rush out to play", "急着跑出去玩"),
                    ],
                },
                {
                    "heading": "Get Started · Task C",
                    "lines": [
                        line("Food waste is a big problem at our school.", "食物浪费是我们学校的一个大问题。", "Mulan"),
                        line("Yes. Sometimes the canteen staff give too much food to students.", "是的。有时候食堂工作人员给学生太多食物。", "Sam"),
                        line("Also, some students are picky about food.", "而且，有些学生挑食。", "Mulan"),
                        line("I know. Do you know what happens to our leftovers?", "我知道。你知道我们的剩饭剩菜会怎样吗？", "Sam"),
                        line("The staff usually throw it away at the end of the day.", "工作人员通常在一天结束时把它们扔掉。", "Mulan"),
                        line("We've got to do something about this!", "我们必须为这件事做点什么！", "Sam"),
                    ],
                },
                {
                    "heading": "Close Reading · Task A",
                    "lines": [
                        multi(
                            "",
                            [
                                ("There are thirty students in our class.", "我们班有三十名学生。"),
                                ("Seven said that they usually don't have enough time for breakfast.", "七名学生说他们通常没有足够时间吃早餐。"),
                                ("So, they feel hungry at noon, and they end up taking too much food.", "所以他们中午会觉得饿，最后拿了太多食物。"),
                            ],
                        ),
                        line("Three students said that sometimes the canteen staff give them too much food.", "三名学生说有时候食堂工作人员给他们太多食物。"),
                        multi(
                            "",
                            [
                                ("Ten students said that they don't like some of the food.", "十名学生说他们不喜欢某些食物。"),
                                ("So, they don't eat it.", "所以他们不吃。"),
                            ],
                        ),
                        multi(
                            "",
                            [
                                ("Six students said that they want to chat or play during lunch break.", "六名学生说他们午休时想聊天或玩耍。"),
                                ("They usually eat very little and then rush out to meet their friends.", "他们通常吃得很少，然后急着跑出去找朋友。"),
                            ],
                        ),
                        multi(
                            "",
                            [
                                ("Lastly, four students said they like to bring snacks to school.", "最后，四名学生说他们喜欢带零食到学校。"),
                                ("When it is time for lunch, they don't feel hungry at all.", "到了午餐时间，他们一点也不饿。"),
                            ],
                        ),
                    ],
                },
            ],
        },
        {
            "id": "unit-7",
            "label": "Unit 7",
            "title": "Play It Safe",
            "sections": [
                {
                    "heading": "Get Started · Task A",
                    "lines": [
                        line("don't play if you are hurt", "如果受伤了就不要参加运动"),
                        line("watch out for others on the playground", "在操场上注意其他人"),
                        line("work with your teammates", "和队友合作"),
                        line("wear the right shoes", "穿合适的鞋"),
                        line("take water breaks", "休息喝水"),
                        line("warm up", "热身"),
                        line("drink enough water", "喝足够的水"),
                        line("follow the rules", "遵守规则"),
                    ],
                },
                {
                    "heading": "Get Started · Task C",
                    "lines": [
                        line("Hey, Lucas! The game starts in five minutes.", "嘿，卢卡斯！比赛五分钟后开始。", "Yiming"),
                        line("Sorry, I overslept.", "抱歉，我睡过头了。", "Lucas"),
                        line("Did you eat breakfast? You shouldn't play when you are hungry!", "你吃早餐了吗？你饿着肚子时不应该比赛！", "Yiming"),
                        line("No, but I think I'll be okay.", "没有，但我想我会没事的。", "Lucas"),
                        line("What about your right foot? Doesn't it still hurt?", "你的右脚怎么样？它不是还疼吗？", "Yiming"),
                        line("It's okay. I got to go now.", "没事。我现在得走了。", "Lucas"),
                        line("Wait! Warm up first! You're not even wearing the right shoes, and it's raining! It's not safe.", "等等！先热身！你甚至没穿合适的鞋，而且还在下雨！这不安全。", "Yiming"),
                        line("Lucas runs away.", "卢卡斯跑开了。", "Narrator"),
                    ],
                },
                {
                    "heading": "Close Reading · Task A",
                    "lines": [
                        line("To: luiskk@mail.com", "收件人：luiskk@mail.com"),
                        line("Subject: What a bad day!", "主题：糟糕的一天！"),
                        line("Dear Luis,", "亲爱的路易斯："),
                        multi(
                            "",
                            [
                                ("I had a bad day yesterday.", "我昨天过得很糟糕。"),
                                ("In the morning, I had an important football game, but I overslept!", "早上，我有一场重要的足球比赛，但我睡过头了！"),
                                ("I ran out of the house without having breakfast.", "我没吃早餐就跑出了家门。"),
                                ("When I arrived at school, I had no time to warm up.", "当我到学校时，我没有时间热身。"),
                                ("I even wore the wrong shoes!", "我甚至穿错了鞋！"),
                                ("What's worse, it was raining!", "更糟的是，当时还在下雨！"),
                            ],
                        ),
                        multi(
                            "",
                            [
                                ("I am sure you can guess what happened next.", "我相信你能猜到接下来发生了什么。"),
                                ("I didn't watch out for others on the playground, got pushed, and fell ...", "我在操场上没有注意其他人，被推了一下，然后摔倒了……"),
                                ("And I hurt my right foot again!", "而且我的右脚又受伤了！"),
                            ],
                        ),
                        multi(
                            "",
                            [
                                ("My foot is okay.", "我的脚没事。"),
                                ("Yafei's mum was there.", "亚飞的妈妈当时在那里。"),
                                ("She is a doctor.", "她是一名医生。"),
                                ("But we lost the game.", "但我们输了比赛。"),
                            ],
                        ),
                        line("I did learn a lesson yesterday: Always get ready before sports, and be careful when you play.", "昨天我确实吸取了一个教训：运动前一定要做好准备，运动时要小心。"),
                        line("Yours,", "你的朋友，"),
                        line("Lucas", "卢卡斯"),
                    ],
                },
            ],
        },
        {
            "id": "review",
            "label": "Review",
            "title": "A Gift for Grandpa",
            "sections": [
                {
                    "heading": "Review · Task A",
                    "lines": [
                        line("Hey, guys, what do you think is a good gift? I want to get my grandpa something for his birthday.", "嘿，大家觉得什么礼物好？我想给爷爷买一份生日礼物。", "Alice"),
                        line("Well, first of all, I think it needs to carry meaning. It doesn't have to be big or cost a lot.", "嗯，首先，我认为它需要有意义。它不一定要很大，也不一定要花很多钱。", "Friend 1"),
                        multi(
                            "Friend 2",
                            [
                                ("I can't agree with you more!", "我完全同意！"),
                                ("Maybe get him something that shows your love.", "也许可以买能表达你爱意的东西。"),
                                ("Or something to help him stay healthy.", "或者买能帮助他保持健康的东西。"),
                                ("You can also get him something he really needs.", "你也可以买他真正需要的东西。"),
                            ],
                        ),
                        line("I agree. You want to show your care for him and make his life better. This way, he knows you are always thinking of him.", "我同意。你想表达对他的关心，让他的生活更好。这样，他就知道你一直想着他。", "Friend 3"),
                    ],
                }
            ],
        },
    ],
}


def main() -> None:
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    TARGET.write_text(json.dumps(DATA, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"WROTE {TARGET.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
