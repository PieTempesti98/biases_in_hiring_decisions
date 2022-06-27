import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud


# load CSV data in a pandas
df = pd.read_csv('data/keyphrases_2.csv')

# Create dictionaries out of the dataframe
records = df.to_dict(orient='records')
data = {x['Keyphrase']: x['Count'] for x in records}

# Generate word cloud from frequencies
wc = WordCloud(background_color="white", max_words=1000, colormap='Blues')
wc.generate_from_frequencies(data)

# Show final result
plt.imshow(wc, interpolation="bilinear")
plt.axis("off")
plt.show()

