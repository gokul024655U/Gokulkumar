import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read the dataset
file_path = r'D:\New folder\dataset.csv'  # Use your local path if running locally
df = pd.read_csv(file_path)

# Clean and prepare data
df.columns = df.columns.str.strip()  # Remove any extra spaces
df['Accident Date'] = pd.to_datetime(df['Accident Date'], dayfirst=True)
df['Month'] = df['Accident Date'].dt.month

# Classify fatal vs other
df['Fatal'] = df['Casualty Severity'] == 1
df['Non-Fatal'] = df['Casualty Severity'] != 1

# Pie Chart Data
death_data = {
    'Road Accidents (Fatal)': df['Fatal'].sum(),
    'Other Casualties': df['Non-Fatal'].sum()
}

# Bar Chart Data: Monthly counts
monthly_data = df.groupby('Month').agg({
    'Fatal': 'sum',
    'Non-Fatal': 'sum'
}).reindex(range(1, 13), fill_value=0)

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
deaths = monthly_data['Fatal'].tolist()
injuries = monthly_data['Non-Fatal'].tolist()

# Create subplot
fig, axs = plt.subplots(1, 2, figsize=(18, 7))

# -------- Pie Chart --------
axs[0].pie(death_data.values(), labels=death_data.keys(), autopct='%1.1f%%',
           startangle=140, colors=['#ff9999', '#66b3ff'])
axs[0].set_title('Distribution of Casualties by Severity (2014)')
axs[0].axis('equal')

# -------- Bar Chart --------
x = np.arange(len(months))
width = 0.35
rects1 = axs[1].bar(x - width/2, deaths, width, label='Fatalities', color='red')
rects2 = axs[1].bar(x + width/2, injuries, width, label='Non-Fatal', color='orange')

axs[1].set_xlabel('Month')
axs[1].set_ylabel('Number of Casualties')
axs[1].set_title('Monthly Fatal and Non-Fatal Road Casualties')
axs[1].set_xticks(x)
axs[1].set_xticklabels(months)
axs[1].legend()

# Label bars
def autolabel(rects, ax):
    for rect in rects:
        height = rect.get_height()
        ax.annotate(f'{int(height)}', xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points", ha='center', va='bottom')

autolabel(rects1, axs[1])
autolabel(rects2, axs[1])

plt.tight_layout()
plt.subplots_adjust(wspace=0.4)
plt.show()
