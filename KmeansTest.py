from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
import pandas as pd

# 假设你有一个包含特征的DataFrame 'df'
df = pd.read_csv('D:\\Desktop\\BUPT\\Final Project\\Otras descargas Datos\\KmeansTest4.csv')  # 或者使用其他方式加载你的数据

# 选择聚类的数量
num_clusters = 3

# 初始化KMeans
kmeans = KMeans(n_clusters=num_clusters, random_state=0)

# 拟合模型
kmeans.fit(df)

# 预测每个样本的簇标号
clusters = kmeans.predict(df)

# 将簇标号添加到原始数据中
df['Cluster'] = clusters
silhouette_avg = silhouette_score(df, clusters)
# 打印前几行查看簇标号


# （可选）使用matplotlib来可视化聚类结果
import matplotlib.pyplot as plt

plt.scatter(df.iloc[:, 0], df.iloc[:, 1], c=df['Cluster'], cmap='viridis')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.title('KMeans Clustering')
plt.show()


clusters = kmeans.labels_

# 轮廓系数评估

print(f'Silhouette Coefficient: {silhouette_avg:.2f}')

# 肘部法则评估
wcss = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, init='k-means++', max_iter=400, n_init=20, random_state=42).fit(df)
    wcss.append(kmeans.inertia_)

# 绘制肘部图
plt.figure(figsize=(10, 8))
plt.plot(range(1, 11), wcss, marker='o', linestyle='--')
plt.title('Elbow Method For Optimal k')
plt.xlabel('Number of Clusters')
plt.ylabel('WCSS')
plt.show()
