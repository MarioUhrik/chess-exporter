import os
import time
from prometheus_client import start_http_server, Gauge, Enum
import requests
import yaml

class ChessMetrics:

    def __init__(self, polling_interval_seconds, config_file_path):
        self.polling_interval_seconds = polling_interval_seconds
        self.config_file_path = config_file_path

        # Load config file
        config_file = open(self.config_file_path)
        self.config = yaml.load(config_file)

        # Declare metrics
        self.player_stats = {}
        if self.config["chess_exporter"]["global_filters"]["online"]:
            self.player_stats["online"] = Enum(name="chess_online", documentation="Online status of a player", labelnames=["playerName"], states=["online", "offline", "unknown"])
        if self.config["chess_exporter"]["global_filters"]["rapid"]:
            self.player_stats["chess_rapid"] = {}
            self.player_stats["chess_rapid"]["last"] = {}
            self.player_stats["chess_rapid"]["last"]["rating"] = Gauge(name="chess_rapid_rating_current", documentation="Current chess rating in rapid", labelnames=["playerName"])
            self.player_stats["chess_rapid"]["record"] = {}
            self.player_stats["chess_rapid"]["record"]["win"] = Gauge(name="chess_rapid_wins", documentation="Number of chess wins in rapid", labelnames=["playerName"])
            self.player_stats["chess_rapid"]["record"]["loss"] = Gauge(name="chess_rapid_losses", documentation="Number of chess losses in rapid", labelnames=["playerName"])
            self.player_stats["chess_rapid"]["record"]["draw"] = Gauge(name="chess_rapid_draws", documentation="Number of chess draws in rapid", labelnames=["playerName"])
        if self.config["chess_exporter"]["global_filters"]["blitz"]:
            self.player_stats["chess_blitz"] = {}
            self.player_stats["chess_blitz"]["last"] = {}
            self.player_stats["chess_blitz"]["last"]["rating"] = Gauge(name="chess_blitz_rating_current", documentation="Current chess rating in blitz", labelnames=["playerName"])
            self.player_stats["chess_blitz"]["record"] = {}
            self.player_stats["chess_blitz"]["record"]["win"] = Gauge(name="chess_blitz_wins", documentation="Number of chess wins in blitz", labelnames=["playerName"])
            self.player_stats["chess_blitz"]["record"]["loss"] = Gauge(name="chess_blitz_losses", documentation="Number of chess losses in blitz", labelnames=["playerName"])
            self.player_stats["chess_blitz"]["record"]["draw"] = Gauge(name="chess_blitz_draws", documentation="Number of chess draws in blitz", labelnames=["playerName"])
        if self.config["chess_exporter"]["global_filters"]["bullet"]:
            self.player_stats["chess_bullet"] = {}
            self.player_stats["chess_bullet"]["last"] = {}
            self.player_stats["chess_bullet"]["last"]["rating"] = Gauge(name="chess_bullet_rating_current", documentation="Current chess rating in bullet", labelnames=["playerName"])
            self.player_stats["chess_bullet"]["record"] = {}
            self.player_stats["chess_bullet"]["record"]["win"] = Gauge(name="chess_bullet_wins", documentation="Number of chess wins in bullet", labelnames=["playerName"])
            self.player_stats["chess_bullet"]["record"]["loss"] = Gauge(name="chess_bullet_losses", documentation="Number of chess losses in bullet", labelnames=["playerName"])
            self.player_stats["chess_bullet"]["record"]["draw"] = Gauge(name="chess_bullet_draws", documentation="Number of chess draws in bullet", labelnames=["playerName"])

    def fetch_leaderboard_players(self):
        try:
            resp = requests.get(url=f"https://api.chess.com/pub/leaderboards")
            status_data = resp.json()
        except requests.exceptions.RequestException as e:
            print(e)
            return []

        player_names = []
        leaderboards = self.config["chess_exporter"]["player_stats"]["leaderboards"]
        for leaderboard in leaderboards:
            top = leaderboards[leaderboard]["top"]
            for rank in range (0, top):
                try:
                    player_names.append(status_data[leaderboard][rank]["username"])
                except Exception as e:
                    continue
        return player_names

    def fetch_player_names(self):
        player_names = []
        player_names.extend(self.config["chess_exporter"]["player_stats"]["players"])
        player_names.extend(self.fetch_leaderboard_players())
        return list(dict.fromkeys(player_names))

    def fetch_player_online(self, player_names):
        if self.config["chess_exporter"]["global_filters"]["online"]:
            for player_name in player_names:
                try:
                    resp = requests.get(url=f"https://api.chess.com/pub/player/{player_name}/is-online")
                    status_data = resp.json()
                except requests.exceptions.RequestException as e:
                    print(e)
                    self.player_stats["online"].labels(player_name).state("unknown")
                    continue

                try:
                    is_online = status_data["online"]
                    if is_online == "true":
                         self.player_stats["online"].labels(player_name).state("online")
                    elif is_online == "false":
                         self.player_stats["online"].labels(player_name).state("offline")
                    else:
                         self.player_stats["online"].labels(player_name).state("unknown")
                except Exception as e:
                    self.player_stats["online"].labels(player_name).state("unknown")
                    continue
        
    def fetch_player_stats(self, player_names):
        for player_name in player_names:
            try:
                resp = requests.get(url=f"https://api.chess.com/pub/player/{player_name}/stats")
                status_data = resp.json()
            except requests.exceptions.RequestException as e:
                print(e)
                continue

            try:
                if self.config["chess_exporter"]["global_filters"]["rapid"]:
                    self.player_stats["chess_rapid"]["last"]["rating"].labels(player_name).set(status_data["chess_rapid"]["last"]["rating"])
                    self.player_stats["chess_rapid"]["record"]["win"].labels(player_name).set(status_data["chess_rapid"]["record"]["win"])
                    self.player_stats["chess_rapid"]["record"]["loss"].labels(player_name).set(status_data["chess_rapid"]["record"]["loss"])
                    self.player_stats["chess_rapid"]["record"]["draw"].labels(player_name).set(status_data["chess_rapid"]["record"]["draw"])
                if self.config["chess_exporter"]["global_filters"]["blitz"]:
                    self.player_stats["chess_blitz"]["last"]["rating"].labels(player_name).set(status_data["chess_blitz"]["last"]["rating"])
                    self.player_stats["chess_blitz"]["record"]["win"].labels(player_name).set(status_data["chess_blitz"]["record"]["win"])
                    self.player_stats["chess_blitz"]["record"]["loss"].labels(player_name).set(status_data["chess_blitz"]["record"]["loss"])
                    self.player_stats["chess_blitz"]["record"]["draw"].labels(player_name).set(status_data["chess_blitz"]["record"]["draw"])
                if self.config["chess_exporter"]["global_filters"]["bullet"]:
                    self.player_stats["chess_bullet"]["last"]["rating"].labels(player_name).set(status_data["chess_bullet"]["last"]["rating"])
                    self.player_stats["chess_bullet"]["record"]["win"].labels(player_name).set(status_data["chess_bullet"]["record"]["win"])
                    self.player_stats["chess_bullet"]["record"]["loss"].labels(player_name).set(status_data["chess_bullet"]["record"]["loss"])
                    self.player_stats["chess_bullet"]["record"]["draw"].labels(player_name).set(status_data["chess_bullet"]["record"]["draw"])
            except Exception as e:
                continue
            

    def run_metrics_loop(self):
        while True:
            player_names = self.fetch_player_names()
            self.fetch_player_stats(player_names)
            self.fetch_player_online(player_names)
            time.sleep(self.polling_interval_seconds)

def main():
    chess_metrics = ChessMetrics(
        polling_interval_seconds=int(os.getenv("CHESSEXPORTER_POLLING_INTERVAL_SECONDS", "29")),
        config_file_path=str(os.getenv("CHESSEXPORTER_CONFIG_FILE_LOCATION", "conf/config.yaml"))
    )
    start_http_server(int(os.getenv("CHESSEXPORTER_METRICS_PORT", "80")))
    chess_metrics.run_metrics_loop()

if __name__ == "__main__":
    main()
