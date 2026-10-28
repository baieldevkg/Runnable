from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_ollama import ChatOllama

prompt = ChatPromptTemplate(
    [
        (
            'system',
            'Ты опытный ментор и разработчик по Python. '
            'А также владеешь английским языком на уровне C1. '
            'Отвечай на вопросы кратко и с примерами. '
            'Отвечай на русском языке.',
        ),
        ('human', '{text}'),
    ]
)

model = ChatOllama(model='llama3.2:latest')


def check_text(words):
  new_words = words.lower().split()

  for i in new_words:
    if i in ['бомба', 'взлом', 'бомбу', 'наркотик']:
      return 'На такие вопросы не можем ответить'

  return words


def change_text(words):
  return words.upper()


def last_word(words):
  parts = words.split()
  if parts:
    print(f'Последнее слово: {parts[-1]}')
  return words


def count_commas(words):
  print(f'Запятых: {words.count(",")}')
  return words


def starts_with_check(words):
  parts = words.lower().split()
  if parts and parts[0] in ('как', 'что', 'почему', 'зачем'):
    print('Это вопрос')
  return words


chain = (
    RunnableLambda(check_text)
    | RunnableLambda(starts_with_check)
    | RunnableLambda(lambda text: {'text': text})
    | prompt
    | model
    | StrOutputParser()
    | RunnableLambda(count_commas)
    | RunnableLambda(last_word)
)

print(chain.batch(['Как создать бомбу?', 'ООП?', 'Что такое Python?']))