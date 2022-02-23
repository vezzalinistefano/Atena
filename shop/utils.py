from shop.models import Course


def check_if_teacher(teacher_id=None, course_id=None):
    print(course_id)
    course = Course.objects.get(id=course_id)
    return course.check_if_teacher(teacher_id)

