from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "试制前三讲"
OUT.mkdir(parents=True, exist_ok=True)
FONT = ROOT / "fonts" / "LXGWWenKai-Regular.ttf"

def F(size):
    return ImageFont.truetype(str(FONT), size)

def wrap(draw, text, font, width):
    lines=[]
    for p in text.split("\n"):
        cur=""
        for ch in p:
            if draw.textbbox((0,0),cur+ch,font=font)[2] <= width:
                cur += ch
            else:
                if cur: lines.append(cur)
                cur=ch
        if cur: lines.append(cur)
    return lines

def page(title, subtitle, sections):
    W,H=1600,2260
    im=Image.new("RGB",(W,H),(255,255,255))
    d=ImageDraw.Draw(im)
    d.text((90,55),"七年级数学 · 大培优 2026",font=F(42),fill=(25,50,90))
    d.text((90,115),title,font=F(72),fill=(18,35,80))
    d.text((92,205),subtitle,font=F(38),fill=(180,55,95))
    y=285
    fills=[(255,247,231),(235,248,240),(236,245,255),(250,238,247),(244,240,255),(245,249,232)]
    for i,(head,body) in enumerate(sections):
        col=i%2
        if col==0 and i>0: y += 24
        x=75+col*775
        f=F(31); lines=wrap(d,body,f,650); h=max(270,115+len(lines)*47)
        d.rounded_rectangle((x,y,x+720,y+h),28,fill=fills[i%len(fills)],outline=(190,200,210),width=3)
        d.text((x+28,y+22),head,font=F(40),fill=(20,65,120))
        yy=y+82
        for line in lines:
            d.text((x+32,yy),line,font=f,fill=(35,35,45)); yy+=47
        if col==1: y += h
    d.text((90,H-65),"樊老师数学 · 知识点整理",font=F(28),fill=(100,100,105))
    return im

def effect(paper):
    W,H=1600,2260
    desk=Image.new("RGB",(W+260,H+220),(112,87,65)); d=ImageDraw.Draw(desk)
    for y in range(0,desk.height,42): d.line((0,y,desk.width,y+8),fill=(125,96,72),width=2)
    paper=paper.rotate(-1.2,expand=True,resample=Image.Resampling.BICUBIC)
    shadow=Image.new("RGBA",paper.size,(0,0,0,0)); sd=ImageDraw.Draw(shadow)
    sd.rounded_rectangle((18,18,paper.width-8,paper.height-8),25,fill=(0,0,0,95))
    shadow=shadow.filter(ImageFilter.GaussianBlur(18))
    desk.paste(shadow,(105,75),shadow); desk.paste(paper,(85,50))
    d=ImageDraw.Draw(desk)
    d.rounded_rectangle((desk.width-185,300,desk.width-125,900),25,fill=(210,45,55))
    d.ellipse((desk.width-180,250,desk.width-130,310),fill=(235,75,80))
    d.rectangle((30,desk.height-250,400,desk.height-200),fill=(70,70,70))
    return desk

lectures=[
("第1讲｜有理数 5 个核心概念一次搞懂","正负数 · 有理数 · 数轴 · 相反数 · 绝对值",[("① 正数与负数","大于0的数叫正数；在正数前添“－”得到负数。0既不是正数，也不是负数。实际问题中，正负号常表示相反意义的量。"),("② 有理数","整数和分数统称有理数。有理数包括正有理数、0、负有理数；整数也可以看作分母为1的分数。"),("③ 数轴","规定原点、正方向和单位长度的直线叫数轴。数轴上的点与有理数一一对应；右边的数总大于左边的数。"),("④ 相反数","只有符号不同的两个数互为相反数。a的相反数是－a，0的相反数仍是0；互为相反数的两个数和为0。"),("⑤ 绝对值","数轴上表示数a的点到原点的距离叫a的绝对值，记作|a|。|a|≥0；|a|=0⇔a=0；|a|=|-a|。"),("⑥ 五个概念的联系","有理数可以按正、0、负分类；数轴把数与点对应起来；相反数关于原点对称；绝对值表示到原点的距离。"),("⑦ 典型题型","判断正负数；写相反数；数轴定位与比较；求绝对值；根据|x|=a判断x。易错：0不是正数也不是负数；|a|不能为负。")]),
("第2讲｜创新题型：把有理数放进真实情境里","生活数学 · 数轴与刻度尺 · 数轴与图形",[("① 生活数学","用正负数表示具有相反意义的量。先确定“基准量”和正方向，再把实际数据转化成有理数。"),("② 数轴与刻度尺","把刻度尺看作数轴：确定0点、单位长度和正方向，再根据实际长度或刻度换算数轴上的数。"),("③ 数轴与位置","数轴上点的位置可以表示实际数量。先读出对应刻度，再利用相邻刻度的单位长度建立数量关系。"),("④ 数轴与折线","折线、移动、上升下降等情境可转化为数轴上的位移问题。方向相反时用相反符号表示。"),("⑤ 解题流程","读情境→确定正负意义→建立数轴或数量关系→列式→计算→结合题意写结论。图形信息多时先标出关键点。"),("⑥ 常见陷阱","不要把“位置”和“距离”混为一谈；距离通常非负，位移可能有正负；刻度单位改变时，数量关系也要同步改变。"),("⑦ 训练重点","数轴读数、刻度换算、位置关系、距离问题、折线图情境。核心不是复杂计算，而是把实际信息准确翻译成数学语言。")]),
("第3讲｜有理数四则运算：先定号，再计算","加法 · 减法 · 分类讨论 · 乘除与混合运算",[("① 有理数加法","同号相加：取相同符号，并把绝对值相加；异号相加：取绝对值较大的数的符号，并用较大绝对值减较小绝对值。"),("② 有理数减法","减去一个数，等于加上这个数的相反数：a－b=a+(－b)。计算时先把减法统一成加法，再按加法法则处理。"),("③ 加减混合运算","先统一成加法，再利用加法交换律、结合律简化计算。多个数连续运算时，先观察符号和绝对值，避免盲算。"),("④ 分类讨论","含字母或绝对值的题目，要根据字母的正负、大小关系分类。每一类分别判断，再检查分类是否完整、互斥。"),("⑤ 乘法与除法","乘法先定符号：同号得正、异号得负，再把绝对值相乘。除法转化为乘法：除以一个数等于乘这个数的倒数。"),("⑥ 混合运算","先乘方，再乘除，最后加减；同级运算从左到右。遇到括号先算括号内，注意符号与运算顺序。"),("⑦ 易错提醒","负号不是“答案符号”而是运算的一部分；除数不能为0；分数、负数连续运算时，先整理符号，再计算更稳。")])]

for i,(title,subtitle,sections) in enumerate(lectures,1):
    p=page(title,subtitle,sections)
    p.save(OUT/f"第{i}讲-正面打印版.png")
    effect(p).save(OUT/f"第{i}讲-实物手写效果图.png")

(OUT/"README.md").write_text("# 前三讲试制图\n\n每讲两张：实物手写效果图 + 正面打印版。统一使用 LXGW WenKai 手写风格字体，两张内容一致。\n",encoding="utf-8")
