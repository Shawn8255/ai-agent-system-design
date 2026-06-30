# AI Agent 系统设计

从经典计算机工程到现代智能体架构 - 第一部分：前三章完整版

*Working Draft v0.2 - 2026-06-29*

## 前言

这份文档不是一份 Agent API 使用手册，也不是一次聊天记录整理。它试图从软件工程师和分布式系统架构师的角度，解释为什么现代 AI Agent 的架构越来越像经典计算机系统。

本文的基本观点是：LLM 是最近几年 AI 的核心突破，但当 LLM 被放进真实产品和真实工作流之后，很多问题又重新回到了计算机工程最熟悉的领域：如何管理状态、如何降低远程调用成本、如何做缓存和索引、如何保持服务无状态、如何在多个计算资源之间调度。

第一部分先完成前三章：第 1 章建立整体视角；第 2 章把 LLM 放回“计算引擎”的位置；第 3 章说明 Agent 为什么更像 Orchestrator，而不是简单的聊天机器人。

> 核心主线：LLM 是新的 Compute Engine，Agent 是围绕它进行上下文管理、工具调用、状态恢复和资源调度的 Orchestrator。

## 目录大纲

| 章节 | 标题 | 状态 |
| --- | --- | --- |
| 第 1 章 | 为什么 AI Agent 让我想到了经典计算机工程 | 已完成 |
| 第 2 章 | LLM：一种新的 Compute Engine | 已完成 |
| 第 3 章 | Agent：为什么它更像 Orchestrator | 已完成 |
| 第 4 章 | Memory、Tool 与 Planner 在 Agent 中的职责 | 后续 |
| 第 5 章 | Compute / Storage Separation 在 AI 中的体现 | 后续 |
| 第 6 章 | Stateless Agent 与微服务设计 | 后续 |
| 第 7 章 | Context Engineering 与 Query Optimization | 后续 |
| 第 8 章 | AGENTS.md 与 Prompt Index | 后续 |
| 第 9 章 | RAG、Retrieval 与 Context Routing | 后续 |
| 第 10 章 | Distillation、Small Model 与 Tiered Compute | 后续 |
| 第 11 章 | Multi-Agent 与分布式系统 | 后续 |
| 第 12 章 | 未来方向：Agent Operating System | 后续 |

## 术语约定

| 术语 | 本文中的含义 | 工程类比 |
| --- | --- | --- |
| LLM | 大语言模型，负责推理计算 | Compute Engine |
| Agent | 围绕 LLM 组织 Memory、Tool、Planner、Context 的系统层 | Orchestrator / Runtime |
| Memory | 长期保存的用户偏好、项目背景和任务状态 | Database / Cache |
| Context | 本次请求真正送入模型的工作集 | Working Set / Buffer Pool |
| Tool | Agent 可调用的外部能力，例如文件、邮件、日历、GitHub、Shell | RPC / API |
| Distillation | 把大模型能力迁移到小模型或固定工作流 | Precomputation / Tiered Compute |

![图 1](assets/figure-01.png)

图 1：AI Agent 的讨论正在从模型中心转向系统中心
