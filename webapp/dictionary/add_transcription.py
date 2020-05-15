from webapp import create_app
from webapp.db import db
from webapp.dictionary.models import EnglishWord
from webapp.dictionary.get_transcription import get_transcription

app = create_app()

# a script to add transcriptions for English words in website common dictionary, if they do not have them
with app.app_context():
    all_eng_words_in_db = EnglishWord.query.order_by(EnglishWord.id).all()
    for engword in all_eng_words_in_db:
        word = engword.word_itself
        transcription = get_transcription(word)
        engword.transcription = transcription
        db.session.commit()
