# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ByrbbsPipeline(object):
    def process_item(self, item, spider):
        with open('data.txt','a',encoding = 'utf-8') as f:
            if item['number'] == '楼主':
                f.write('\n\n\n\n主题：{}\n'.format(item['title']))
            f.write('-' * 10)
            f.write(
                '''\n{number}
{nickname}({author})在{time}写道：
{content}

{like}   {dislike}

'''.format(
                                number = item['number'],
                                nickname = item['nickname'],
                                author = item['author'],
                                time = item['time'],
                                content = item['content'],
                                like = item['like'],
                                dislike = item['dislike']
                                )
                )
