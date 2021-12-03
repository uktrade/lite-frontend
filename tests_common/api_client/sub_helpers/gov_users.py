class GovUsers:
    def __init__(self, api_client, request_data, **kwargs):
        super().__init__(**kwargs)
        self.api_client = api_client
        self.request_data = request_data

    def put_test_user_in_team(self, team_name):
        response = self.api_client.make_request(
            method="GET", url="/teams/?disable_pagination=True", headers=self.api_client.gov_headers
        )
        team_list = response.json()["teams"]
        team_id = None
        for team in team_list:
            if team["name"] == team_name:
                team_id = team["id"]
        self.api_client.make_request(
            method="PUT",
            url=f"/gov-users/{self.api_client.context['gov_user_id']}/",
            headers=self.api_client.gov_headers,
            body={"team": team_id, "default_queue": "00000000-0000-0000-0000-000000000001"},
        )
