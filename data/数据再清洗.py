import pandas as pd
import json

# 读取Excel文件
df = pd.read_excel('体育场馆统计结果.xlsx')

# 选择需要的列并重命名
df = df[['所在城市', '场馆', '场馆项目数量']].rename(columns={
    '所在城市': 'city',
    '场馆': 'venue',
    '场馆项目数量': 'typesCount'
})

# 按城市分组并转换为所需格式
cities_data = []
for city, group in df.groupby('city'):
    venues_list = []
    for _, row in group.iterrows():
        # 跳过无效数据（项目数量为0或NaN）
        if pd.notna(row['typesCount']) and row['typesCount'] > 0:
            venues_list.append({
                "name": row['venue'],
                "typesCount": int(row['typesCount'])
            })

    if venues_list:  # 只添加有场馆的城市
        cities_data.append({
            "name": city,
            "venues": venues_list
        })

# 转换为JavaScript格式字符串
js_output = "const citiesData = [\n"
for city in cities_data:
    js_output += "    {\n"
    js_output += f'        name: "{city["name"]}",\n'
    js_output += "        venues: [\n"

    for venue in city["venues"]:
        js_output += f'            {{name: "{venue["name"]}", typesCount: {venue["typesCount"]}}},\n'

    js_output += "        ]\n"
    js_output += "    },\n"
js_output += "];"

# 保存到文件或打印输出
with open('体育馆新格式数据.js', 'w', encoding='utf-8') as f:
    f.write(js_output)

print("JavaScript数据已保存到体育馆新格式数据.js文件")