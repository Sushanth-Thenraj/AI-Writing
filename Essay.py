import os
from google import genai
from google.genai import types
from colorama import init, Fore, Style
import config

init(autoreset=True)

client = genai.Client(api_key=config.GEMINI_API_KEY)

def generate_response(prompt, temperature=0.3):
    try:
        contents= [types.Content
                    (role= "user",
                    parts= types.Part.from_text
                    (text=prompt
                 )
            )
        ]
        config_params= types.GenerateContentConfig(
            temperature=temperature
        )
        response= client.model.generate_content(
            model= "gemini-2.0-flash",
            contents= contents,
            config= config_params
        )
        return response.text
    except Exception as e:
        print(Fore.RED + "Error generating response:", e)
        return None
    
def get_essay_details():
    print(f"{Fore.CYAN}Welcome to the Essay Generator!")

    topic = input(f"{Fore.YELLOW}Enter the essay topic: {Style.RESET_ALL}")

    type= input(f"{Fore.YELLOW}Enter the essay type (e.g., argumentative, descriptive): {Style.RESET_ALL}")

    print(f"{Fore.GREEN} Here is a list of the Word Counts: ")
    print(f"{Fore.MAGENTA}1. 300 words")
    print(f"{Fore.MAGENTA}2. 600 words")
    print(f"{Fore.MAGENTA}3. 900 words")
    print(f"{Fore.MAGENTA}4. 1200 words")
    word_count_choice = int(input(f"{Fore.YELLOW}Choose a word count (1-4): {Style.RESET_ALL}"))
    word_count_dict= {1:300, 2:600, 3:900, 4:1200}
    length= word_count_dict.get(word_count_choice, 300)

    target_audience = input(f"{Fore.YELLOW}Enter the target audience (e.g., high school students, professionals): {Style.RESET_ALL}")
    specific_points= input(f"{Fore.YELLOW}Enter any specific points to include (optional): {Style.RESET_ALL}")

    stance= input(f"{Fore.YELLOW}Enter your stance (e.g., for, against, neutral): {Style.RESET_ALL}")

    references= input(f"{Fore.YELLOW}Any references or sources to include? (optional): {Style.RESET_ALL}")

    writing_style= input(f"{Fore.YELLOW}Preferred writing style (e.g., formal, informal, persuasive): {Style.RESET_ALL}")

    outline= input(f"{Fore.YELLOW}Do you want an outline before the essay? (yes/no): {Style.RESET_ALL}").lower()

    return{
        "topic": topic,
        "type": type,
        "length": length,
        "target_audience": target_audience,
        "specific_points": specific_points,
        "stance": stance,
        "references": references,
        "writing_style": writing_style,
        "outline": outline
    }

def generate_essay(details):

    response_temperature= input(f"{Fore.YELLOW}Enter the response temperature (0.0 - 1.0, default 0.3): {Style.RESET_ALL}")

    introduction_prompt = f"Write an introduction for a {details['length']}-word {details['type']} essay on the topic '{details['topic']}' targeted at {details['target_audience']}. The writing style should be {details['writing_style']}. "
    introduction= generate_response(introduction_prompt, response_temperature)
    print("|||Generated Introduction|||")
    print(Fore.GREEN + introduction)

    body_style= int(input(f"{Fore.YELLOW}Choose body generation style - (1) Full Essay or (2) Section by Section: {Style.RESET_ALL}"))
    if body_style == '1':
        body_prompt = f"Continue the essay with a detailed body for the topic '{details['topic']}' including the following points: {details['specific_points']}. The essay should be {details['length']} words long, targeted at {details['target_audience']}, and written in a {details['writing_style']} style. The stance is {details['stance']}. Include references: {details['references']}."
        body= generate_response(body_prompt, response_temperature)
        print("|||Generated Body|||")
        print(Fore.GREEN + body)
    else:
        body_step_prompt = f"Write a section of the essay on '{details['topic']}' including the point: {details['specific_points']}. The essay should be {details['length']} words long, targeted at {details['target_audience']}, and written in a {details['writing_style']} style. The stance is {details['stance']}. Include references: {details['references']}."
        
        body_step = generate_response(body_step_prompt, response_temperature)
        print(Fore.CYAN + "\n=== Generated Step-by-Step Body ===")
        print(Fore.GREEN + body_step)


    conclusion_prompt = f"Write a conclusion for an {details['essay_type']} essay about {details['topic']} on the topic of {details['theme']}."
    conclusion = generate_response(conclusion_prompt, response_temperature)
    (Fore.CYAN + "\n=== Generated Conclusion ===")
    print(Fore.GREEN + conclusion)

def feedback_and_refinement():
    satisfaction = int(input("Rate your satisfaction with the generated content. (Rate from 1 to 5 stars): "))
    if satisfaction <= 3:
        print(Fore.YELLOW + "We appreciate your feedback! We can improve the content (tone, structure, etc.)")
        input(Fore.YELLOW)
    else:
        print(Fore.CYAN + "Thank you for your feedback! We will refine the essay based on your input. Feedback:")
        input(Fore.YELLOW)
        print(Fore.CYAN + "Thank you for the feedback! The essay looks good.")

# Main Function
def run_activity():
    print(Fore.CYAN + "\nWelcome to the AI Writing Assistant!")

    # Get essay details from UI
    details = get_essay_details()

    # Generate the essay content based on the details
    generate_essay(details)

    # Ask for feedback and refine
    feedback_and_refinement()

# Run the Activity
if __name__ == "__main__":
    run_activity() 
