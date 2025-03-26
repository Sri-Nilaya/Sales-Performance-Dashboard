import pandas as pd

df = pd.DataFrame({
    'A': [1, 2, -3, 4, -5, 9, 8,-00,-100]
})

# Create the boolean mask
mask = df[df['A'] > 0]

print(mask)