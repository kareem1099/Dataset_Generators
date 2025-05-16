import random
import pandas as pd

AR_templates = {
    
}

placeholders={

}
EN_templates={

}
english_placeholders = {
    
}

# Function to generate a single post
def generate_post(template, placeholders, template_type):
    symptom = random.choice(placeholders["symptom"])
    activity = random.choice(placeholders["activity"]) if "{activity}" in template else ""
    time = random.choice(placeholders["time"]) if "{time}" in template else ""
    condition = random.choice(placeholders["condition"]) if "{condition}" in template else ""

    try:
        return template.format(symptom=symptom, activity=activity, time=time, condition=condition)
    except KeyError:
        return template.format(symptom=symptom)

# Function to generate unique posts
def generate_posts(templates, placeholders, num_posts, template_type_counts, used_posts):
    posts = []
    target_per_type = num_posts // len(templates)
    
    for template_type, template_list in templates.items():
        target_count = template_type_counts[template_type]
        current_count = 0
        attempts = 0
        max_attempts = 10000

        while current_count < target_count and attempts < max_attempts:
            template = random.choice(template_list)
            post = generate_post(template, placeholders, template_type)
            if post not in used_posts:
                posts.append(post)
                used_posts.add(post)
                current_count += 1
                template_type_counts[template_type] -= 1
            attempts += 1

        if current_count < target_count:
            print(f"Warning: Only generated {current_count}/{target_count} unique posts for type '{template_type}'")

    return posts

# Main generation function
def main():
    used_arabic_posts = set()
    used_english_posts = set()

    template_type_counts_ar = {
        "short": 500,
        "question": 500,
        "narrative": 500,
        "help": 500
    }

    template_type_counts_en = {
        "short": 500,
        "question": 500,
        "narrative": 500,
        "help": 500
    }

    print("Generating Arabic posts...")
    arabic_posts = generate_posts(AR_templates, placeholders, 2000, template_type_counts_ar, used_arabic_posts)

    print("Generating English posts...")
    english_posts = generate_posts(EN_templates, english_placeholders, 2000, template_type_counts_en, used_english_posts)

    # Combine both into a single dataset
    data = [{"post": post, "Tag": "category"} for post in arabic_posts + english_posts] #replace category with every diesese each time

    df = pd.DataFrame(data)
    df.to_csv("knee_posts.csv", index=False, encoding="utf-8")

    print(f"Done! Generated {len(arabic_posts)} Arabic and {len(english_posts)} English posts.")
    print("File saved as: knee_posts.csv")

# Run the script
if __name__ == "__main__":
    main()
