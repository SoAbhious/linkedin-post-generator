from llm_helper import llm
from few_shot import FewShotPosts
import re

few_shot = FewShotPosts()


def get_length_str(length):
    if length == "Short":
        return "1 to 5 lines"
    if length == "Medium":
        return "6 to 10 lines"
    if length == "Long":
        return "11 to 15 lines"


def get_prompt(length, purpose, topic):
    prompt = f'''
        Generate LinkedIn post using the below information. No preamble.

        1) Topic: {topic}
        2) Length: {length}
        3) Purpose: {purpose}


        '''
    examples = few_shot.get_filtered_posts(length, purpose, topic)
    if len(examples) > 0:
        prompt += "4) Use the writing style as per the following examples."
        for i, post in enumerate(examples):
            post_text = post["text"]
            prompt += f"\n\n Example {i+1}: \n\n {post_text}"
            if i == 3:
                break
    return prompt


def clean_post_text(text):
    text = re.sub(r'\b(?:Hashtags?:?|Tags?:?)\s*', '', text, flags=re.IGNORECASE)
    hashtags = re.findall(r'#\w+', text)
    text = re.sub(r'\s*#\w+', '', text)

    if hashtags:
        text = text.strip() + "\n\n" + " ".join(hashtags)

    return text.strip()


def generate_post(length, purpose, topic):
    prompt = get_prompt(length, purpose, topic)
    response = llm.invoke(prompt)
    post = clean_post_text(response.content)
    return post


if __name__ == "__main__":
    post = generate_post("Medium", "Share a personal story", "Technology")
    # post = post.replace("Hashtag", "").replace("Hashtags", "").strip()
    print(post)
