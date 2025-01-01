import httpx
import re

class RestoreCord:
    def __init__(self, proxy):
        self.proxy = proxy
        self.session = httpx.Client(proxies=self.proxy, headers={
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
        })

    def bypass_restorecord(self, token, guild_id):
        try:
            response = self.session.get(f"https://restorecord.com/verify/{guild_id}")
            match = re.search('clientId":"(\d+?)"', response.text)

            if not match:
                print(f"Failed to extract client ID for guild {guild_id}")
                return False

            client_id = match.group(1)

            oauth_response = self.session.post(
                "https://discord.com/api/v9/oauth2/authorize",
                params={
                    'client_id': client_id,
                    'response_type': 'code',
                    'redirect_uri': 'https://restorecord.com/api/callback',
                    'scope': 'identify guilds.join',
                    'state': guild_id
                },
                json={'permissions': '0', 'authorize': True},
                headers={'Authorization': token}
            )

            if oauth_response.status_code == 429:
                print("Ratelimited during bypass attempt")
                return False

            if oauth_response.status_code != 200:
                print(f"Failed to bypass: {oauth_response.json()}")
                return False

            print(f"Bypassed: {guild_id}")
            return True

        except Exception as e:
            print(f"Error occurred: {e}")
            return False

# Very basic example usage :L
proxy = {'http': 'http://proxy.example.com:8080'}
discord = RestoreCord(proxy=proxy)
discord.bypass_restorecord(token="discord-token", guild_id="your-guild-id")
