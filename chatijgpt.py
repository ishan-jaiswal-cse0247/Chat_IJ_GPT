import os
import sys
from dotenv import load_dotenv
from flask import Flask, render_template, request
from flask import url_for
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from langchain_openai.chat_models import ChatOpenAI
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain_community.llms import OpenAI
from langchain_community.vectorstores import Chroma

load_dotenv()

#Only to remove some unnecessary warnings 
import warnings
warnings.filterwarnings('ignore')
warnings.warn('Error: A warning just appeared')
print('initializing IJ bot')

#Flask for UI
app = Flask(__name__)
#app.add_url_rule('/favicon.ico', redirect_to=url_for('static', filename='favicon.ico'))

#API Key
os.environ["OPENAI_API_KEY"] = os.getenv("APIKEY")

# Enable to save to disk & reuse the model (for repeated queries on the same data)
PERSIST = False
query = None
if len(sys.argv) > 1:
  query = sys.argv[1]
if PERSIST and os.path.exists("persist"):
  print("Reusing index...\n")
  vectorstore = Chroma(persist_directory="persist", embedding_function=OpenAIEmbeddings())
  index = VectorStoreIndexWrapper(vectorstore=vectorstore)
else:
  loader = TextLoader("data/data.txt") # Use this line if you only need data.txt
  #loader = DirectoryLoader("data/")
  if PERSIST:
    index = VectorstoreIndexCreator(vectorstore_kwargs={"persist_directory":"persist"}).from_loaders([loader])
  else:
    index = VectorstoreIndexCreator().from_loaders([loader])

chain = ConversationalRetrievalChain.from_llm(
  llm=ChatOpenAI(model="gpt-3.5-turbo"),
  retriever=index.vectorstore.as_retriever(search_kwargs={"k": 1}),
)

chat_history = []

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/get")
def get_bot_response():
    global chat_history
    user_input = request.args.get("msg")
    
    if user_input.lower() in ['quit', 'q', 'exit','bye','goodbye']:
        return 'Have a Grate day ahead, Namaste 🙏'

    result = chain({"question": user_input, "chat_history": chat_history})
    chat_history.append((user_input, result['answer']))
    
    return result['answer']

#if __name__ == "__main__":
#    app.run()


#while True:
#  if not query:
#    query = input("Prompt: ")
#  if query in ['quit', 'q', 'exit']:
#    print('Have a Grate day ahead, Namaste 🙏')
#    sys.exit()
#  result = chain({"question": query, "chat_history": chat_history})
#  print(result['answer'])

#  chat_history.append((query, result['answer']))
#  query = None


#@app.route("/get")
#def get_bot_response():
#    userText = request.args.get('msg')
#    return str(chatbot.get_response(userText))


