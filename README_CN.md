# 🎮 GamePlayVideoMaker —— 基于 Gameplay 背景的短视频自动生成工具

> **给我一段讲解文案，我帮你自动生成一条短视频。**  
> *Gameplay 只是背景，内容靠语音与配图。*

GamePlayVideoMaker 是一个 **面向 TikTok / Shorts / B 站短视频创作的自动化视频生成工具**，  
专门用于制作一种非常常见、但制作成本高的短视频形式：

> **“Gameplay 作为动态背景 + TTS 语音讲解 + 配图辅助说明”**

⚠️ **重要说明**：  
- Gameplay **仅作为视觉背景**  
- 视频讲解内容 **与游戏本身完全无关**

---

## 🎥 这个工具是做什么的？

GamePlayVideoMaker 用来自动生成以下类型的视频：

- 技术 / AI / 编程 / 知识讲解
- 观点输出 / 解说 / 旁白
- 故事型口播内容
- 教育类短视频
- Shorts / TikTok 常见“背景跑酷 + 讲解”风格视频

其核心思想是：

> **用 Gameplay 提供“动态画面与停留率”，  
> 用语音和配图承载真正的信息。**

---

## 🎬 输入与输出

**输入：**
- 讲解脚本（文本）
- 可选配图 / 示意图
- 一段 gameplay 视频（作为背景）

**输出：**
- 一条可直接发布的短视频
- 支持：
  - 9:16（TikTok / Shorts）
  - 16:9（B 站 / YouTube）

---

## 🧠 核心特性

- 🎮 Gameplay 背景裁剪 / 循环 / 适配比例
- 🎙️ 高质量 TTS 语音生成（支持多角色）
- 🖼️ 图片 / 示意图按脚本自动叠加
- 📝 自动生成并对齐字幕
- 🔊 音频自动混音与响度归一化
- 📐 横屏 / 竖屏一键切换
- 🔁 基于 JSON 的流水线，可单段重生成
- ⚙️ 支持批量自动化生产

---

## 🚀 项目目标

GamePlayVideoMaker 的目标非常简单：

> **把 Shorts / TT 常见的“讲解 + 游戏背景”视频生产流程彻底自动化。**

你只需要负责：

- 写讲解内容  
- 选一个 gameplay 当背景  

剩下的全部交给系统完成：

1. TTS 语音生成  
2. Gameplay 背景处理  
3. 配图叠加  
4. 字幕生成与时间轴对齐  
5. 视频合成与导出  

非常适合：

- 短视频创作者
- 知识型账号
- 教育内容自动化
- 批量内容生产

---

## 🖥️ Web 界面（Gradio）

![UI Screenshot](example/picture/ui1.png)

启动方式：

```bash
python videogen/gradio_app.py
````

环境变量配置：

复制 `.env_example` → `.env`，并填写所需的 API Key。

---

## 🤖 使用的模型与组件

* **TTS（语音合成）：** GPT-SoVITS（支持自定义音色）
* **LLM（脚本解析 / 时间轴规划）：** DeepSeek-V3
* **视频处理：** MoviePy / FFmpeg
* **Web UI：** Gradio

> Gameplay 视频由用户自行提供，本工具 **不生成游戏画面**。

---

## 📺 内容声明（B 站）

以下 B 站账号中的 **大部分视频内容**，均由 **GamePlayVideoMaker** 自动生成：

🔗 [https://space.bilibili.com/109455236](https://space.bilibili.com/109455236)
