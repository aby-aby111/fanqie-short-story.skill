#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
番茄短故事字数统计工具（修订版）
用于检查故事是否符合平台字数要求，包括导语检查
"""

import sys
import os
import re

def count_words(text):
    """统计中文字数和总字数"""
    chinese_chars = re.findall(r'[\u4e00-\u9fff]', text)
    chinese_count = len(chinese_chars)
    total_chars = len(text)
    paragraphs = len([p for p in text.split('\n') if p.strip()])
    # 统计第一段（可能是导语）的字数
    first_para = text.split('\n')[0].strip() if text.split('\n') else ''
    chinese_first_para = len(re.findall(r'[\u4e00-\u9fff]', first_para))
    
    return {
        'chinese_words': chinese_count,
        'total_chars': total_chars,
        'paragraphs': paragraphs,
        'first_para_length': chinese_first_para
    }

def analyze_story_length(counts):
    """分析故事长度是否符合平台要求（超短故事）"""
    chinese_words = counts['chinese_words']
    
    # 超短故事要求
    requirements = {
        'min_words': 6000,        # 最低字数
        'optimal_min': 10000,     # 最佳最低字数
        'optimal_max': 25000,     # 超短故事上限
        'max_words': 80000,       # 中短故事上限
        'lead_min': 200,          # 导语最低字数
        'lead_max': 500,          # 导语最高字数
    }
    
    analysis = {
        'is_super_short': chinese_words <= 25000,
        'is_medium_short': 25000 < chinese_words <= 80000,
        'meets_minimum': chinese_words >= requirements['min_words'],
        'in_optimal_range': requirements['optimal_min'] <= chinese_words <= requirements['optimal_max'],
        'exceeds_max': chinese_words > requirements['max_words'],
        'lead_check': requirements['lead_min'] <= counts['first_para_length'] <= requirements['lead_max'],
        'word_count': chinese_words,
        'story_type': '',
        'recommendation': ''
    }
    
    # 确定故事类型
    if chinese_words <= 25000:
        analysis['story_type'] = '超短故事'
    elif chinese_words <= 80000:
        analysis['story_type'] = '中短故事'
    else:
        analysis['story_type'] = '超出范围'
    
    # 生成建议
    if chinese_words < requirements['min_words']:
        analysis['recommendation'] = '字数不足：{}字，超短故事至少{}字，中短故事至少{}字'.format(
            chinese_words, requirements['min_words'], requirements['min_words'])
    elif chinese_words > requirements['max_words']:
        analysis['recommendation'] = '字数偏多：{}字，超短故事不超过{}字，中短故事不超过{}字'.format(
            chinese_words, 25000, requirements['max_words'])
    elif requirements['optimal_min'] <= chinese_words <= requirements['optimal_max']:
        analysis['recommendation'] = '字数合适：{}字，在超短故事最佳范围{}~{}字内'.format(
            chinese_words, requirements['optimal_min'], requirements['optimal_max'])
    elif chinese_words <= 25000 and chinese_words >= requirements['min_words']:
        analysis['recommendation'] = '字数在超短故事范围内：{}字，建议扩充到{}~{}字以获取更好推荐'.format(
            chinese_words, requirements['optimal_min'], requirements['optimal_max'])
    else:
        analysis['recommendation'] = '字数在范围内：{}字'.format(chinese_words)
    
    # 导语建议
    if not analysis['lead_check']:
        if counts['first_para_length'] < requirements['lead_min']:
            analysis['lead_recommendation'] = '⚠ 第一段仅{}字，可能缺少导语。导语应为200-500字独立高能片段'.format(counts['first_para_length'])
        elif counts['first_para_length'] > requirements['lead_max']:
            analysis['lead_recommendation'] = '⚠ 第一段{}字超过导语限制（{}字），导语应控制在{}~{}字之间'.format(
                counts['first_para_length'], requirements['lead_max'], requirements['lead_min'], requirements['lead_max'])
        else:
            analysis['lead_recommendation'] = ''
    else:
        analysis['lead_recommendation'] = ''
    
    return analysis

def estimate_chapter_count(chinese_words):
    """估算分章数量"""
    return max(1, chinese_words // 1000)

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python word-count.py <文件路径>")
        print("或直接输入文本（按Ctrl+Z然后Enter结束输入）")
        print("\n请输入故事文本（按Ctrl+Z然后Enter结束）：")
        try:
            text = sys.stdin.read()
        except KeyboardInterrupt:
            print("\n已取消")
            sys.exit(1)
    else:
        file_path = sys.argv[1]
        try:
            with open(file_path, 'r') as f:
                text = f.read()
        except IOError:
            print("错误：文件不存在 - {}".format(file_path))
            sys.exit(1)
        except Exception as e:
            print("读取文件错误：{}".format(e))
            sys.exit(1)
    
    if not text.strip():
        print("错误：输入文本为空")
        sys.exit(1)
    
    counts = count_words(text)
    analysis = analyze_story_length(counts)
    chapters = estimate_chapter_count(counts['chinese_words'])
    
    print("\n" + "="*50)
    print("番茄短故事字数分析报告（修订版）")
    print("="*50)
    print("故事类型：{}".format(analysis['story_type']))
    print("中文字数：{}字".format(counts['chinese_words']))
    print("总字符数：{}字符".format(counts['total_chars']))
    print("段落数：{}段".format(counts['paragraphs']))
    print("建议分章：约{}章（每章约1000字）".format(chapters))
    
    print("\n字数检查：")
    print("✓ 最低字数要求（{}字）：{}".format(6000, '符合' if analysis['meets_minimum'] else '不符合'))
    
    if analysis['is_super_short']:
        print("✓ 超短故事范围（6000-25000字）：在范围内" if counts['chinese_words'] >= 6000 and counts['chinese_words'] <= 25000 else "⚠ 不在超短故事最佳范围")
    elif analysis['is_medium_short']:
        print("✓ 中短故事范围（25000-80000字）：在范围内" if 25000 < counts['chinese_words'] <= 80000 else "⚠ 超出中短故事范围")
    
    if counts['chinese_words'] >= 6000 and counts['chinese_words'] <= 25000:
        print("✓ 最佳字数范围（10000-25000字）：{}".format(
            '在范围内' if analysis['in_optimal_range'] else '不在范围（可扩充或精简）'))
    
    if analysis['exceeds_max']:
        print("⚠ 警告：字数超过平台最大限制（80000字）")
    
    print("\n导语检查：")
    if analysis['lead_check']:
        print("✓ 第一段{}字，符合导语要求（200-500字）".format(counts['first_para_length']))
    else:
        print(analysis.get('lead_recommendation', '⚠ 请确认是否有导语片段'))
    
    print("\n建议：{}".format(analysis['recommendation']))
    
    # 移动端阅读优化建议
    print("\n移动端阅读优化建议：")
    if counts['paragraphs'] > counts['chinese_words'] / 15:
        print("⚠ 段落过多，建议每段3-5行")
    
    avg_paragraph_length = counts['chinese_words'] / max(counts['paragraphs'], 1)
    if avg_paragraph_length > 200:
        print("⚠ 平均段落过长（{}字/段），建议拆分长段落".format(round(avg_paragraph_length, 1)))
    elif avg_paragraph_length < 30:
        print("⚠ 平均段落过短（{}字/段），适当合并相似段落".format(round(avg_paragraph_length, 1)))
    
    print("="*50)
    print("\n结构提示：番茄短故事标准结构")
    print("  导语(200-500字) → 事件展开(20%) → 冲突升级(30%) → 高潮反转(40%) → 结尾(10%)")
    print("  正文每章约1000字，每章设一个爽点/反转，章末必须有钩子")

if __name__ == "__main__":
    main()
