import pandas as pd
from datetime import datetime, timedelta
import dataframe_image as dfi

# Calculate the number of days in the year
start_date = datetime(2023, 1, 1)
end_date = datetime(2024, 1, 1)
delta = end_date - start_date
days_in_year = delta.days

# Create a DataFrame with a date range for the year
df = pd.DataFrame()
df['date'] = [start_date + timedelta(days=i) for i in range(days_in_year)]

# Calculate the savings amount for each day
df['savings'] = df['date'].apply(lambda x: x.month + x.day/100)

# Calculate the cumulative sum of the savings
df['cumulative_sum'] = df['savings'].cumsum()

# Convert the DataFrame to a wide format with each month as a column
df['month'] = df['date'].dt.strftime('%B')
df['day'] = df['date'].dt.day

# Stack savings and cumulative sum into multi-index columns
df.set_index(['day', 'month'], inplace=True)
df = df.stack().reset_index()
df.columns = ['day', 'month']

# Sort columns to ensure 'savings' appears before 'cumulative_sum'
df['type'] = pd.Categorical(df['type'], categories=['savings', 'cumulative_sum'], ordered=True)
df.sort_values(by=['day', 'month'], inplace=True)

# Drop rows where 'day' is null before pivoting
# df.dropna(subset=['day'], inplace=True)

# Pivot the DataFrame
df_wide = df.pivot(index='day', columns=['month'])

# Fill 'nan' cells with 'N/A'
df_wide.fillna('N/A', inplace=True)

# Make borders bolder by applying styles
df_styled = df_wide.style.set_table_styles([
    {'selector': 'th', 'props': 'border: 1px solid black'},
    {'selector': 'td', 'props': 'border: 1px solid black'}
])

# Save DataFrame as an image
dfi.export(df_styled, 'df_styled.jpg', max_rows=-1, max_cols=-1)
