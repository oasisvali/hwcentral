from edge.models import Tick


def register_tick(student, question, mark):
    new_tick = Tick(student=student, question=question, mark=mark)
    new_tick.save()
