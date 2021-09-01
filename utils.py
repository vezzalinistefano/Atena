def type_error_management(form, field):
    form._errors[field] = form.error_class([
        f'This field can\'t be blank'])
