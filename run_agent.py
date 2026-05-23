import os
import sys

# Add the current directory to sys.path to allow absolute imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    from agent.monitor import CryptrixAgent
    agent = CryptrixAgent()
    agent.run()
