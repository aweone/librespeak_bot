from auth import vk


def get_admin(peerid, groupid):
    try:
        admins = []
        admins_str = ""
        members = vk.messages.getConversationMembers(
            peer_id=peerid, group_id=groupid)["items"]
        for member in members:
            if "is_admin" in member:
                admins.append(member["member_id"])
                if member["member_id"] > 0:
                    admins_str += ("\n @id"+str(member["member_id"]))
        return admins_str, admins
    except Exception:
        admins = []
        admins_str = ""
        return admins_str, admins
