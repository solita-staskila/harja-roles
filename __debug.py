import __utils as u
from collections import defaultdict, Counter


def debug_role_parsing(roles_dict, contract_ids, contract_names):
    """
    TODO 
    Ei käytetä, debug
    """
    print("========== DEBUG ROLE PARSING ==========")

    # 1
    keys_list = list(roles_dict.keys())
    print(f"\nroles_dict {len(keys_list)} keys total.\n")

    limit = 10

    # 2
    print(f"Ensimmäiset ~{limit} avainta roles_dict:\n--------------------------------")
    for i, k in enumerate(keys_list[:limit]):
        print(f"{i+1}: {k}")
    if len(keys_list) > limit:
        print(f"... (plus {len(keys_list) - limit} more) ...")
    print("--------------------------------\n")

    # 3
    print(f"contract_ids (total {len(contract_ids)}):\n--------------------------------")
    for i, cid in enumerate(contract_ids[:limit]):
        print(f"{i+1}: {cid}")
    if len(contract_ids) > limit:
        print(f"... (plus {len(contract_ids) - limit} more) ...")
    print("--------------------------------\n")

    # 4
    print(f"contract_names (total {len(contract_names)}):\n--------------------------------")
    for i, nm in enumerate(contract_names[:limit]):
        print(f"{i+1}: {nm}")
    if len(contract_names) > limit:
        print(f"... (plus {len(contract_names) - limit} more) ...")
    print("--------------------------------\n")

    # 5
    if contract_ids:
        test_cid = contract_ids[0]
        print(f"Täsmäävä string contract_ids[0] = '{test_cid}' vastaan roolien avaimia.")
        matched_keys = [rk for rk in keys_list if test_cid in rk]
        print(f"  Löydettiin {len(matched_keys)} täsmäävää roolia cidllä.")
        for i, mk in enumerate(matched_keys[:limit]):
            print(f"{i+1}: {mk}")
        if len(matched_keys) > limit:
            print(f"... (plus {len(matched_keys) - limit} more) ...")
    else:
        print("Ei sampoditä (contract_ids).")

    print("========== END DEBUG ==========\n")


def invert_roles(roles):
    """
    TODO 
    Ei käytetä, visualisoi dataa

    Rakenna inverted map -> {role_type -> count}.
    Esim.. user_role_counts["alisa@example.com"]["ELY_Laadunvalvoja"] = 2
    """
    user_role_counts = defaultdict(Counter)

    for full_role, user_list in roles.items():
        # 'full_role' esim "PR00053283_ELY_Laadunvalvoja"
        # parsitaan esim "ELY_Laadunvalvoja" tai "Laadunvalvoja"
        base_role = u.parse_name(full_role)

        for user in user_list:
            user_role_counts[user][base_role] += 1

    return user_role_counts


def visualize_user_roles(user_role_counts, top_n_users=10):
    """
    TODO 
    Ei käytetä, visualisoi dataa
    """

    users_sorted = sorted(
        user_role_counts.items(),
        key=lambda item: sum(item[1].values()),  #
        reverse=True
    )

    top_users = users_sorted[:top_n_users]
    print(f"\nTop {top_n_users} käyttäjät eniten rooleja:\n" + "-"*60)

    for user, role_counter in top_users:

        total = sum(role_counter.values())
        print(f"\nKäyttäjä: {user} (roolien määrä: {total})")

        for role_type, count in role_counter.most_common():
            print(f"  {role_type}: {count}")

    print("-"*60)


def detect_duplicates(no_member_roles_for_cid, cid):
    """
    TODO 
    Ei käytetä, katsoo datasta duplikaatit
    """
    counts = Counter(no_member_roles_for_cid)

    duplicates = [role for role, cnt in counts.items() if cnt > 1]
    if duplicates:
        print(f"\nUrakka {cid} duplikaatti roolit:")
        for dup in duplicates:
            print(f"  {dup} laskettu {counts[dup]} kertaa.")


def visualize_empty_roles(roles_without_members):

    empty_role_counts = {}

    for role in roles_without_members:
        role_type = u.parse_name(role)
        empty_role_counts[role_type] = empty_role_counts.get(role_type, 0) + 1

    print("\n")
    print("-" * 60)
    print("Huomioi, onko mergetys käytössä (vain käynnissä olevat + tilaajan roolit mergetty)")
    print("Tyhjät roolit (ei käyttäjiä):  ")
    sorted_items = sorted(empty_role_counts.items(), key=lambda x: x[1], reverse=True)

    total_count = 0 

    for role_type, count in sorted_items:
        total_count += count 
        bar = "=" * min(count, 100)
        print(f"    {role_type:35} | {bar} ({count})")

    print("Tyhjiä yhteensä:", total_count)
    print("-" * 60 + "\n")



def visualize(roles_ongoing, roles_without_members, roles_dict_ongoing):
    empty_role_counts = {}
    sampoidt = roles_ongoing

    """for cid in sampoidt:
        # e.g. "PR00038030", "PR00051752"
        # Etsi korjaus urakoiden roolit, mitä ei käytetä ollenkaan (0 käyttäjää)
        # no_members_list sisältää kaikki tyhjät ('No members') roolit
        no_member_roles_for_cid = [r for r in roles_without_members if cid in r]
        detect_duplicates(no_member_roles_for_cid, cid)

        # Array, jossa korjaus urakan tyhjät roolit
        if no_member_roles_for_cid:
            # Poista nämä tyhjät roolit
            sampoidt = sampoidt - set(no_member_roles_for_cid)

            # print(f"Urakalla {cid} on nämä tyhäjt roolit:")
            for nr in no_member_roles_for_cid:
                role_type = u.parse_name(nr)
                empty_role_counts[role_type] = empty_role_counts.get(role_type, 0) + 1
                # print(f"  {nr}  -> parse_name = {r.__parse_name(nr)}")

    u.log(f"Poistettu tyhjät roolit ylläpidosta (ei vielä realistinen): {len(sampoidt)}")"""

    visualize_empty_roles(roles_without_members)

    user_role_counts = invert_roles(roles_dict_ongoing)
    visualize_user_roles(user_role_counts, top_n_users=10)
