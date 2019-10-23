#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2019/10/16 17:24
# @Author: yanmiexingkong
# @email : yanmiexingkong@gmail.com
# @File  : bios.py

# python 3.7
# pip install requests, pyquery
import time

import requests
from pyquery import PyQuery as pq


class Bios():
    def __init__(self, url, wild_path, mutation_list_path):
        """
        :param url: 稳定性预测表的请求地址
        :param wild_path: wild 文件的路径
        :param mutation_list_path: mutation_list_path 文件的路径
        """
        self.url = url
        self.files = {
            'wild': open(wild_path),
            'mutation_list': open(mutation_list_path)
        }
        self.html = None
        self.result = {}

    def run(self):
        """
        requests 模拟请求：传入 wild 文件、mutation_list 文件
        解析返回的 html，并使用 self.extract_result 提取预测结果
        :return: 预测结果
        """
        r = requests.post(self.url, files=self.files)
        if r.status_code == 200:
            self.html = r.text
            self.extract_result()
            return self.result
        else:
            print('访问错误！！！')
            raise

    def extract_result(self):
        """
        从 html 中提取预测结果，存放到 self.result
        """
        doc = pq(self.html)
        index_1 = doc.find('tbody tr:nth-child(1) td')
        index_2 = doc.find('tbody tr:nth-child(2) td')

        title_list = ['Index', 'PDB File', 'Chain', 'Wild Residue', 'Residue Position', 'Mutant Residue', 'RSA (%)',
                      'Predicted ΔΔG', 'Outcome']
        result_1 = {}
        result_2 = {}
        for i in range(9):
            result_1.update({title_list[i]: index_1[i].text.strip()})
            result_2.update({title_list[i]: index_2[i].text.strip()})

        self.result.update({
            '1': result_1,
            '2': result_2
        })


if __name__ == '__main__':
    start_time = time.time()  # 记录程序运行开始时间

    url = 'http://biosig.unimelb.edu.au/mcsm/prot_dna_prediction_list'
    wild = 'files/3ngb.pdb'
    mutation_list = 'files/test.txt'
    result = Bios(url=url, wild_path=wild, mutation_list_path=mutation_list).run()
    print(result)

    end_time = time.time()  # 记录程序运行结束时间
    spend_time = end_time - start_time
    print('运行时间: ', spend_time)
