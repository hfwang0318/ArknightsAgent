# ArknightsAgent(明日方舟自动代理)
整合了图像识别模块的自动代理脚本。支持多任务队列，自动使用理智合剂和源石等功能的便利代理。

# Notice
* **本脚本使用 MuMu 模拟器作为默认模拟器，使用前请将模拟器的分辨率设置为 1600*900。**
* 使用前需要先安装 Tesseract 框架和下载模型数据，将 Tesseract 根目录加入到环境变量，将模型数据放在脚本根目录。<br>
Tesseract 5.0：<br>
[tesseract-ocr-w32-setup-v5.0.0-alpha.20190708.exe](https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w32-setup-v5.0.0-alpha.20190708.exe)<br>
模型数据：<br>
[chi_sim.traineddata](https://github.com/tesseract-ocr/tessdata/raw/master/chi_sim.traineddata)<br>
以上链接引用自：<br>
[UB-Mannheim/tesseract](https://github.com/UB-Mannheim/tesseract/wiki)<br>
[tesseract-ocr/tessdata](https://github.com/tesseract-ocr/tessdata)<br>
* 请预先下载 `adb` 工具，并加入到环境变量。（MuMu 模拟器自带的 adb 位于根目录/emulator/nemu/vmonitor/bin/adb_server.exe，若使用 MuMu 自带的 adb 请将 `adb_server` 重命名为 `adb`）
* 若需要使用其他模拟器，请自行指定模拟器占用端口。<br>
`--local-host[-l] 127.0.0.1:port`

# Requirements
`Numpy`<br>
`OpenCV2`<br>
可以通过执行`pip install -r requirements.txt`快速安装所有依赖。

# Usage
## Base
打开模拟器先进入游戏任意页面（请保证左上角有主页按钮，即不能在`设置`等页面启用脚本）。<br>
cmd cd 到脚本根目录输入 `python main.py -m OF-8,2`, 脚本将开始运行。<br>
`-m OF-8,2`是指打 OF-8 关卡 2 次。<br>

## Details
脚本支持的所有参数如下：<br>
`--missions[-m] mission_name,times` 输入关卡名和需要代理的次数，中间用`,`隔开。可支持多任务。当代理次数为 -1 时将代理指定关卡至理智消耗完。<br>
`--tessdata-dir[-t] file_path` 指定文本检测框架`Tesseract`数据集的目录。<br>
`--use-mixture` 当理智不足时自动使用理智合剂。<br>
`--use-stone` 当理智不足时自动使用源石。<br>
`--n-mixture` 使用理智合剂的数量。<br>
`--n-stone` 使用源石的数量。<br>
`--plan[-p]` 代理完成后需要执行的操作。<br>
`--local-host[-l]` 虚拟机占用的本地端口。<br>

## Examples
* 代理 CE-5 关卡 3 次。<br>
`python main.py -m CE-5,3`
* 代理 OF-8 关卡 5 次后再代理 OF-F4 关卡至门票消耗完。<br>
`python main.py -m OF-8,5,OF-F4,-1`<br>
* 代理 OF-8 关卡至理智全部消耗，并自动使用一支理智合剂和一颗源石。<br>
`python main.py -m OF-8,-1 --use-mixture --n-mixture 1 --use-stone --n-stone 1`
* 代理 龙门市区 至理智耗尽，然后自动关机。<br>
`python -m 龙门市区,-1 -p "shutdown -s -t 300"`

# 目前支持的关卡(19/09/12 Update)
OF-6<br>
OF-7<br>
OF-8<br>
OF-F1<br>
OF-F2<br>
OF-F3<br>
OF-F4<br>
LS-1<br>
LS-2<br>
LS-3<br>
LS-4<br>
LS-5<br>
CA-1<br>
CA-2<br>
CA-3<br>
CA-4<br>
CA-5<br>
SK-1<br>
SK-2<br>
SK-3<br>
SK-4<br>
SK-5<br>
AP-1<br>
AP-2<br>
AP-3<br>
AP-4<br>
AP-5<br>
CE-1<br>
CE-2<br>
CE-3<br>
CE-4<br>
CE-5<br>
PR-A-1<br>
PR-A-2<br>
PR-B-1<br>
PR-B-2<br>
PR-C-1<br>
PR-C-2<br>
PR-D-1<br>
PR-D-2<br>
切尔诺伯格<br>
龙门外环<br>
龙门市区<br>
0-1<br>
1-7<br>
3-8<br>
4-5<br>
S4-1<br>
4-2<br>
4-10<br>
4-6<br>
4-9<br>
4-8<br>
4-7<br>
4-4<br>
5-8<br>
5-1<br>
