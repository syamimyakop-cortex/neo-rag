import langchain
import pkgutil

print(f"LangChain version: {langchain.__version__}")
print(f"LangChain path: {langchain.__path__}")

try:
    from langchain.chains import RetrievalQA
    print("Success: from langchain.chains import RetrievalQA")
except ImportError as e:
    print(f"Failed: {e}")

try:
    from langchain_community.chains import RetrievalQA
    print("Success: from langchain_community.chains import RetrievalQA")
except ImportError as e:
    print(f"Failed community: {e}")
