import pandas as pd
import json

# Đọc file JSON
input_path = "/mnt/data/tuyensinh.json"
output_path = "/mnt/data/tuyensinh.csv"

with open(input_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Chuyển sang DataFrame
df = pd.DataFrame(data)

# Xuất sang CSV
df.to_csv(output_path, index=False, encoding="utf-8-sig")

output_path
