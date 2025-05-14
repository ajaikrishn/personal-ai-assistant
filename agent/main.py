from agent.agent_maneger import run_assistant,process_user_input

def handle_input(user_input):
    return process_user_input(user_input)  

def main():
    run_assistant()

if __name__ == "__main__":
    main()
