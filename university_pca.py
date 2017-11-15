#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import numpy as np
from matplotlib import pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

CLUSTER_NUM = 5
UNIVERSITY_DATA_FILE = 'data/university_data.csv'


def main():
    features = []
    targets = []
    f = open(UNIVERSITY_DATA_FILE)
    reader = csv.reader(f)
    for row in reader:
        #features.append(row[1:])
        features.append([row[1], row[3], row[4], row[5]])
        targets.append(row[0])
    features = np.array(features)
    targets = np.array(targets)
    f.close()

    # 標準化
    scaler = StandardScaler()
    features = scaler.fit_transform(features)

    # 主成分分析する
    pca = PCA(n_components=2, whiten=False)
    transformed = pca.fit_transform(features)

    # Kmeansでクラスタ分
    clusters = KMeans(n_clusters=CLUSTER_NUM).fit_predict(transformed)

    # 主成分をプロットする
    for label in np.unique(clusters):
        plt.scatter(transformed[clusters == label, 0],
                    transformed[clusters == label, 1])

    # クラスタごとの大学と座標
    for i in range(CLUSTER_NUM):
        print "=== CLUSTER %d ===" %(i)
        for j, t in enumerate(transformed):
            if clusters[j] == i:
                print targets[j] + t.__str__()

    # 主成分の寄与率を出力する
    print '==='
    print('各次元の寄与率: {0}'.format(pca.explained_variance_ratio_))
    print('累積寄与率: {0}'.format(sum(pca.explained_variance_ratio_)))

    # グラフを表示する
    plt.legend()
    plt.title('University PCA')
    plt.xlabel('pc1')
    plt.ylabel('pc2')
    plt.show()


if __name__ == '__main__':
    main()
