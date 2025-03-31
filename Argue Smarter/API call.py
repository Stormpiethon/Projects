import openai
import os

def get_api_key(filepath="api_key.txt"):
    try:
        with open(filepath, 'r') as f:
            api_key = f.readline().strip()  # Read the first line and remove any whitespace
            return api_key
    except FileNotFoundError:
        print(f"Error: API key file not found at {filepath}")
        return None
    except Exception as e:
        print(f"An error occurred while reading the API key: {e}")
        return None

# Read the API key from the file
api_key = get_api_key(filepath="api_key.txt")

# Initialize the OpenAI client only if the API key was successfully loaded
if api_key:
    client = openai.OpenAI(api_key=api_key)

    def generate_insult():
        prompt = (
            "Generate a single humorous insult that incorporates exactly three **random, uncommon, and distinct** complex vocabulary words. "
            "Each word must come from a different category: one describing intelligence, one describing physical appearance, and one describing behavior or smell. "
            "Ensure that the words are not commonly used together and do not repeat words from previous responses. "
            "The insult should be highly creative, absurd, and vividly descriptive. "
            "Here are some examples of the type of insult you're aiming for:\n\n"

            "1. 'Your perspicacity is about as sharp as a blunted spoon, and your effluvium makes skunks question their life choices.'\n"
            "   - Perspicacity: Keenness of mental perception.\n"
            "   - Blunted: Made dull or less sharp.\n"
            "   - Effluvium: An unpleasant or harmful odor.\n\n"

            "2. 'Your demeanor is so lugubrious that even rain clouds find you depressing, and your sartorial choices scream ‘lost in a thrift store.’\n"
            "   - Demeanor: Outward behavior or appearance.\n"
            "   - Lugubrious: Looking or sounding sad and dismal.\n"
            "   - Sartorial: Related to clothing or fashion.\n\n"

            "3. 'You have the panache of a confused ostrich, the olfactory charm of a gym sock, and the erudition of a goldfish.'\n"
            "   - Panache: Flamboyant confidence or style.\n"
            "   - Olfactory: Related to the sense of smell.\n"
            "   - Erudition: Deep, scholarly knowledge.\n\n"

            "4. 'Your prolix explanations make even sloths impatient, and your penchant for hyperbole is almost as unbearable as your halitosis.'\n"
            "   - Prolix: Using too many words; overly wordy.\n"
            "   - Penchant: A strong liking for something.\n"
            "   - Halitosis: Chronic bad breath.\n\n"

            "5. 'Your countenance radiates a serendipitous mix of confusion and misplaced confidence, with a fragrance reminiscent of antique cheese.'\n"
            "   - Countenance: A person's facial expression.\n"
            "   - Serendipitous: Happening by chance in a happy or beneficial way.\n"
            "   - Reminiscent: Tending to remind one of something.\n\n"

            "Now, using the same style and format as the examples above, generate a new insult following the rules:\n\n"
            "Insult: [Hilarious insult containing three distinct complex words]\n\n"
            "Word 1: [Complex word 1]\n"
            "Definition: [Definition of word 1]\n"
            "Synonyms: [Synonym 1a, Synonym 1b, Synonym 1c]\n"
            "Antonyms: [Antonym 1a, Antonym 1b, Antonym 1c]\n\n"
            "Word 2: [Complex word 2]\n"
            "Definition: [Definition of word 2]\n"
            "Synonyms: [Synonym 2a, Synonym 2b, Synonym 2c]\n"
            "Antonyms: [Antonym 2a, Antonym 2b, Antonym 2c]\n\n"
            "Word 3: [Complex word 3]\n"
            "Definition: [Definition of word 3]\n"
            "Synonyms: [Synonym 3a, Synonym 3b, Synonym 3c]\n"
            "Antonyms: [Antonym 3a, Antonym 3b, Antonym 3c]\n\n"
            "Be as creative, vivid, and unpredictable as possible!"
        )

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=500
        )

        return response.choices[0].message.content.strip()

    # Call the function and print the output
    print(generate_insult())
else:
    print("OpenAI client could not be initialized. Check the API key file.")