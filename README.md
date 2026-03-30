<h1 align="center">MindStudio Ops Generator</h1>

<div align="center">
<h2>昇腾 AI 算子工程工具</h2>

 [![Ascend](https://img.shields.io/badge/Community-MindStudio-blue.svg)](https://www.hiascend.com/developer/software/mindstudio) 
 [![License](https://badgen.net/badge/License/MulanPSL-2.0/blue)](./docs/LICENSE)

</div>

## ✨ 最新消息

* [2026.2.10]：msOpGen适配AscendC算子新工程
* [2025.12.30]：MindStudio Ops Generator项目首次上线

## ℹ️ 简介

MindStudio Ops Generator（算子工程创建，msOpGen）是算子开发效率提升工具，提供模板工程生成能力，简化算子工程搭建并辅助算子测试验证。完成算子分析和原型定义后，可使用msOpGen工具生成自定义算子工程。使用msOpGen工具完成自定义算子包部署后，可选择使用MindStudio Ops System Test（算子测试，msOpST）工具进行ST（System Test）测试，在真实的硬件环境中，对算子的输入输出进行测试，以验证算子的功能是否正确。

## ⚙️ 功能介绍

- msOpGen目前已支持的功能如下：包括算子工程创建、算子实现（Host侧&Kernel侧）、算子工程编译部署以及解析算子仿真流水图文件等。

| 功能 | 使用说明  |
|---------|--------|
| [算子工程创建](./docs/zh/msopgen_user_guide.md#创建算子工程) |按照步骤执行创建算子工程 |
|[算子实现（Host侧&Kernel侧）](./docs/zh/msopgen_user_guide.md#算子开发)   | 按照步骤执行完成算子开发实现 |
| [算子工程编译部署](./docs/zh/msopgen_user_guide.md#算子编译部署)   | 完成算子Kernel、Host侧的开发后，需要对算子工程进行编译，生成自定义算子安装包*.run |
|  [解析算子仿真流水图文件](./docs/zh/msopgen_user_guide.md#查看算子仿真流水图) | msOpGen工具通过解析用户生成的dump文件，并生成算子仿真流水图文件（trace.json）|

- msOpST支持生成算子的ST测试用例并在硬件环境中执行。具有如下功能：

| 功能 | 使用说明  |
|---------|--------|
| [生成测试用例定义文件](./docs/zh/msopgen_user_guide.md#生成测试用例定义文件) |根据用户定义并配置的算子期望数据生成函数，回显期望算子输出和实际算子输出的对比测试结果 |
| [生成并执行测试用例](./docs/zh/msopgen_user_guide.md#生成执行测试用例)   | 根据算子测试用例定义文件生成ST测试数据及测试用例执行代码，在硬件环境上执行算子测试用例，自动生成运行报表（st_report.json）功能，报表记录了测试用例信息及各阶段运行情况 |
| [生成单算子上板测试框架](./docs/zh/msopgen_user_guide.md#生成单算子上板测试框架)  | 自动生成算子调用核函数的上板测试框架，进行算子的测试验证|

## 🚀 快速入门

详细操作步骤请参见[msOpGen 快速入门](./docs/zh/quick_start/msopgen_quick_start.md)和[msOpSt 快速入门](./docs/zh/msopst_quick_start.md)。

## 📦 安装指南

介绍msOpGen工具的环境依赖及安装方式，具体请参见[MindStudio Ops Generator 安装指南](./docs/zh/msopgen_install_guide.md)。

## 📘 使用指南

工具的详细使用方法，请参见 [MindStudio Ops Generator 使用指南](./docs/zh/msopgen_user_guide.md)

## 💡 典型案例

msOpGen工具通过一些典型案例帮助用户理解并熟悉工具，具体案例请参见[MindStudio Ops Generator典型案例](./docs/zh/example.md)。

## 🛠️ 贡献指南

若您有意参与项目贡献，请参见 [《贡献指南》](./docs/zh/contributing/contributing_guide.md)。 

## ⚖️ 相关说明

* [《版本说明》](./docs/zh/release_notes/release_notes.md) 
* [《License声明》](./docs/zh/legal/license_notice.md) 
* [《安全声明》](./docs/zh/legal/security_statement.md) 
* [《免责声明》](./docs/zh/legal/disclaimer.md)

## 🤝 建议与交流

欢迎大家为社区做贡献。如果有任何疑问或建议，请提交[Issues](https://gitcode.com/Ascend/msopgen/issues)，我们会尽快回复。感谢您的支持。

## 🙏 致谢

msOpGen由华为公司的下列部门联合贡献：

- 计算产品线

感谢来自社区的每一个PR，欢迎贡献msOpGen。
