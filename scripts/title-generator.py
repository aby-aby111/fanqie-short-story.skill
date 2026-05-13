#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
番茄短故事标题生成工具
根据热门题材和爆款模式生成吸引眼球的标题
"""

import random
import sys
import json

class TitleGenerator:
    def __init__(self):
        # 标题模板库（基于番茄爆款标题分析）
        self.templates = {
            # 虐恋类标题模板
            'tragic_love': [
                "离婚那天，{character}在民政局外跪了一夜",
                "我死后第三年，{character}终于疯了",
                "{character}的白月光回国那天，我确诊了癌症晚期",
                "婚礼前夜，我发现{character}有个私生子",
                "重生后，我嫁给了{character}的死对头",
                "{character}为了救白月光，抽干了我的血",
            ],
            
            # 悬疑推理类标题模板
            'mystery': [
                "接到报警电话时，凶手正站在我身后",
                "地下室发现一具女尸，竟是我失踪三年的妹妹",
                "新搬来的邻居每天半夜敲墙，直到我在墙里发现...",
                "算命先生说我会死于非命，第二天我就收到了死亡预告",
                "直播算命连线到杀人犯，他问我：下一个轮到谁？",
            ],
            
            # 重生复仇类标题模板
            'reborn_revenge': [
                "重生回到被陷害那天，我反手举报了所有人",
                "穿越成恶毒女配，我直接摆烂了",
                "死后我重生成了仇人的女儿",
                "系统让我攻略反派，我直接把他送进了监狱",
                "重生后，我抢走了姐姐的豪门婚事",
            ],
            
            # 甜宠爽文类标题模板
            'sweet_romance': [
                "相亲对象是暗恋十年的男神",
                "捡到的流浪猫变成了霸总",
                "和死对头协议结婚后，他真香了",
                "上司是我网恋三年的游戏CP",
                "被迫和商业联姻对象同居后，他宠我上天",
            ],
            
            # 现实题材类标题模板
            'realistic': [
                "35岁被裁员后，我开网约车月入五万",
                "陪女儿考研，我考上了985",
                "辞职回农村种地，年入百万",
                "离婚后带着孩子创业，前夫后悔了",
                "老公出轨后，我成了公司总裁",
            ]
        }
        
        # 人物名称库
        self.characters = [
            "总裁", "前夫", "男友", "老公", "上司", "学长", 
            "竹马", "初恋", "白月光", "死对头", "反派",
            "陆霆", "沈清", "顾衍", "苏晚", "林墨", "江辰"
        ]
        
        # 情感关键词
        self.emotion_words = [
            "跪了一夜", "疯了", "确诊癌症", "私生子", "抽干血",
            "反手举报", "直接摆烂", "送进监狱", "真香了", "宠上天",
            "后悔了", "月入五万", "考上985", "年入百万"
        ]
        
        # 数字关键词（增加点击率）
        self.number_words = [
            "三年", "五年", "十年", "三天", "一夜", 
            "第100天", "35岁", "第3年", "第二天", "第三次"
        ]
    
    def generate_title(self, genre=None, custom_character=None):
        """生成标题"""
        if genre is None:
            genre = random.choice(list(self.templates.keys()))
        
        if genre not in self.templates:
            available = ", ".join(self.templates.keys())
            raise ValueError("未知题材类型。可用类型：{}".format(available))
        
        # 选择模板
        template = random.choice(self.templates[genre])
        
        # 替换人物
        character = custom_character if custom_character else random.choice(self.characters)
        title = template.format(character=character)
        
        # 50%概率添加数字前缀
        if random.random() > 0.5:
            number = random.choice(self.number_words)
            title = "{}，{}".format(number, title)
        
        # 30%概率添加情感后缀
        if random.random() > 0.7:
            emotion = random.choice(self.emotion_words)
            title = "{}，{}".format(title, emotion)
        
        return {
            'title': title,
            'genre': genre,
            'character': character,
            'length': len(title)
        }
    
    def generate_multiple_titles(self, count=5, genre=None):
        """生成多个标题"""
        titles = []
        for _ in range(count):
            title_data = self.generate_title(genre)
            titles.append(title_data)
        return titles
    
    def analyze_title(self, title):
        """分析标题质量"""
        analysis = {
            'length': len(title),
            'has_number': any(word in title for word in self.number_words),
            'has_emotion': any(word in title for word in self.emotion_words),
            'has_character': any(char in title for char in self.characters),
            'score': 0,
            'recommendations': []
        }
        
        # 评分规则
        if 8 <= analysis['length'] <= 15:
            analysis['score'] += 30
        elif analysis['length'] < 8:
            analysis['score'] += 20
            analysis['recommendations'].append("标题偏短，建议增加细节")
        else:
            analysis['score'] += 10
            analysis['recommendations'].append("标题偏长，建议精简")
        
        if analysis['has_number']:
            analysis['score'] += 25
        else:
            analysis['recommendations'].append("考虑添加数字元素增加点击率")
        
        if analysis['has_emotion']:
            analysis['score'] += 25
        else:
            analysis['recommendations'].append("考虑添加情感关键词")
        
        if analysis['has_character']:
            analysis['score'] += 20
        else:
            analysis['recommendations'].append("考虑明确人物身份")
        
        # 评估等级
        if analysis['score'] >= 80:
            analysis['grade'] = "优秀"
        elif analysis['score'] >= 60:
            analysis['grade'] = "良好"
        else:
            analysis['grade'] = "需要优化"
        
        return analysis

def main():
    """主函数"""
    generator = TitleGenerator()
    
    print("番茄短故事标题生成工具")
    print("="*50)
    
    # 显示可用题材
    print("可用题材类型：")
    for i, genre in enumerate(generator.templates.keys(), 1):
        print(f"  {i}. {genre}")
    
    # 获取用户选择
    try:
        choice = input("\n请选择题材类型（输入编号或直接按Enter随机生成）：").strip()
        
        genre_map = {str(i+1): genre for i, genre in enumerate(generator.templates.keys())}
        selected_genre = None
        
        if choice in genre_map:
            selected_genre = genre_map[choice]
            print(f"已选择题材：{selected_genre}")
        elif choice == "":
            print("将随机生成标题")
        else:
            if choice in generator.templates:
                selected_genre = choice
            else:
                print(f"未知类型，将随机生成")
        
        # 生成标题数量
        count_input = input("生成标题数量（默认5个）：").strip()
        count = int(count_input) if count_input.isdigit() else 5
        
        # 生成标题
        print(f"\n生成{count}个标题：")
        print("-"*30)
        
        titles = generator.generate_multiple_titles(count, selected_genre)
        
        for i, title_data in enumerate(titles, 1):
            analysis = generator.analyze_title(title_data['title'])
            print(f"{i}. {title_data['title']}")
            print(f"   题材：{title_data['genre']} | 长度：{title_data['length']}字 | 评分：{analysis['score']}/100 ({analysis['grade']})")
            
            if analysis['recommendations']:
                print(f"   建议：{'；'.join(analysis['recommendations'][:2])}")
            print()
        
        # 分析模式
        print("-"*30)
        analyze_choice = input("是否分析现有标题？(y/n)：").strip().lower()
        
        if analyze_choice == 'y':
            title_to_analyze = input("请输入要分析的标题：").strip()
            if title_to_analyze:
                analysis = generator.analyze_title(title_to_analyze)
                print(f"\n标题分析结果：")
                print(f"长度：{analysis['length']}字")
                print(f"包含数字：{'是' if analysis['has_number'] else '否'}")
                print(f"包含情感词：{'是' if analysis['has_emotion'] else '否'}")
                print(f"包含人物：{'是' if analysis['has_character'] else '否'}")
                print(f"综合评分：{analysis['score']}/100 ({analysis['grade']})")
                
                if analysis['recommendations']:
                    print("优化建议：")
                    for rec in analysis['recommendations']:
                        print(f"  • {rec}")
        
        print("\n标题创作技巧：")
        print("1. 使用数字增加真实感和紧迫感")
        print("2. 明确人物身份和关系")
        print("3. 加入强烈情感冲突")
        print("4. 控制在8-15字最佳阅读长度")
        print("5. 制造悬念和好奇心")
        
    except KeyboardInterrupt:
        print("\n\n已取消")
    except Exception as e:
        print(f"错误：{e}")

if __name__ == "__main__":
    main()