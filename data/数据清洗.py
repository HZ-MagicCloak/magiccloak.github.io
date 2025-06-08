import pandas as pd
from collections import Counter

# 读取Excel数据
df = pd.read_excel('体育场馆数据.xlsx')

# 1. 合并处理体育类型列
sports_cols = ['体育类型1', '体育类型2', '体育类型3', '体育类型4', '体育类型5', '体育类型6']
df['体育类型列表'] = df[sports_cols].apply(
    lambda row: [sport for cell in row if pd.notna(cell) for sport in str(cell).split()],
    axis=1
)

# 2. 统计每个场馆的项目数量
df['场馆项目数量'] = df['体育类型列表'].apply(len)

# 3. 统计每种体育类型总频次
all_sports = [sport for sublist in df['体育类型列表'] for sport in sublist]
sport_freq = pd.Series(Counter(all_sports)).sort_values(ascending=False).reset_index()
sport_freq.columns = ['体育类型', '总频次']

# 4. 统计每个城市的体育馆数量（新增）
city_stadium_count = df.groupby('所在城市').size().reset_index(name='体育馆数量')

# 5. 统计每个城市的体育类型数量
city_sports = df.groupby('所在城市')['体育类型列表'].sum().apply(lambda sports: len(set(sports)))
city_sports = city_sports.reset_index(name='体育类型数量')

# 6. 创建带场馆列表的城市统计
city_sports_detail = df.groupby('所在城市')['体育类型列表'].agg(
    lambda x: set([item for sublist in x for item in sublist]))
city_sports_detail = city_sports_detail.reset_index()
city_sports_detail.columns = ['所在城市', '体育类型集合']
city_sports_detail['体育类型数量'] = city_sports_detail['体育类型集合'].apply(len)
city_sports_detail = city_sports_detail[['所在城市', '体育类型数量', '体育类型集合']]

# 7. 创建带场馆数量的体育类型统计
sport_venues = {}
for sport in sport_freq['体育类型']:
    count = df[df['体育类型列表'].apply(lambda x: sport in x)].shape[0]
    sport_venues[sport] = count
sport_venues_df = pd.DataFrame({
    '体育类型': sport_venues.keys(),
    '覆盖场馆数': sport_venues.values()
}).sort_values('覆盖场馆数', ascending=False)

# 8. 合并城市统计信息（新增）
city_stats = pd.merge(city_sports, city_stadium_count, on='所在城市')

# 将结果保存到Excel的不同工作表
with pd.ExcelWriter('体育场馆统计结果.xlsx') as writer:
    # 原始数据添加新列
    df.to_excel(writer, sheet_name='原始数据(带新列)', index=False)

    # 场馆项目数量统计
    venue_counts = df[['场馆', '所在城市', '场馆项目数量', '体育类型列表']]
    venue_counts.to_excel(writer, sheet_name='场馆项目数量', index=False)

    # 体育类型频次统计
    sport_freq.to_excel(writer, sheet_name='体育类型频次', index=False)

    # 城市体育馆数量统计（新增）
    city_stadium_count.to_excel(writer, sheet_name='城市体育馆数量', index=False)

    # 城市体育类型数量统计
    city_sports.to_excel(writer, sheet_name='城市体育类型数量', index=False)

    # 城市综合统计（新增）
    city_stats.to_excel(writer, sheet_name='城市综合统计', index=False)

    # 城市详细统计
    city_sports_detail.to_excel(writer, sheet_name='城市体育类型详情', index=False)

    # 体育类型场馆覆盖统计
    sport_venues_df.to_excel(writer, sheet_name='体育类型覆盖场馆', index=False)

print("数据统计完成，结果已保存到 '体育场馆统计结果.xlsx'")