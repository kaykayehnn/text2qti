from pathlib import Path

from text2qti.qti import QTI
from text2qti.config import Config
from text2qti.quiz import Quiz

def main():
  text = Path("quiz.txt").read_text()
  config = Config()
  config['latex_render_url'] = "https://canvas.instructure.com/equation_images/"
  quiz = Quiz(text, config=config)
  qti = QTI(quiz)
  print(123)
  qti.save("quiz.zip")

main()