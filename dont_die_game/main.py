from dont_die_game.chatbot import MyChatbot

if __name__ == "__main__":
    # Initialize the chatbot
    chatbot = MyChatbot()
    
    # Start the greeting process
    chatbot.greeting()

    # Enter the main conversation loop
    while chatbot.conversation_is_active:
        chatbot.respond()

    # End with a farewell message
    chatbot.farewell()