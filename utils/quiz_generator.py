import random

def generate_mcq(chunks):
    quiz = []
    for c in random.sample(chunks, min(5, len(chunks))):
        words = c["content"].split()
        if len(words) < 6:
            continue
        answer = random.choice(words)
        question = c["content"].replace(answer, "_____")

        options = random.sample(words, 3)
        options.append(answer)
        random.shuffle(options)

        quiz.append({
            "question": question,
            "options": options,
            "answer": answer
        })
    return quiz
