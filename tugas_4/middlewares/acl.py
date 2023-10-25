from pyramid.security import ALL_PERMISSIONS


def add_role_principals(userid, request):
    return [f'{request.jwt_claims.get("role", [])}']
    # return [f'role:{request.jwt_claims.get("role", [])}']
