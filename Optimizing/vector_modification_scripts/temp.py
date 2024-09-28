import sys
import os

conf_path = os.getcwd()
sys.path.append('D:/git/STS/Optimizing/')

from resources.open_ai_api_key import open_ai_api_key

print(open_ai_api_key)
