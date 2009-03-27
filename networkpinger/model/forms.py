import formencode

class AddNote(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    short = formencode.validators.String(not_empty=True)
    long  = formencode.validators.String(if_missing=None)
