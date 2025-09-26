import pandas as pd
import google.generativeai as genai
import time
import sys

sys.stdout.reconfigure(encoding='utf-8')

genai.configure(api_key="AIzaSyBql2t7UDVix0Olaa1HWswl5Fdd1kc_D5Q")
#cấu hình API key để xác thực với Google
model = genai.GenerativeModel("gemini-1.5-flash")
# khởi tạo mô hình Gemini 1.5 Flash

df = pd.read_csv("Comment_cleaned.csv", encoding="utf-8-sig")
print(f"Đã đọc {len(df)} comment.") #hiển thị số comment đã đọc

def classify_sentiment_batch(comments):
    joined = "\n".join([f"{i+1}. {c}" for i, c in enumerate(comments)]) 
    # đánh số thứ tự comment (chỉ_số, giá_trị) 
    prompt = f"""
    Phân loại cảm xúc cho các câu dưới đây thành một trong 3 nhãn:
    - Tích cực
    - Tiêu cực
    - Trung lập
    Trả về kết quả dạng danh sách, mỗi dòng chỉ chứa đúng 1 nhãn theo thứ tự câu.
    Danh sách câu:
    {joined}
    """
    try:
        response = model.generate_content(prompt)
        labels = [line.strip() for line in response.text.split("\n") if line.strip()]
        # đảm bảo số lượng nhãn khớp số comment
        while len(labels) < len(comments):
            labels.append("Không xác định")
        return labels
    except Exception as e:
        print(f"Lỗi batch: {e}")
        return ["Không xác định"] * len(comments)

batch_size = 20
sentiments = []

for i in range(0, len(df), batch_size):
    batch = df['comment_cleaned'][i:i+batch_size].tolist()
    labels = classify_sentiment_batch(batch)
    sentiments.extend(labels)
    time.sleep(0.5)  # delay nhẹ để tránh quota

df['sentiment'] = sentiments
df.to_csv("comments_label.csv", index=False, encoding="utf-8-sig")
print(" Đã lưu file comments_label.csv")
