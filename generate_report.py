"""
生成课程设计说明书 Word 文档
"""
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE

doc = Document()

# 设置默认字体
style = doc.styles['Normal']
font = style.font
font.name = '宋体'
font.size = Pt(12)

# 标题
title = doc.add_heading('面向数控生产线刀具磨损状态识别与剩余寿命预测系统', 0)
title.alignment = WD_ALIGN_PARAGRAPH.CENTER

subtitle = doc.add_paragraph('制造智能技术课程设计说明书')
subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
subtitle_run = subtitle.runs[0]
subtitle_run.font.size = Pt(16)
subtitle_run.bold = True

doc.add_paragraph()

# 目录提示
doc.add_heading('目录', level=1)
doc.add_paragraph('1. 背景调研与研究意义')
doc.add_paragraph('2. 方案设计')
doc.add_paragraph('3. 数据集构建')
doc.add_paragraph('4. 技术方向详细设计')
doc.add_paragraph('5. 系统界面设计')
doc.add_paragraph('6. 系统调试与测试')
doc.add_paragraph('7. AI使用披露')
doc.add_paragraph('8. 总结与展望')

doc.add_page_break()

# 第1章 背景调研与研究意义
doc.add_heading('1. 背景调研与研究意义', level=1)

doc.add_heading('1.1 研究背景', level=2)
p = doc.add_paragraph()
p.add_run('随着智能制造技术的快速发展，数控加工生产线在现代制造业中扮演着越来越重要的角色。在数控加工过程中，刀具作为直接参与切削的关键部件，其磨损状态直接影响加工零件的尺寸精度、表面质量和生产效率。据统计，刀具磨损导致的非计划停机时间占整个生产线停机时间的20%以上，刀具成本占总制造成本的3%-5%。')

doc.add_heading('1.2 研究意义', level=2)
doc.add_paragraph('传统的刀具管理主要采用定期换刀和事后维修两种模式，存在以下问题：')
doc.add_paragraph('（1）定期换刀造成刀具浪费：为了保证加工质量，往往在刀具还未达到使用寿命时就提前更换，增加了生产成本；')
doc.add_paragraph('（2）事后维修导致产品不合格：刀具过度磨损后未能及时发现，导致加工出的零件尺寸超差、表面质量下降，造成批量报废；')
doc.add_paragraph('（3）设备停机损失大：刀具突然断裂可能导致设备损坏，造成更大的经济损失。')

p = doc.add_paragraph()
p.add_run('本项目研究基于传感器数据的刀具磨损状态识别与剩余寿命预测技术，实现预测性维护，具有以下重要意义：')
doc.add_paragraph('• 降低生产成本：精准掌握刀具磨损状态，在保证质量的前提下充分利用刀具寿命；')
doc.add_paragraph('• 提高产品合格率：实时监测刀具状态，及时发现异常磨损，避免批量不合格产品；')
doc.add_paragraph('• 减少非计划停机：预测剩余使用寿命，合理安排换刀计划，提高设备利用率；')
doc.add_paragraph('• 推动智能制造落地：将制造智能技术应用于实际生产场景，为 predictive maintenance 提供技术参考。')

doc.add_heading('1.3 国内外研究现状', level=2)
doc.add_paragraph('目前国内外学者在刀具磨损监测领域开展了大量研究，主要分为以下几类方法：')
doc.add_paragraph('（1）直接测量法：通过光学、接触式等方法直接测量刀具后刀面磨损量，精度高但难以在线应用；')
doc.add_paragraph('（2）间接监测法：通过采集切削力、振动、声发射等传感器信号，建立信号特征与磨损状态的映射关系，是目前的主流研究方向；')
doc.add_paragraph('（3）机器学习方法：从传统的统计分析、神经网络，到深度学习、迁移学习，模型的预测精度和泛化能力不断提升。')

doc.add_page_break()

# 第2章 方案设计
doc.add_heading('2. 方案设计', level=1)

doc.add_heading('2.1 系统总体架构', level=2)
doc.add_paragraph('本系统采用 B/S（Browser/Server）架构，整体分为四层：')
doc.add_paragraph('（1）前端展示层：基于 HTML+CSS+JavaScript 开发，提供可视化交互界面，包括预测表单、结果展示、历史记录、统计图表等功能；')
doc.add_paragraph('（2）后端服务层：基于 Python Flask 框架开发，提供 RESTful API 接口，处理业务逻辑，协调各模块工作；')
doc.add_paragraph('（3）算法模型层：实现刀具磨损状态分类和剩余寿命预测算法，基于 scikit-learn 机器学习库构建；')
doc.add_paragraph('（4）数据存储层：采用 SQLite 轻量级数据库，存储历史预测记录和系统运行数据。')

doc.add_heading('2.2 技术栈选型', level=2)
table = doc.add_table(rows=1, cols=2)
table.style = 'Table Grid'
hdr_cells = table.rows[0].cells
hdr_cells[0].text = '模块'
hdr_cells[1].text = '技术选型'

modules = [
    ('后端框架', 'Python 3.10 + Flask 2.0'),
    ('前端技术', 'HTML5 + CSS3 + JavaScript + Chart.js'),
    ('数据库', 'SQLite 3'),
    ('机器学习', 'scikit-learn（RandomForest）'),
    ('数据处理', 'numpy + pandas'),
    ('版本控制', 'Git + GitHub'),
]
for mod, tech in modules:
    row_cells = table.add_row().cells
    row_cells[0].text = mod
    row_cells[1].text = tech

doc.add_heading('2.3 功能需求分析', level=2)
doc.add_paragraph('系统主要实现以下功能：')
doc.add_paragraph('（1）数据预处理功能：对原始传感器数据进行清洗、异常值检测、标准化处理；')
doc.add_paragraph('（2）磨损状态预测功能：输入传感器特征参数，输出刀具磨损等级（轻微/中度/严重）；')
doc.add_paragraph('（3）剩余寿命预测功能：预测刀具剩余使用寿命（RUL），提前安排换刀计划；')
doc.add_paragraph('（4）历史记录管理：保存每次预测的结果，支持查询和统计分析；')
doc.add_paragraph('（5）可视化展示：通过图表直观展示磨损等级分布和预测趋势。')

doc.add_page_break()

# 第3章 数据集构建
doc.add_heading('3. 数据集构建', level=1)

doc.add_heading('3.1 数据来源', level=2)
p = doc.add_paragraph()
p.add_run('本项目采用 PHM Society 2010 年举办的刀具磨损预测竞赛公开数据集作为基础。该数据集由美国 National Institute of Standards and Technology (NIST) 提供，是刀具磨损监测领域最经典的公开数据集之一。')

doc.add_paragraph('数据集详细信息：')
doc.add_paragraph('• 实验对象：微型铣刀加工不锈钢工件')
doc.add_paragraph('• 采样信号：三向切削力（Fx, Fy, Fz）、三向振动（Vx, Vy, Vz）、声发射（AE-RMS）')
doc.add_paragraph('• 采样频率：50 kHz')
doc.add_paragraph('• 标签：刀具后刀面磨损量（单位：μm）')
doc.add_paragraph('• 完整规模：共 6 把刀具全生命周期实验数据')

doc.add_heading('3.2 示例子集构建', level=2)
doc.add_paragraph('由于完整数据集较大（约200MB），本项目构建了简化示例子集用于课程设计演示：')
doc.add_paragraph('（1）样本数量：训练集 200 个样本窗口，测试集 50 个样本窗口；')
doc.add_paragraph('（2）特征维度：28 维统计特征，包括各信号的均值、标准差、均方根(RMS)、最大值；')
doc.add_paragraph('（3）标签设计：')
doc.add_paragraph('    • 磨损等级：0=轻微磨损（<100μm），1=中度磨损（100-200μm），2=严重磨损（>200μm）')
doc.add_paragraph('    • 剩余寿命 RUL：以 300μm 为总寿命基准，计算剩余可磨损量')

doc.add_heading('3.3 数据预处理流程', level=2)
doc.add_paragraph('数据预处理主要包含以下步骤：')

doc.add_paragraph('（1）缺失值检查：遍历所有特征列，统计缺失值数量，本示例数据集无缺失值。')

doc.add_paragraph('（2）异常值检测：采用 IQR（四分位距）方法检测异常值。计算每个特征的 Q1（25%分位数）和 Q3（75%分位数），定义 IQR = Q3 - Q1，超出 [Q1 - 1.5*IQR, Q3 + 1.5*IQR] 范围的值判定为异常值。')

doc.add_paragraph('（3）异常值处理：采用边界截断法，将异常值截断到正常范围内，避免删除样本造成数据损失。')

doc.add_paragraph('（4）特征标准化：采用 Z-score 标准化方法，将每个特征转换为均值为0、标准差为1的标准正态分布。公式为：')
p = doc.add_paragraph()
p.add_run('    z = (x - μ) / σ').italic = True
doc.add_paragraph('其中 μ 为训练集均值，σ 为训练集标准差。')

doc.add_paragraph('（5）特征提取：从原始时序信号中提取统计特征，包括：')
doc.add_paragraph('    • 时域特征：均值、标准差、均方根、最大值、峭度、偏度')
doc.add_paragraph('    • 频域特征：通过 FFT 变换提取主频能量')

doc.add_page_break()

# 第4章 技术方向详细设计
doc.add_heading('4. 技术方向详细设计', level=1)

doc.add_heading('4.1 技术方向一：特征工程', level=2)
doc.add_paragraph('特征工程是刀具磨损预测的基础，直接影响模型的预测精度。本项目实现了完整的特征工程流程：')

doc.add_heading('4.1.1 特征提取', level=3)
doc.add_paragraph('从原始传感器信号中提取以下统计特征：')
table = doc.add_table(rows=1, cols=3)
table.style = 'Table Grid'
hdr = table.rows[0].cells
hdr[0].text = '特征类型'
hdr[1].text = '具体特征'
hdr[2].text = '物理意义'

features = [
    ('时域统计特征', '均值、标准差、均方根、最大值', '反映信号的整体能量和波动情况'),
    ('概率分布特征', '峭度、偏度', '反映信号分布的对称性和陡峭程度'),
    ('频域特征', '主频频率、主频能量', '反映信号的频率成分变化'),
]
for ft, fs, mean in features:
    row = table.add_row().cells
    row[0].text = ft
    row[1].text = fs
    row[2].text = mean

doc.add_heading('4.1.2 特征选择', level=3)
doc.add_paragraph('采用随机森林模型的特征重要性评估方法，对提取的特征进行重要性排序，保留对磨损状态区分度高的特征，去除冗余特征。')

doc.add_heading('4.1.3 数据标准化', level=3)
doc.add_paragraph('由于不同传感器信号的量纲和数值范围差异较大（如切削力量级为N，振动量级为g），需要进行标准化处理。本项目采用 Z-score 标准化方法，确保各特征对模型的贡献权重均衡。')

doc.add_heading('4.2 技术方向二：机器学习模型（分类+回归）', level=2)
doc.add_paragraph('本项目同时实现了磨损等级分类和剩余寿命预测两个任务，均采用 RandomForest（随机森林）算法。')

doc.add_heading('4.2.1 随机森林算法原理', level=3)
doc.add_paragraph('随机森林是一种集成学习方法，通过构建多棵决策树并集成它们的预测结果来提高模型的泛化能力。其核心思想是：')
doc.add_paragraph('（1）Bootstrap 抽样：从训练集中有放回地抽取 N 个子样本，每棵树使用不同的子样本训练；')
doc.add_paragraph('（2）特征随机选择：每个节点分裂时，从所有特征中随机选择一部分特征作为候选；')
doc.add_paragraph('（3）投票决策：分类任务采用多数投票，回归任务采用平均值。')

doc.add_heading('4.2.2 磨损等级分类模型', level=3)
doc.add_paragraph('任务目标：输入传感器特征向量，输出刀具磨损等级（0=轻微，1=中度，2=严重）。')
doc.add_paragraph('模型参数：')
doc.add_paragraph('• 决策树数量：50 棵')
doc.add_paragraph('• 最大深度：10')
doc.add_paragraph('• 评估指标：准确率、精确率、召回率、F1 分数、混淆矩阵')

doc.add_heading('4.2.3 剩余寿命回归模型', level=3)
doc.add_paragraph('任务目标：输入传感器特征向量，输出刀具剩余使用寿命（RUL，单位：小时）。')
doc.add_paragraph('模型参数：')
doc.add_paragraph('• 决策树数量：50 棵')
doc.add_paragraph('• 损失函数：均方误差（MSE）')
doc.add_paragraph('• 评估指标：RMSE、MAE、R² 决定系数')

doc.add_heading('4.2.4 模型优势', level=3)
doc.add_paragraph('随机森林相比其他算法的优势：')
doc.add_paragraph('• 抗过拟合能力强：多棵树集成降低了单棵树的过拟合风险；')
doc.add_paragraph('• 处理高维数据能力强：自动进行特征选择；')
doc.add_paragraph('• 对异常值不敏感：鲁棒性好；')
doc.add_paragraph('• 可解释性好：可以输出特征重要性排序。')

doc.add_heading('4.3 技术方向三：PHM 故障预测与健康管理', level=2)
doc.add_paragraph('PHM（Prognostics and Health Management，故障预测与健康管理）是智能制造的核心技术之一，本项目在系统设计中融入了 PHM 理念。')

doc.add_heading('4.3.1 健康状态分级', level=3)
doc.add_paragraph('根据磨损等级将刀具健康状态分为三级：')
table = doc.add_table(rows=1, cols=4)
table.style = 'Table Grid'
hdr = table.rows[0].cells
hdr[0].text = '等级'
hdr[1].text = '磨损范围'
hdr[2].text = '状态'
hdr[3].text = '建议措施'

levels = [
    ('一级', '0-100 μm', '正常（绿色）', '继续使用，按计划监测'),
    ('二级', '100-200 μm', '预警（黄色）', '加强监测，准备换刀'),
    ('三级', '>200 μm', '报警（红色）', '立即更换刀具'),
]
for lvl, wear, status, action in levels:
    row = table.add_row().cells
    row[0].text = lvl
    row[1].text = wear
    row[2].text = status
    row[3].text = action

doc.add_heading('4.3.2 预测性维护策略', level=3)
doc.add_paragraph('传统维护策略 vs 预测性维护：')
doc.add_paragraph('（1）纠正性维护（事后维修）：设备坏了再修，停机损失大；')
doc.add_paragraph('（2）预防性维护（定期更换）：按固定周期换刀，可能造成浪费；')
doc.add_paragraph('（3）预测性维护（本项目）：根据实时监测和预测结果，在最佳时间点换刀，兼顾成本和可靠性。')

doc.add_heading('4.3.3 风险预警机制', level=3)
doc.add_paragraph('系统根据预测结果自动触发风险预警：')
doc.add_paragraph('• 正常状态（绿色）：刀具状态良好，无需干预；')
doc.add_paragraph('• 预警状态（黄色）：刀具磨损加剧，提示运维人员关注；')
doc.add_paragraph('• 报警状态（红色）：刀具接近寿命终点，建议立即更换。')

doc.add_page_break()

# 第5章 系统界面设计
doc.add_heading('5. 系统界面设计', level=1)

doc.add_heading('5.1 界面整体布局', level=2)
doc.add_paragraph('系统采用响应式布局，整体分为三个区域：')
doc.add_paragraph('（1）顶部导航区：系统标题和项目说明；')
doc.add_paragraph('（2）统计概览区：4 个关键指标卡片（总预测次数、平均剩余寿命、当前状态、模型准确率）；')
doc.add_paragraph('（3）主内容区：左侧预测操作面板，右侧历史记录表格，底部统计图表。')

doc.add_heading('5.2 核心功能模块界面', level=2)

doc.add_heading('5.2.1 预测操作面板', level=3)
doc.add_paragraph('用户输入以下传感器特征参数：')
doc.add_paragraph('• 切削力 X/Y 均值（N）')
doc.add_paragraph('• 振动 X/Z 均方根')
doc.add_paragraph('• 声发射 RMS')
doc.add_paragraph('点击"开始预测"按钮后，系统调用后端 API 进行预测，结果以颜色区分的卡片形式展示：绿色（正常）、黄色（预警）、红色（报警）。')

doc.add_heading('5.2.2 历史记录表格', level=3)
doc.add_paragraph('表格展示最近 20 条预测记录，包含：时间、样本ID、磨损等级、RUL 数值、风险等级。风险等级用彩色标签（badge）直观展示。')

doc.add_heading('5.2.3 统计图表', level=3)
doc.add_paragraph('底部柱状图展示磨损等级分布统计，直观反映当前刀具健康状况。图表使用 Chart.js 库实现，支持响应式显示。')

doc.add_heading('5.3 后端 API 设计', level=2)
table = doc.add_table(rows=1, cols=3)
table.style = 'Table Grid'
hdr = table.rows[0].cells
hdr[0].text = '接口路径'
hdr[1].text = '请求方法'
hdr[2].text = '功能说明'

apis = [
    ('/', 'GET', '前端主页面'),
    ('/api/predict', 'POST', '磨损状态预测'),
    ('/api/records', 'GET', '获取历史预测记录'),
    ('/api/stats', 'GET', '获取系统统计信息'),
]
for path, method, desc in apis:
    row = table.add_row().cells
    row[0].text = path
    row[1].text = method
    row[2].text = desc

doc.add_page_break()

# 第6章 系统调试与测试
doc.add_heading('6. 系统调试与测试', level=1)

doc.add_heading('6.1 调试过程中遇到的问题及解决', level=2)

doc.add_heading('6.1.1 Git 路径问题', level=3)
doc.add_paragraph('问题描述：在 Git Bash 中使用 Windows 格式路径（C:\\...）时，反斜杠被转义，导致找不到目录。')
doc.add_paragraph('解决方法：Git Bash 中使用 Unix 风格路径（/c/Users/...），或使用引号包裹路径。')

doc.add_heading('6.1.2 Git 权限问题', level=3)
doc.add_paragraph('问题描述：推送代码时出现 403 权限错误，提示 Permission denied。')
doc.add_paragraph('原因分析：Git 凭据管理器中保存的是其他 GitHub 账号的登录信息，没有当前仓库的推送权限。')
doc.add_paragraph('解决方法：打开 Windows 凭据管理器，删除旧的 GitHub 凭据，重新执行 git push，通过浏览器 OAuth 授权登录正确的账号。')

doc.add_heading('6.1.3 Python 环境问题', level=3)
doc.add_paragraph('问题描述：在 Git Bash 中执行 python 命令没有任何输出。')
doc.add_paragraph('原因分析：Git Bash 的 PATH 环境变量中未正确配置 Python 路径，可能指向了 Windows Store 的 Python 占位符。')
doc.add_paragraph('解决方法：在 PowerShell 或 CMD 中运行，或使用 Python 的完整路径。')

doc.add_heading('6.2 功能测试', level=2)
doc.add_paragraph('系统完成后进行了全面的功能测试：')

doc.add_paragraph('（1）数据预处理测试：')
doc.add_paragraph('    • 缺失值检测：正确识别无缺失值的数据集')
doc.add_paragraph('    • 异常值检测：正确识别 IQR 范围外的异常点')
doc.add_paragraph('    • 标准化：验证标准化后特征均值为0，标准差为1')

doc.add_paragraph('（2）预测功能测试：')
doc.add_paragraph('    • 输入低磨损特征：正确判定为轻微磨损，RUL 较高')
doc.add_paragraph('    • 输入高磨损特征：正确判定为严重磨损，RUL 较低')
doc.add_paragraph('    • 预测结果自动保存到数据库')

doc.add_paragraph('（3）界面交互测试：')
doc.add_paragraph('    • 预测按钮点击后正确显示结果')
doc.add_paragraph('    • 历史记录表格自动刷新')
doc.add_paragraph('    • 统计图表数据正确更新')

doc.add_page_break()

# 第7章 AI 使用披露
doc.add_heading('7. AI 使用披露', level=1)

doc.add_heading('7.1 所用 AI 工具', level=2)
doc.add_paragraph('• AI 编程助手：豆包（Doubao）')
doc.add_paragraph('• 辅助内容：需求分析、代码生成、文档撰写、问题调试')

doc.add_heading('7.2 关键 Prompt 策略', level=2)
doc.add_paragraph('（1）角色设定：明确 AI 角色为"资深智能制造工程师"，确保输出内容专业；')
doc.add_paragraph('（2）分步实现：将复杂任务拆解为小步骤，逐个完成，避免 AI 生成大段不可控代码；')
doc.add_paragraph('（3）约束说明：明确技术栈（Python + Flask）、代码风格、输出格式要求；')
doc.add_paragraph('（4）要求解释：要求 AI 解释关键代码逻辑，确保自己理解后再使用；')
doc.add_paragraph('（5）小步验证：每完成一个小功能立即测试，发现问题及时调整。')

doc.add_heading('7.3 AI 出错案例及纠正', level=2)
table = doc.add_table(rows=1, cols=3)
table.style = 'Table Grid'
hdr = table.rows[0].cells
hdr[0].text = '错误类型'
hdr[1].text = '具体表现'
hdr[2].text = '纠正方法'

errors = [
    ('路径错误', 'Git Bash 中 Windows 路径被转义', '改用 Unix 风格路径格式'),
    ('权限错误', 'Git 推送 403 权限不足', '清除旧凭据，重新授权登录'),
    ('依赖缺失', 'ModuleNotFoundError', '使用 python -m pip 安装依赖'),
    ('环境问题', 'Git Bash 中 Python 无输出', '改用 PowerShell 运行'),
]
for etype, expr, fix in errors:
    row = table.add_row().cells
    row[0].text = etype
    row[1].text = expr
    row[2].text = fix

doc.add_page_break()

# 第8章 总结与展望
doc.add_heading('8. 总结与展望', level=1)

doc.add_heading('8.1 项目总结', level=2)
doc.add_paragraph('本项目完成了面向数控生产线的刀具磨损状态识别与剩余寿命预测系统，主要成果包括：')
doc.add_paragraph('（1）完成了完整的 B/S 架构系统开发，包括前端可视化界面、后端 API 服务、SQLite 数据库和机器学习算法模块；')
doc.add_paragraph('（2）实现了三大核心功能：刀具磨损等级分类、剩余使用寿命预测、风险分级预警；')
doc.add_paragraph('（3）融入了制造智能技术课程的三个核心技术方向：特征工程、机器学习模型、PHM 预测性维护；')
doc.add_paragraph('（4）全程采用 Vibe Coding 方法开发，使用 Git 进行版本控制，保留了完整的开发过程记录。')

doc.add_heading('8.2 存在的不足', level=2)
doc.add_paragraph('（1）当前使用的是简化示例数据集，与真实工业数据还有差距；')
doc.add_paragraph('（2）算法模型采用随机森林，未来可以尝试更先进的深度学习模型（CNN+LSTM）；')
doc.add_paragraph('（3）前端界面较为简单，后续可以增加实时数据接入、3D 可视化等功能；')
doc.add_paragraph('（4）目前只支持单台刀具监测，未来可以扩展到生产线多设备集群监测。')

doc.add_heading('8.3 未来展望', level=2)
doc.add_paragraph('（1）接入真实工业传感器数据，提高模型的实际应用价值；')
doc.add_paragraph('（2）引入深度学习模型（CNN-LSTM、Transformer），提升预测精度；')
doc.add_paragraph('（3）开发移动端应用，方便现场运维人员随时查看刀具状态；')
doc.add_paragraph('（4）集成 MES 系统，实现从预测性维护到自动调度换刀的闭环。')

doc.add_paragraph()
p = doc.add_paragraph()
p.add_run('通过本次课程设计，我深入理解了制造智能技术在工业场景中的应用方法，掌握了从数据采集、预处理、建模到系统部署的完整流程，为今后从事智能制造相关工作打下了坚实基础。')

# 保存文档
doc.save(r'C:\Users\ASUS\Doubao\chats\2026-09-13\new-chat\repo\设计说明书.docx')
print("设计说明书生成成功！")
