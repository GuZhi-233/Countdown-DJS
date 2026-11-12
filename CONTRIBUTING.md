# 贡献指南

感谢你愿意为倒计时·DJS 提供帮助。提交 Issue 或 Pull Request 前，请先阅读以下约定。

## 反馈问题

请优先使用 Gitee Issues：

https://gitee.com/guzhi233/countdown---djs/issues

也可以在 GitHub Issues 提交：

https://github.com/GuZhi-233/Countdown-DJS/issues

Bug 反馈请尽量包含：

- 主程序版本与构建号（设置 → 关于 / 版本信息）
- Windows 版本
- 复现步骤
- 预期结果与实际结果
- `data/LOG.txt` 中的相关日志
- 是否启用了插件系统、是否使用了动态背景或全屏

## 开发环境

- Python 3.10+
- Windows 10 / 11
- 依赖：`pip install -r requirements.txt`

从源码运行：

```bash
python src/djs_pyqt6.py
```

请从仓库根目录运行，程序会读取根目录的 `data` 并自动创建 `plugins`。

## 代码约定

- 主程序保持单文件结构，暂不拆分模块。
- 代码保持简洁，不添加解释性注释。
- 新增界面必须同时适配深色与浅色主题。
- 修改配置结构时同步编写迁移逻辑，并升级配置版本。
- 修改用户可见功能时同步更新程序内帮助与 `CHANGELOG.md`。
- 版本号统一通过 `python tools/bump_version.py <版本>` 修改，不要手工改两处常量。

## 插件与远控

ZX 插件、Windows / Android 远控控制台位于附属仓库：

https://github.com/GuZhi-233/Countdown-DJS-Addons

插件相关的 Issue 与 PR 请提交到该仓库。

## Pull Request

- 一个 PR 只做一件事，避免混合无关改动。
- 说明改动目的、影响范围与测试方式。
- 涉及界面时附上深色与浅色截图。
- 涉及插件 API 或清单结构时，在 PR 中注明插件作者是否需要调整。
- 提交前至少执行一次：

```bash
python -m py_compile src/djs_pyqt6.py
```
