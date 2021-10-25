from bot.core.configs import roles_config


def get_all_ranks_dict():
    return roles_config.officer_roles | roles_config.soldier_roles


def get_officers_ranks_dict():
    return roles_config.officer_roles


def get_soldier_ranks_dict():
    return roles_config.soldier_roles


def get_all_ranks_id():
    return list(get_all_ranks_dict().keys())


def get_officers_ranks_id():
    return list(get_officers_ranks_dict().keys())


def get_soldier_ranks_id():
    return list(get_soldier_ranks_dict().keys())


def get_all_ranks_name():
    return [a[1] for a in list(get_all_ranks_dict().items())]


def get_officers_ranks_name():
    return [a[1] for a in list(get_officers_ranks_dict().items())]


def get_soldier_ranks_name():
    return [a[1] for a in list(get_soldier_ranks_dict().items())]


def get_officer_rank_number(rank):
    if isinstance(rank, int):
        return get_officers_ranks_id(rank).index() + 1
    elif isinstance(rank, str):
        return get_officers_ranks_name(rank).index() + 1


def get_soldier_rank_number(rank):
    if isinstance(rank, int):
        return get_soldier_ranks_id().index(rank) + 1
    elif isinstance(rank, str):
        return get_soldier_ranks_name().index(rank) + 1


def get_global_rank_number(rank):
    if isinstance(rank, int):
        return get_all_ranks_id().index(rank) + 1
    elif isinstance(rank, str):
        return get_all_ranks_name().index(rank) + 1


def get_member_rank(member, str=False):
    member_roles_set = set([role.id for role in member.roles])
    role_id = list(member_roles_set.intersection(get_all_ranks_id()))[0]

    if str:
        return get_all_ranks_dict()[role_id]
    else:
        return role_id


def get_next_member_rank(member, str=False):
    member_roles_set = set([role.id for role in member.roles])
    role_id = list(member_roles_set.intersection(get_all_ranks_id()))[0]
    new_role_id = get_all_ranks_id()[get_all_ranks_id().index(role_id) + 1]
    if str:
        return get_all_ranks_dict()[new_role_id]
    else:
        return new_role_id


def get_previous_member_rank(member, str=False):
    member_roles_set = set([role.id for role in member.roles])
    role_id = list(member_roles_set.intersection(get_all_ranks_id()))[0]
    new_role_id = get_all_ranks_id()[get_all_ranks_id().index(role_id) - 1]
    if str:
        return get_all_ranks_dict()[new_role_id]
    else:
        return new_role_id


def get_rank_id_by_name(name):
    return list(get_all_ranks_dict().keys())[list(get_all_ranks_dict().values()).index(name)]


def get_rank_name_by_id(id):
    return get_all_ranks_dict()[id]


def if_rank_member1_above_member2(member1, member2):
    member1_rank = get_member_rank(member1)
    member2_rank = get_member_rank(member2)
    member1_rank_numb = get_global_rank_number(member1_rank)
    member2_rank_numb = get_global_rank_number(member2_rank)

    if member1_rank_numb > member2_rank_numb:
        return True
    else:
        return False


def if_member_can_up_officers(member):
    return get_member_rank(member, str=True) in get_officers_ranks_name()[4:10]
