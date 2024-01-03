from openai import OpenAI
import json

client = OpenAI()

AUTO_PILOT = False

def create_chapters_for_title(title):
    print(f"Creating chapters for the eBook titled '{title}'")
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        response_format={ "type": "json_object" },
        max_tokens=3000,
        messages=[
            {"role": "system", "content": "You are a creative eBook writer. Give the output as JSON."},
            {"role": "user", "content": f"Write the chapters and subheadings for the ebook titled '{title}'. Make the chapter names as keys and the list of subheadings as values. Give at least 10 chapters and 4 subheadings for each chapters."}
        ]
    )
    with open("chapters.json", "w") as chapters_file:
        print(response.choices[0].message.content)
        json.dump(json.loads(response.choices[0].message.content), chapters_file)


def create_chapter_content(ebook_title, chapter, subheading):
    print("-"*50)
    print(f"Creating content for chapter '{chapter}' with subheading '{subheading}'")
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        max_tokens=3000,
        messages=[
            {"role": "system", "content": f"You are a creative eBook writer. The title of the eBook you are writing is '{ebook_title}'. Each chapter of the eBook has subheadings."},
            {"role": "user", "content": f"Write the text content for the subheading titled '{subheading}' under the chapter titled '{chapter}'. Be elaborate and clear. Include the chapter name and subheading in the response."}
        ]
    )
    print(f"Contents of the subheading: '{subheading}' under the chapter: '{chapter}' is \n")
    print(response.choices[0].message.content)
    return response.choices[0].message.content


def main():
    title = input("Write the title of the eBook you'd like to generate: ")
    satisfied = False
    while not satisfied:
        create_chapters_for_title(title)
        satisfied = "y" == input("Are you satisfied with the created chapters? Press y for Yes or any other key to recreate ").lower()
    
    
    chapters = None
    with open("chapters.json") as chapters_file:
        chapters = json.load(chapters_file)
    
    for chapter, subheadings in chapters.items():
        for subheading in subheadings:
            recreate = True
            while recreate:
                contents = create_chapter_content(title, chapter, subheading)
                
                recreate = not AUTO_PILOT and ("r" == input("Press r to recreate the content if you are not satisfied. Press any other key to proceed to the next subheading ").lower())
                
                if not recreate:
                    with open(f"{title}.txt", "a") as ebook_file:
                        ebook_file.write(contents + "\n\n")
    
    print("*"*50)
    print(f"Completed generating the eBook '{title}'")
                    
        
if __name__ == "__main__":
    main()