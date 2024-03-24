#!/usr/bin/env python
import arrow
import os
import re
import copy
import codefast as cf

import typing
import frontmatter


class PathFinder(object):
    def __init__(self, date: str, title: str) -> None:
        self.date = date
        self.title = title

    def __str__(self) -> str:
        """ Path for saving posted articles
        """
        md_name = str(self.date) + '-' + self.title.replace(' ', '-') + '.md'
        year = str(self.date).split('-')[0]
        return f'_posts/{year}/{md_name}'


class Article(object):
    def __init__(self, path: str, author: str) -> None:
        self.path = path
        self.author = author
        self.fm = frontmatter.load(path)

    @property
    def layouts(self) -> typing.Dict:
        return self.fm.metadata

    def ready_post(self) -> None:
        xpath = PathFinder(self.layouts['date'], self.layouts['title'])
        if str(self):
            with open(str(xpath), 'w') as f:
                f.write(str(self))

    @property
    def content(self) -> str:
        cs = self.fm.content
        if "{:toc}" not in cs:
            i = 0
            while i < min(len(cs), 30) or (i < len(cs) and cs[i] != '\n'):
                i += 1
            cs = cs[:i] + '\n\n\n' + cs[i:]
            return "\n* content\n{:toc}\n" + cs
        return cs

    def __str__(self):
        if self.layouts["layout"] != "post":
            return ""
        con = self.content
        con = re.sub(r'\$(.*?)\$', r'$$\1$$', con)
        con = re.sub(r'\$\$\$\$', r'$$', con)
        # Add TOC for preview

        fm_copy = copy.deepcopy(self.fm)
        fm_copy.content = ""
        return frontmatter.dumps(fm_copy) + con


class ArticleCollector(object):
    def __init__(self, workdir: str, author: str) -> None:
        self.workdir = workdir
        self.author = author

    def __enter__(self):
        year = arrow.now().format('YYYY')
        target_dir = f'_posts/{year}'
        if not cf.io.exists(target_dir):
            os.makedirs(target_dir)
        for root, subdirs, files in os.walk('_posts'):
            if len(subdirs) == 0:
                for f in files:
                    full_path = f'{root}/{f}'
                    if os.path.isfile(full_path) and full_path.endswith('.md'):
                        os.system(f'unlink {full_path}')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def update(self):
        for root, subdirs, files in os.walk(self.workdir):
            if len(subdirs) == 0:
                for f in files:
                    full_path = f'{root}/{f}'
                    if os.path.isfile(full_path) and full_path.endswith('.md'):
                        artciel = Article(full_path, self.author)
                        artciel.ready_post()


class ProgressTracker(object):
    def __init__(self) -> None:
        self._logs = cf.lis(cf.js('assets/progress.json')) if cf.io.exists(
            'assets/progress.json') else cf.lis([('1970-01-01', 0)])

    def count_cn(self, md_file: str) -> int:
        """Count Chinese Character"""
        with open(md_file, 'r') as f:
            return len(re.findall(r'[\u4e00-\u9fa5]', f.read()))

    def run(self):
        sm = sum(cf.lis(cf.io.walk('_drafts', depth=6)).map(self.count_cn).data)
        today = arrow.now().format('YYYY-MM-DD')
        self._logs.sort()
        if self._logs[-1][0] == today:
            presum = sum([v for _, v in self._logs.data[:-1]])
            self._logs[-1] = (today, sm - presum)
        else:
            self._logs.print()
            presum = sum([v for _, v in self._logs.data])
            self._logs.append([today, sm-presum])
        self._logs.print()
        cf.js.write(self._logs.data, 'assets/progress.json')


if __name__ == "__main__":
    with ArticleCollector('_drafts', 'ultrasev') as ac:
        ac.update()
    ProgressTracker().run()
