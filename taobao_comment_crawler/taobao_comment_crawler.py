from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

CHROMEDRIVER_PATH = "D:/chromedriver-win64/chromedriver.exe"
service = Service(CHROMEDRIVER_PATH)
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

# 打开淘宝并扫码登录
driver.get("https://www.taobao.com")
print("请在60秒内扫码登录淘宝...")
time.sleep(60)

# 商品页（你也可以换成其他商品）
driver.get("https://detail.tmall.com/item.htm?detail_redpacket_pop=true&id=865120623715&ltk2=1744005797564ws8mmg1rfrzswsc5u3kg&ns=1&pisk=gCPjEI27jnxfRaG95xbrRPi3dyh6ka5ecFgT-Pd2WjhxX8a3fm7GnjySfuESDI7cnAn_mjHg3coqffagAaSFT6z0ofDdYM5eR4E2TX0vDKKZyz3i1qCfaT7YofcOfdQ8kXa0vF4aed3tyagZ7CKYXAU-2Vi-WKhTX0H-J2-x6lEtwQ3E8h3xHmhJe00vBKHxBzp-5VxxkqETyagi2chtBlU-Bd_EyLn7lZArNhVywenmVCdTN4IiRrskZVFZlxiLkSODiN0jhDUx2M2KDPk8SANMSCMakJqiJoKAfcV7ySeLvgJqDJg_8RZd7K0rCScSXSCHR0Fb57M0UnpxRjijpSEJ-wzSB8NSgSIMKzzSDvGzUTjqQjZbKDDAEgq_PmrTGYKf4cyUzSH7vgR7jAwTgbFA26syZBoB51p6PvAsPD75PdvGIKIB1Jao5HDxr4v5Pa9nLx3oPD75PdviH40kRa_WKv5..&priceTId=2101280917440044663625523e0bdd&query=%E5%85%B0%E8%8A%B1&skuId=5858795891319&spm=a21n57.1.hoverItem.1&utparam=%7B%22aplus_abtest%22%3A%22e47695ffc4aa51f853ef4d25e87e8c13%22%7D&xxc=ad_ztc")
time.sleep(5)

# 滚动以加载评论区
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(3)

# 点击“全部”评论标签页
try:
    comments_section = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//span[@data-spm-anchor-id="pc_detail.29232929/evo365560b447259.202207.i8.6fd27dd6o0VFF5"]'))
    )
    comments_section.click()
    print("已点击评论标签页")
    time.sleep(4)
except Exception as e:
    print("未找到评论标签页，跳过", e)

# 存储评论
all_comments = []

# 抓取多页评论（最多抓取 N 页）
MAX_PAGES = 5
for page in range(MAX_PAGES):
    print(f"\n📄 正在抓取第 {page+1} 页评论...")
    time.sleep(3)

    # 滚动以加载评论
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    # 找到评论内容（多个 class 名尝试）
    comments = driver.find_elements(By.CLASS_NAME, "tm-rate-content") or \
               driver.find_elements(By.CLASS_NAME, "rate-content")

    for c in comments:
        text = c.text.strip()
        if text and len(text) > 3:  # 简单过滤无效内容
            all_comments.append(text)

    print(f"当前累计评论数：{len(all_comments)}")

    # 找“下一页”按钮翻页
    try:
        next_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//a[contains(text(), "下一页") or contains(@class, "ui-page-next")]'))
        )
        if "disabled" in next_button.get_attribute("class"):
            print("❌ 下一页按钮不可点击，停止抓取。")
            break
        next_button.click()
    except Exception as e:
        print("⚠️ 找不到下一页按钮，停止翻页。", e)
        break

# 输出部分结果
print(f"\n✅ 共抓取评论数：{len(all_comments)}")
for i, comment in enumerate(all_comments[:10]):
    print(f"[{i+1}] {comment}")

# 保存为文本文件，后续用于词云
with open("orchid_comments.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(all_comments))

# driver.quit()  # 可取消注释关闭浏览器