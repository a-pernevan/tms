from ldap3 import NTLM
from ms_active_directory import ADDomain

domain = ADDomain('tauros.lan')
try: 
    session = domain.create_session_as_user('andrei@tauros.lan', 'Ar10fiatbti$')
    print(session)
    print("User authenticated successfully!")
except Exception as e:
    print(f"Eroare: {e}")
