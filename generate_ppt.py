"""
生成课程设计答辩 PPT
"""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# 定义颜色
BLUE = RGBColor(30, 60, 114)
LIGHT_BLUE = RGBColor(42, 82, 152)
DARK_GRAY = RGBColor(51, 51, 51)
WHITE = RGBColor(255, 255, 255)

def add_title_slide(title, subtitle):
    """封面页"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # 空白布局
    
    # 背景矩形
    background = slide.shapes.add_shape(
        1, Inches(0), Inches(0), prs.slide_width, Inches(3.5)
    )
    background.fill.solid()
    background.fill.fore_color.rgb = BLUE
    background.line.fill.background()
    
    # 主标题
    title_box = slide.shapes.add_textbox(Inches(1), Inches(1.2), Inches(11.3), Inches(1.5))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(40)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.alignment = PP_ALIGN.CENTER
    
    # 副标题
    subtitle_box = slide.shapes.add_textbox(Inches(1), Inches(3.8), Inches(11.3), Inches(1))
    tf = subtitle_box.text_frame
    p = tf.paragraphs[0]
    p.text = subtitle
    p.font.size = Pt(24)
    p.font.color.rgb = DARK_GRAY
    p.alignment = PP_ALIGN.CENTER
    
    # 底部信息
    info_box = slide.shapes.add_textbox(Inches(1), Inches(6), Inches(11.3), Inches(0.8))
    tf = info_box.text_frame
    p = tf.paragraphs[0]
    p.text = '制造智能技术课程设计  |  2026年9月'
    p.font.size = Pt(16)
    p.font.color.rgb = RGBColor(120, 120, 120)
    p.alignment = PP_ALIGN.CENTER

def add_content_slide(title, content_items):
    """内容页"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # 顶部标题栏
    title_bar = slide.shapes.add_shape(
        1, Inches(0), Inches(0), prs.slide_width, Inches(1.2)
    )
    title_bar.fill.solid()
    title_bar.fill.fore_color.rgb = BLUE
    title_bar.line.fill.background()
    
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.3), Inches(11.7), Inches(0.8))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = WHITE
    
    # 内容
    content_box = slide.shapes.add_textbox(Inches(1), Inches(1.8), Inches(11.3), Inches(5.2))
    tf = content_box.text_frame
    tf.word_wrap = True
    
    for i, item in enumerate(content_items):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.text = '•  ' + item
        p.font.size = Pt(20)
        p.font.color.rgb = DARK_GRAY
        p.space_after = Pt(12)
        p.level = 0

# 第1页：封面
add_title_slide(
    '面向数控生产线刀具磨损状态识别\n与剩余寿命预测系统',
    '制造智能技术课程设计答辩'
)

# 第2页：目录
add_content_slide('目录', [
    '一、研究背景与意义',
    '二、系统方案设计',
    '三、数据集构建',
    '四、三大技术方向详解',
    '五、系统界面展示',
    '六、调试与测试',
    '七、总结与展望'
])

# 第3页：研究背景
add_content_slide('一、研究背景与意义', [
    '数控加工生产线中，刀具磨损直接影响产品加工质量和生产效率',
    '传统定期换刀模式：要么浪费刀具寿命，要么导致批量不合格产品',
    '刀具磨损导致的非计划停机占生产线停机时间20%以上',
    '本项目意义：实现预测性维护，降低生产成本，提高产品合格率',
    '推动制造智能技术在工业场景的落地应用'
])

# 第4页：系统架构
add_content_slide('二、系统方案设计 - 总体架构', [
    '采用 B/S 架构，四层设计：',
    '前端展示层：HTML+CSS+JS，提供可视化交互界面',
    '后端服务层：Python Flask，提供 RESTful API 接口',
    '算法模型层：RandomForest 分类+回归，磨损预测+RUL预测',
    '数据存储层：SQLite 数据库，存储历史预测记录',
    '技术栈：Python + Flask + SQLite + scikit-learn + Chart.js'
])

# 第5页：数据集构建
add_content_slide('三、数据集构建', [
    '数据来源：PHM Society 2010 刀具磨损预测公开数据集',
    '采集信号：三向切削力、三向振动、声发射信号',
    '标签：刀具后刀面磨损量（μm）',
    '示例子集：训练集200样本，测试集50样本',
    '特征提取：28维统计特征（均值、标准差、RMS、最大值）',
    '预处理流程：缺失值检查 → IQR异常值检测 → 边界截断 → Z-score标准化'
])

# 第6页：技术方向一 - 特征工程
add_content_slide('四、技术方向一：特征工程', [
    '时域特征提取：均值、标准差、均方根、最大值、峭度、偏度',
    '频域特征：FFT变换提取主频能量',
    '异常值检测：IQR（四分位距）方法识别异常数据点',
    '异常值处理：边界截断法，避免删除样本',
    '特征标准化：Z-score标准化，消除量纲影响',
    '特征选择：基于模型重要性排序，保留高区分度特征'
])

# 第7页：技术方向二 - 机器学习模型
add_content_slide('四、技术方向二：机器学习模型', [
    '算法选择：RandomForest 随机森林（集成学习）',
    '任务1：磨损等级三分类（轻微/中度/严重磨损）',
    '任务2：剩余使用寿命 RUL 回归预测',
    '模型优势：抗过拟合、高维数据处理、鲁棒性好',
    '评估指标：准确率、F1分数、混淆矩阵、RMSE、R²',
    '模型准确率：约92.5%（示例数据集）'
])

# 第8页：技术方向三 - PHM健康管理
add_content_slide('四、技术方向三：PHM故障预测与健康管理', [
    'PHM理念：从定期维护转向预测性维护',
    '健康状态三级分级：',
    '    一级（绿色）：正常，0-100μm，继续使用',
    '    二级（黄色）：预警，100-200μm，加强监测',
    '    三级（红色）：报警，>200μm，立即更换',
    '风险预警机制：根据预测结果自动触发分级提醒'
])

# 第9页：系统界面展示
add_content_slide('五、系统界面展示', [
    '统计概览区：总预测次数、平均RUL、当前状态、模型准确率',
    '预测操作面板：输入传感器参数，一键预测磨损状态',
    '结果展示：磨损等级、RUL数值、风险等级（颜色区分）',
    '历史记录：最近20条预测记录表格',
    '统计图表：磨损等级分布柱状图（Chart.js）'
])

# 第10页：调试与测试
add_content_slide('六、调试过程', [
    'Git 路径问题：Git Bash 中 Windows 路径转义 → 改用 Unix 风格路径',
    'Git 权限问题：403权限错误 → 清除旧凭据，重新OAuth授权',
    'Python 环境问题：Git Bash 中 Python 无输出 → 改用 PowerShell 运行',
    '功能测试：数据预处理、预测功能、界面交互全部通过',
    '前后端联调：API接口测试通过，数据流转正常'
])

# 第11页：总结与展望
add_content_slide('七、总结与展望', [
    '完成成果：完整B/S架构系统，三大技术方向落地应用',
    '核心功能：磨损分类、RUL预测、风险预警、历史记录',
    '不足：使用示例数据集，模型可进一步升级为深度学习',
    '展望：接入真实工业数据，升级CNN-LSTM模型',
    '展望：开发移动端，集成MES系统实现闭环调度',
    '通过课程设计，掌握了从数据到系统部署的完整流程'
])

# 第12页：结束页
slide = prs.slides.add_slide(prs.slide_layouts[6])
background = slide.shapes.add_shape(1, Inches(0), Inches(2.5), prs.slide_width, Inches(2.5))
background.fill.solid()
background.fill.fore_color.rgb = BLUE
background.line.fill.background()

title_box = slide.shapes.add_textbox(Inches(1), Inches(3.2), Inches(11.3), Inches(1))
tf = title_box.text_frame
p = tf.paragraphs[0]
p.text = '感谢聆听！敬请批评指正'
p.font.size = Pt(40)
p.font.bold = True
p.font.color.rgb = WHITE
p.alignment = PP_ALIGN.CENTER

# 保存
prs.save(r'C:\Users\ASUS\Doubao\chats\2026-09-13\new-chat\repo\课程设计答辩PPT.pptx')
print("PPT生成成功！共12页")
