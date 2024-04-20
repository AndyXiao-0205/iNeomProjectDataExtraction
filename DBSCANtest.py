from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score
import pandas as pd
import numpy as np

# 假设你有一个包含特征的DataFrame 'df'
df = pd.read_csv('D:\\Desktop\\BUPT\\Final Project\\Otras descargas Datos\\KmeansTest2.csv')  # 或者使用其他方式加载你的数据

# 初始化DBSCAN
# eps 是两个样本被看作邻居的最大距离
# min_samples 是一个簇需要的最小样本数
dbscan = DBSCAN(eps=0.5, min_samples=5)

# 拟合模型
# dbscan.fit(df)
clusters = dbscan.fit_predict(df)

# 预测簇标号 (-1 表示噪声)
# clusters = dbscan.labels_
core_samples_mask = np.zeros_like(dbscan.labels_, dtype=bool)
core_samples_mask[dbscan.core_sample_indices_] = True
labels = dbscan.labels_
n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
n_noise = list(labels).count(-1)

# 计算轮廓系数
if n_clusters > 1:  # 轮廓系数至少需要两个簇
    silhouette_avg = silhouette_score(df[core_samples_mask], labels[core_samples_mask])
    print(f"Silhouette Coefficient: {silhouette_avg:.2f}")
# 将簇标号添加到原始数据中
df['Cluster'] = clusters

# 打印前几行查看簇标号
print(df)

# （可选）使用matplotlib来可视化聚类结果
import matplotlib.pyplot as plt

# 噪声点用不同颜色表示
plt.scatter(df.iloc[:, 0], df.iloc[:, 1], c=df['Cluster'], cmap='viridis', label='Cluster')
plt.scatter(df[df['Cluster'] == -1].iloc[:, 0], df[df['Cluster'] == -1].iloc[:, 1], c='red', label='Noise')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.title('DBSCAN Clustering')
plt.legend()
plt.show()