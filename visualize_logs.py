import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

LOG_FILE = Path("file_log.csv")

df = pd.read_csv(LOG_FILE)

df['Extension'] = df['File Name'].apply(lambda x: Path(x).suffix.lower())

df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')

df['Date'] = df['Timestamp'].dt.date

plt.figure(figsize=(8, 5))
df['Extension'].value_counts().plot(kind='bar')
plt.title("Number of Files Moved by Type")
plt.xlabel("File Type")
plt.ylabel("Count")
plt.tight_layout()
plt.show()

plt.figure(figsize=(8, 5))
df['Date'].value_counts().sort_index().plot(kind='bar')
plt.title("Date-wise File Movement Activity")
plt.xlabel("Date")
plt.ylabel("Number of Files Moved")
plt.tight_layout()
plt.show()