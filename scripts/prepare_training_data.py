import pandas as pd

# Load each session
relaxed_df = pd.read_csv('relaxed_data.csv')
relaxed_df['label'] = 'relaxed'

flexed_df = pd.read_csv('flexed_data.csv')
flexed_df['label'] = 'flexed'

# Combine into one dataset
combined_df = pd.concat([relaxed_df, flexed_df], ignore_index=True)

# Save to a new file
combined_df.to_csv('training_data.csv', index=False)

print("Combined and labeled data saved to 'training_data.csv'")