import json
import pandas as pd


class FewShotPosts:
    def __init__(self, filepath="data/processed_posts.json"):
        self.df = None
        self.unique_tags = None
        self.purposes = None
        self.load_posts(filepath)

    def load_posts(self, file_path):
        with open(file_path, encoding="utf-8") as f:
            posts = json.load(f)
            self.df = pd.json_normalize(posts)
            self.df['length'] = self.df['line_count'].apply(self.categorize_length)
            all_tags = self.df['tags'].apply(lambda x: x).sum()
            self.unique_tags = set(list(all_tags))
            self.purposes = self.df['purpose'].unique().tolist()

    def categorize_length(self, line_count):
        if line_count < 5:
            return "Short"
        elif 5 <= line_count <= 10:
            return "Medium"
        else:
            return "Long"

    def get_tags(self):
        return self.unique_tags

    def get_filtered_posts(self, length, purpose, tag):
        df_filtered = self.df[
            (self.df['purpose'] == purpose) &
            (self.df['length'] == length) &
            (self.df['tags'].apply(lambda tags: tag in tags))
        ]
        return df_filtered.to_dict(orient="records")


if __name__ == "__main__":
    fs = FewShotPosts()
    posts = fs.get_filtered_posts("Medium", "Share a personal story", "Technology")
    print(posts)