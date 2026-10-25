# 看懂投资：从一笔钱到整个市场

面向普通读者的中文投资基础图解。六篇、24章，另含导读与判断工具附录。正文按章分文件，配24幅原创教学SVG。数字为明示的假设案例，不是行情预测或个性化买卖建议。

## 阅读顺序

见 `CONTENTS.md` 与 `book.json`。顺序为钱与投资→资产→交易机制→公司与估值→市场变化→个人投资方法。各章保留本章来源链接。制度核验日期见正文；`references/source-index.json` 汇总64个外部链接，分组记录保留资料出处。

## 工程结构

- `chapters/`：24章可编辑Markdown主稿。
- `appendices/`：导读、判断表和词汇。
- `assets/images/`：SVG教学图及封面。
- `references/`：一手资料记录与引用索引。
- `editorial/`：覆盖表、图片审查索引、六篇交叉审稿报告与修订记录，不并入读者版。
- `scripts/`：绘图重建、内容检查与EPUB构建。
- `build/`：生成产物，不入Git。网站构建产物；不入 Git。首页、目录、搜索和阅读页从同一份 `book.json` 与正文生成。

## 构建

需要Python 3.10+、Pillow、Pandoc 3.x、Inkscape，以及可显示中文的字体（建议Noto Serif CJK SC）。SVG按720像素视口设计，PNG导出宽1080像素。

```bash
python scripts/build_book.py --check
python scripts/build_book.py
```

产物为 `build/Investment-From-Money-to-Markets.epub`；每幅SVG先渲染为PNG，并验证可解码后嵌入，以提高阅读器兼容性。构建同时验证本地链接、SVG结构、章数及嵌入图片数量。

重建教学图：

```bash
python scripts/figures_part1.py
python scripts/figures_part2.py
python scripts/figures_part3.py
python scripts/figures_part4.py
python scripts/figures_part5.py
python scripts/figures_part6.py
```

重建封面可运行 `python scripts/make_cover.py`，也可通过环境变量 `BOOK_CJK_FONT` 指定本机字体文件；不需要重建封面即可构建EPUB。

## 版本管理

根提交仅含零字节README，随后依次提交规划、分章与插图、审校与构建。工程包中 `history.bundle` 保存完整提交历史，可用 `git clone history.bundle investment-foundations` 恢复。原始提交通过 `history.bundle` 完整保留；GitHub 上按原有阶段导入书稿，再加入网站与发布配置。

## 在线阅读与自动发布

- [在线阅读](https://yzyexp.github.io/Learn-Invest/)
- [网页发布状态](https://github.com/YZYExp/Learn-Invest/actions/workflows/pages.yml)
- [EPUB 导出与产物](https://github.com/YZYExp/Learn-Invest/actions/workflows/epub.yml)

网页仅需 Python 与 Markdown，不安装整书导出工具。

```bash
python -m pip install -r site/requirements.txt
python scripts/build_site.py --base-path /Learn-Invest/
```

输出 `build/site/`，含独立首页、26 个阅读单元、目录全文搜索、字号调整和图片放大。可用 `python -m http.server --directory build/site` 从站点根目录预览，此时请先以 `--base-path /` 构建。

`main` 更新后自动检查和部署；PR 仅构建检查。首次发布需在仓库 **Settings → Pages → Source** 选择 **GitHub Actions**。网页发布与 EPUB 分为独立流程，导出失败不会阻塞网页。EPUB 产物需 GitHub 登录下载，保留 90 天；可手动重新导出。
