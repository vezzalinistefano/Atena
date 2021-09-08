from shop.models import Course


def check_if_teacher(teacher_id=None, course_id=None):
    course = Course.objects.get(id=course_id)
    return course.teacher_id == teacher_id

