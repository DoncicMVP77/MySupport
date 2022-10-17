

def filter_by_group(request, group_name) -> bool:
    if request.user.groups.filter(name=group_name):
        return True
    return False

